# bp
is a tool to quickly and easily create projects.

It allows you to easily clone/download various project boilerplates, either as git repositories or tarballs/zipballs.

## Installation
You should have Python 2.7. This is the system python on OS X and most Linux distributions.

```sh
$ git clone http://github.com/code-boilerplates/bp.git # Or download a zip/tar and extract it
$ cd bp
$ python setup.py install
```

## Usage
```
bp <boilerplate-name> [<destination>] [--github | --bitbucket]
```
Where `<boilerplate-name>` can be a `<user>/<repo>` stub of a github/bitbucket repository, or a git clone URL, or a link to a zipball/tarball, and `<destination>` is the destination directory.

`--github` is used when `<boilerplate-name>` is in the form of `<user>/<repo>`, and you want to clone the boilerplate from GitHub. This is the default.

`--bitbucket` is used when `<boilerplate-name>` is in the form of `<user>/<repo>`, and you want to clone the boilerplate from Bitbucket.

`--help` or `-h` will output a similar help message and exit.

`--version` will output the version number and exit.

## License
MIT License. See `./LICENSE` for details.

## Contributing
Please contribute! Boilerplate is still very incomplete, so I would welcome help and contributions. Boilerplate is written in python, so it would be best if you tried to follow the PEP8 style guide as much as possible.
