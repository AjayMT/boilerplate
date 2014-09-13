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
  [-p] [--type=(zip | tar | git)]
```
Where `<boilerplate-name>` can be a `<user>/<repo>` stub of a github/bitbucket repository, or a git clone URL, or a link to a zipball/tarball, and `<destination>` is the destination directory.

`--github` is used when `<boilerplate-name>` is in the form of `<user>/<repo>`, and you want to clone the boilerplate from GitHub. This is the default.

`--bitbucket` is used when `<boilerplate-name>` is in the form of `<user>/<repo>`, and you want to clone the boilerplate from Bitbucket.

`--preserve-vcs` or `-p` is used when you don't want `bp` to delete '.git', '.hg' or '.svn' folders after cloning the boilerplate.

`--type` is used when you want to specify the type of the boilerplate (namely `git` for git repositories, `zip` for zipballs and `tar` for tarballs) rather than letting `bp` infer the type based on `<boilerplate-name>`.

`--help` or `-h` will output a similar help message and exit.

`--version` will output the version number and exit.

## Creating boilerplates
Boilerplates can be git repositories, zipballs or tarballs. If your boilerplate is hosted on GitHub or Bitbucket, users can do

```sh
$ bp <user>/<repo>
```

instead of typing in the whole URL.

After a boilerplate has been cloned, its contents are modified to be more project-specific. `bp` will replace a certain pattern (`@name@`) in the paths of files and directories as well as in file contents, with the name of the project the user is creating (which is `<destination>`, as specified above). For example, after a boilerplate is cloned, its contents will be modified from this:

```
.
|-- @name@.rb
|-- Gemfile
`-- README.md
```

into this:

```
.
|-- my-awesome-app.rb
|-- Gemfile
`-- README.md
```

where 'my-awesome-app' is the project. File contents will be modified the same way.

## License
MIT License. See `./LICENSE` for details.

## Contributing
Please contribute! Boilerplate is still very incomplete, so I would welcome help and contributions. Boilerplate is written in python, so it would be best if you tried to follow the PEP8 style guide as much as possible.
