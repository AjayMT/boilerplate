#!/usr/bin/env python

"""
Usage: boilerplate <boilerplate-name> [<destination>] [--github | --bitbucket]

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

import docopt
from urllib import urlretrieve
from subprocess import call
from os import remove


def get_boilerplate_type(name):
    if len(name.split('/')) == 2: return 'user/repo'
    if name.startswith(('http://', 'https://')):
        if name.endswith('.zip'): return 'zip'
        if name.endswith(('.tar.gz', '.tgz')): return 'tar'
        if name.endswith('.git'): return 'git'


def main(argv):
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
        contents = urlretrieve(name)
        open('/tmp/bp-file', 'w').write(contents)
        archive_path = '/tmp/bp-file'
        args = ['unzip', archive_path]
        args += ['-d', dest] if dest else []
        if bp_type == 'tar':
            args = ['tar', 'xf', archive_path]
            args += ['-C', dest] if dest else []

        call(args)
        remove(archive_path)


if __name__ == '__main__':
    main(docopt.docopt(__doc__, version='0.0.1'))
