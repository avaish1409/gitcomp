# gitcompare

A simple python package to compare git users/ repos via github api

[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPi Download stats](http://pepy.tech/badge/gitcomp)](http://pepy.tech/project/gitcomp)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/avaish1409/gitcomp/releases)


# Installation
 
Install via pip:
```
pip install gitcomp
```

# How to use gitcomp

## Compare Github User profiles

You can use a command in following manner by replacing with desired username. You may compare any number of users simultaneously by providing their username. Example:

```
gitcomp -u avaish1409 Rohitrajak1807
```

## Compare Github Repositories

You can use a command in following manner by replacing with desired username and repository names. You may compare any number of repositoryies simultaneously by providing their credentials. Example:

```
gitcomp -r avaish1409/VideoChatBot Rohitrajak1807/power-management
```


## Specify output type

You can generate the resultant table in: Plain text, CSV, JSON or HTML format easily via specifying output parameter (-o). Example:

```
gitcomp -u avaish1409 -o html
gitcomp -r avaish1409/VideoChatBot Rohitrajak1807/power-management -o json
```

Options:
- Plain Text ( Default )
- CSV ( -o csv )
- JSON ( -o json )
- HTML ( -o html )

# History

See release notes for changes https://github.com/avaish1409/gitcomp/releases


# Development pattern for contributors

1. [Create a fork](https://help.github.com/articles/fork-a-repo/) of
   the [main gitcomp repository](https://github.com/avaish1409/gitcomp) on GitHub.
2. Make your changes in a branch named something different from `main` and titled as per your contribution, e.g. create
   a new branch `documentation-fixes`.
3. [Create a pull request](https://help.github.com/articles/creating-a-pull-request/).
4. Please follow the [Python style guide for PEP-8](https://www.python.org/dev/peps/pep-0008/).


# License

gitcomp is licensed under the [MIT License](https://github.com/avaish1409/gitcomp/blob/main/LICENSE).
