#!/usr/bin/env python

"""
Usage: bp <boilerplate-name> [<destination>]
         [--github | --bitbucket] [-p] [--type=(zip | tar | git)]
       bp (--help | -h)
       bp --version

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
  --type=<type>       Assume that <boilerplate-name> is a zipball, tarball, or
                      a git repository, instead of inferring the type.
  -h, --help          Display this help message and exit.
  --version           Display version number and exit.
"""

import os
import tarfile
import zipfile
from sys import stderr
from shutil import rmtree
from tempfile import gettempdir
from docopt import docopt
from urllib2 import urlopen
from subprocess import call

VERSION = '0.0.2'


def get_files(dirname):
    """Gets and returns a list of files from a directory tree.

    Arguments:
    dirname -- the path of the directory to get the files from
    """
    files = []
    for root, dirnames, filenames in os.walk(dirname):
        files += [os.path.join(root, f) for f in filenames]

    return files


def rename_all(dirname, pattern, replacement):
    """Search for and rename multiple files and directories in a
    directory tree.

    Arguments:
    dirname -- the path of the directory to search
    pattern -- the pattern used to search for files/direcories
    replacement -- the string that replaces 'pattern' in file/directory names
    """
    for root, dirs, files in os.walk(dirname):
        for name in dirs + files:
            os.rename(os.path.join(root, name),
                      os.path.join(root, name.replace(pattern, replacement)))


def modify_files(dirname, pattern, replacement):
    """Replace a specific pattern with a replacement string in the contents
    of all files in a directory tree.

    Arguments:
    dirname -- the path of the directory to rename files in
    pattern -- the pattern to replace in the contents of the files
    replacement -- the string to replace the pattern with in the contents
      of the files
    """
    # We don't want to modify files that are in .git, .hg or .svn directories
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


def download_file(url, path):
    """Download a file and save it to a location.

    Arguments:
    url -- the URL of the file
    path -- the path at which the file will be saved
    """
    contents = urlopen(url).read()
    f = open(path, 'w')
    f.write(contents)
    f.close()


def get_boilerplate_type(name):
    """Get the boilerplate type based on the boilerplate name."""
    if len(name.split('/')) == 2: return 'user/repo'
    if name.startswith(('http://', 'https://')):
        if name.endswith('.zip'): return 'zip'
        if name.endswith(('.tar.gz', '.tgz')): return 'tar'
        if name.endswith('.git'): return 'git'


def main(argv=None):
    if not argv:
        argv = docopt(__doc__, version=VERSION)

    # We only support GitHub and Bitbucket as <user>/<repo> sources for now
    # The type specified with the --type option takes precedence
    # over the the type we infer based on <boilerplate-name>
    name = argv['<boilerplate-name>']
    bp_type = get_boilerplate_type(name) if not argv['--type'] else argv['--type']
    src = 'github' if not argv['--bitbucket'] else 'bitbucket'
    preserve_vcs = argv['--preserve-vcs']
    dest = argv['<destination>']
    dirname = dest

    if argv['--type'] and not dest:
        # We won't try to guess a destination when the type is specified
        print 'You must supply a target directory when using the --type option.'
        dest = raw_input('Target directory: ')
        dirname = dest

    if bp_type == 'user/repo' or bp_type == 'git':
        url = name
        if bp_type == 'user/repo':
            url = 'http://'
            url += 'github.com/' if src == 'github' else 'bitbucket.org/'
            url += name + '.git'

        # We only use the following list comprehension because 'dest'
        # may be None, in which case we'll let git decide
        # what the destination should be
        # We guess repo_name based on the repository URL
        args = ['command', 'git', 'clone', url, dest]
        call([arg for arg in args if arg])
        repo_name = '.'.join(url.split('/')[-1].split('.')[:-1])
        dirname = repo_name if not dirname else dest

    elif bp_type == 'zip' or bp_type == 'tar':
        # We guess archive_name based on the URL of the tarball/zipball
        # i.e the boilerplate name
        archive_ext = '.zip' if bp_type == 'zip' else '.tgz'
        archive_path = os.path.join(gettempdir(),
                                    'bp-file' + archive_ext)
        archive_name = '.'.join(name.split('/')[-1].split('.')[:-1])
        archive = None
        dirname = archive_name if not dirname else dest

        print 'Downloading...'
        download_file(name, archive_path)
        if bp_type == 'tar':
            archive = tarfile.open(archive_path, 'r')
        elif bp_type == 'zip':
            archive = zipfile.ZipFile(archive_path, 'r')

        print 'Extracting...'
        archive.extractall(path=dirname)
        archive.close()
        os.remove(archive_path)

    if not preserve_vcs:
        print 'Removing .git/.hg/.svn folder...'
        # We only remove .git, .hg and .svn folders for now, because
        # these are the mainstream VCSs
        for path in [os.path.join(dirname, p)
                     for p in ('.git', '.hg', '.svn')]:
            if os.path.exists(path): rmtree(path)

    # '@name@' is the pattern that is replaced in the file/directory names
    # and file contents
    print 'Renaming files and directories...'
    rename_all(dirname, '@name@', dirname)
    print 'Changing file contents...'
    modify_files(dirname, '@name@', dirname)
    print 'done.'


if __name__ == '__main__':
    main(docopt(__doc__, version=VERSION))
