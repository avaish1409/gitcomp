# gitcomp

A simple python package with a CLI to compare GitHub users and repositories by associating a ```git_score``` to each 
entry which is a weighted sum of features mapped to a score. ```git_score``` for a **user** is calculated on the basis of 
**followers, followers to following ratio, number of public gists and number of organisations** a user is part of.
For a **public repository**, the determining factors are **number of forks, if the repository itself is forked or not,
number of stars and number of watchers**.

[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPi Download stats](http://pepy.tech/badge/gitcomp)](http://pepy.tech/project/gitcomp)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![version](https://img.shields.io/badge/version-1.0.1-blue)](https://github.com/avaish1409/gitcomp/releases)


# Installation
 
Install via pip:
```shell
pip install gitcomp
```
```
usage: gitcomp [-h] [-u user_name [user_name ...] | -r repo [repo ...]] [-t output_t] [-o out]

gitcomp A CLI utility to compare the vital stats of GitHub repositories

optional arguments:
  -h, --help            show this help message and exit
  
  -u user_name [user_name ...], --user user_name [user_name ...]
                        -u, --user <username...> The GitHub username(s) to query against.
                        Multiple usernames can be queried at a time by providing a space
                        separated argument list.
                        
  -r repo [repo ...], --repo repo [repo ...]
                        -r, --repo <repo> The public GitHub repository to query against
                        where repo takes the form: <user/repo>
                        Example: -r octocat/Spoon-Knife
                        
  -t output_t, --type output_t
                        -t, --type <type> Default: ascii. Choose the format of output. 
                        All output is dumped to STDOUT unless output file is specified
                        using -o, --output flag.
                        The types available are: json: Show the result as JSON
                                                 csv: Format the output to CSV 
                                                 ascii: Show the result as an ASCII Table 
                                                 html: Show output as HTML Table
                                                 
  -o out, --output out  -o, --output <out_file> Output to out_file, defaults to STDOUT.
```

# Examples

## Comparing Users
```shell
gitcomp -u Rohitrajak1807 avaish1409
```
## Comparing Repositories
```shell
gitcomp -r avaish1409/VideoChatBot Rohitrajak1807/algorithms
```
## Specifying output type
- ASCII Table (Default)
```shell
gitcomp -u Rohitrajak1807 avaish1409 -t ASCII
```
- JSON
```shell
gitcomp -u Rohitrajak1807 avaish1409 -t json
```
- CSV
```shell
gitcomp -u Rohitrajak1807 avaish1409 -t csv
```
- HTML Table
```shell
gitcomp -u Rohitrajak1807 avaish1409 -t html
```

## Specifying output file
```shell
gitcomp -u Rohitrajak1807 avaish1409 -t json -o res.json
```
```shell
gitcomp -u Rohitrajak1807 avaish1409 -t csv -o res.csv
```
```shell
gitcomp -u Rohitrajak1807 avaish1409 -t html -o res.html
```
```shell
gitcomp -u Rohitrajak1807 avaish1409 -o res.txt
```

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
