#!/usr/bin/env python

"""
Usage: bp <boilerplate-name> [<destination>] [--github | --bitbucket] [-p]

Where <boilerplate-name> can be a <user>/<repo> stub of
a github/bitbucket repository, or a git clone URL, or a
link to a zipball/tarball, and <destination> is the
destination directory.

Options:
  -p, --preserve-vcs  Don't delete .git, .hg or .svn folders after
                      cloning the boilerplate.
  --github            When <boilerplate-name> is in the form of <user>/<repo>,
                      clone the boilerplate from GitHub. This is the default.
  --bitbucket         When <boilerplate-name> is in the form of <user>/<repo>,
                      clone the boilerplate from Bitbucket.
  -h, --help          Display this help message and exit.
  --version           Display version number and exit.
"""

import os
import shutil
from sys import stderr
from docopt import docopt
from urllib import urlretrieve
from subprocess import call

VERSION = '0.0.2'


def get_files(dirname):
    files = []
    for root, dirnames, filenames in os.walk(dirname):
        files += [os.path.join(root, f) for f in filenames]

    return files


def rename_all(dirname, pattern, replacement):
    for root, dirs, files in os.walk(dirname):
        for name in dirs + files:
            os.rename(os.path.join(root, name),
                      os.path.join(root, name.replace(pattern, replacement)))


def modify_files(dirname, pattern, replacement):
    paths = [f for f in get_files(dirname)
             if not any([s in f for s in ('.git', '.hg', '.svn')])]
    for path in paths:
        try:
            f = open(path, 'r+')
            contents = f.read().replace(pattern, replacement)
            f.seek(0)
            f.write(contents)
            f.close()
        except IOError:
            stderr.write('Error writing to file: %s\n' % path)
            continue


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
    dirname = dest

    if bp_type == 'user/repo' or bp_type == 'git':
        url = name
        if bp_type == 'user/repo':
            url = 'http://'
            url += 'github.com/' if src == 'github' else 'bitbucket.org/'
            url += name + '.git'

        args = ['git', 'clone', url, dest]
        call([arg for arg in args if arg])
        repo_name = '.'.join(url.split('/')[-1].split('.')[:-1])
        dirname = repo_name if not dirname else dest

    elif bp_type == 'zip' or bp_type == 'tar':
        archive_path = os.path.join('/', 'tmp', 'bp-file')
        urlretrieve(name, archive_path)
        archive_name = '.'.join(name.split('/')[-1].split('.')[:-1])
        dirname = archive_name if not dirname else dest
        args = ['unzip', archive_path, '-d', dirname]
        if bp_type == 'tar':
            if not os.path.exists(dirname): os.makedirs(dirname)
            args = ['tar', 'xf', archive_path, '-C', dirname]

        call(args)
        os.remove(archive_path)
        if bp_type == 'tar':
            for file in os.listdir(os.path.join(dirname, 'package')):
                shutil.move(os.path.join(dirname, 'package', file),
                            os.path.join(dirname, file))

            os.rmdir(os.path.join(dirname, 'package'))

    rename_all(dirname, '@name@', dirname)
    modify_files(dirname, '@name@', dirname)


if __name__ == '__main__':
    main(docopt(__doc__, version=VERSION))
