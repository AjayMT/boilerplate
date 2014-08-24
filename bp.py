#!/usr/bin/env python

"""
Usage: bp <boilerplate-name> [<destination>] [--github | --bitbucket]

Where <boilerplate-name> can be a <user>/<repo> stub of
a github/bitbucket repository, or a git clone URL, or a
link to a zipball/tarball, and <destination> is the
destination directory.

Options:
  --github     When <boilerplate-name> is in the form of <user>/<repo>,
               clone the boilerplate from GitHub. This is the default.
  --bitbucket  When <boilerplate-name> is in the form of <user>/<repo>,
               clone the boilerplate from Bitbucket.
  --help -h    Display this help message and exit.
  --version    Display version number and exit.
"""

import os
from docopt import docopt
from urllib import urlretrieve
from shutil import move
from subprocess import call

VERSION = '0.0.2'


def get_boilerplate_type(name):
    if len(name.split('/')) == 2: return 'user/repo'
    if name.startswith(('http://', 'https://')):
        if name.endswith('.zip'): return 'zip'
        if name.endswith(('.tar.gz', '.tgz')): return 'tar'
        if name.endswith('.git'): return 'git'


def main(argv=None):
    if not argv:
        argv = docopt(__doc__, version=VERSION)

    name = argv['<boilerplate-name>']
    bp_type = get_boilerplate_type(name)
    src = 'github' if not argv['--bitbucket'] else 'bitbucket'
    dest = argv['<destination>']

    if bp_type == 'user/repo' or bp_type == 'git':
        url = name
        if bp_type == 'user/repo':
            url = 'http://'
            url += 'github.com/' if src == 'github' else 'bitbucket.org/'
            url += name + '.git'

        args = ['git', 'clone', url, dest]
        call([arg for arg in args if arg])

    elif bp_type == 'zip' or bp_type == 'tar':
        archive_path = os.path.join('/', 'tmp', 'bp-file')
        urlretrieve(name, archive_path)
        dirname = dest or '.'.join(name.split('/')[-1].split('.')[:-1])
        args = ['unzip', archive_path, '-d', dirname]
        if bp_type == 'tar':
            if not os.path.exists(dirname): os.makedirs(dirname)
            args = ['tar', 'xf', archive_path, '-C', dirname]

        call(args)
        os.remove(archive_path)
        if bp_type == 'tar':
            for file in os.listdir(os.path.join(dirname, 'package')):
                move(os.path.join(dirname, 'package', file),
                     os.path.join(dirname, file))

            os.rmdir(os.path.join(dirname, 'package'))


if __name__ == '__main__':
    main(docopt(__doc__, version=VERSION))
