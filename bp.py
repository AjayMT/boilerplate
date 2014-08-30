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
from sys import stderr
from docopt import docopt
from urllib import urlretrieve
from shutil import move
from subprocess import call

VERSION = '0.0.2'


def get_leaf_nodes(path):
    if os.path.isfile(path): return [path]

    paths = []
    contents = os.listdir(path)
    for file in contents:
        filepath = os.path.join(path, file)
        if os.path.isfile(filepath) or len(os.listdir(filepath)) == 0:
            paths.append(filepath)
        else:
            paths += get_leaf_nodes(filepath)

    return paths


def rename_all(paths, pattern, replacement):
    remove_leaf = lambda p: '/'.join(p.split('/')[:-1])
    for path in paths:
        leaf = path.split('/')[-1]
        leaf_name = '.'.join(leaf.split('.')[:-1])
        leaf_ext = leaf.split('.')[-1]
        location = remove_leaf(path)
        if pattern in leaf_name:
            new_name = '.'.join([leaf_name.replace(pattern, replacement),
                                 leaf_ext])
            os.rename(path, os.path.join(location, new_name))

    next_paths = [remove_leaf(path) for path in paths
                  if remove_leaf(path) != '']
    if next_paths == []:
        rename_all(next_paths, pattern, replacement)


def modify_files(dirname, pattern, replacement):
    paths = [f for f in get_leaf_nodes(dirname)
             if os.path.isfile(f)
             and not any([s in f for s in ('.git', '.hg', '.svn')])]
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
                move(os.path.join(dirname, 'package', file),
                     os.path.join(dirname, file))

            os.rmdir(os.path.join(dirname, 'package'))

    rename_all(get_leaf_nodes(dirname), '@name@', dirname)
    modify_files(dirname, '@name@', dirname)


if __name__ == '__main__':
    main(docopt(__doc__, version=VERSION))
