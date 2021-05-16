import argparse
import json
import re
import logging
import urllib.request
from user import User


class GitCompare:
    api_base = 'https://api.github.com/'
    """
    explicitly request v3 of the API
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api#current-version
    """
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    logger: logging.Logger
    arg_parser: argparse.ArgumentParser
    users: [str]
    repos: [str]
    user_data: dict
    repo_data: dict
    username_regex = '^[a-zA-Z]+'
    repo_regex = '^[a-zA-Z]+/^[a-zA-Z]+'

    def __init__(self, users=None, repos=None):
        self.__init_logger()
        self.__init_arg_parser()
        self.users = users
        self.repos = repos
        self.user_data = {}
        if self.users is not None:
            self.user_data = {}
            self.__fetch_user_data()
        if self.repos is not None:
            self.repo_data = {}
            self.__fetch_repo_data()

    def __fetch_user_data(self):
        api_route = 'users/'
        self.__validate_user_names()
        for user in self.users:
            with urllib.request.urlopen(f'{self.api_base}{api_route}{user}') as url:
                self.user_data[user] = User(json.loads(url.read().decode()))

    def __validate_user_names(self):
        for user in self.users:
            if not re.match(GitCompare.username_regex, user):
                raise ValueError(f"""
                Improper username {user} 
                """)

    def __fetch_repo_data(self):
        api_route = 'repos/'
        self.__validate_repo_string()

    def __validate_repo_string(self):
        for repo in self.repos:
            if not re.match(GitCompare.repo_regex, repo):
                raise ValueError("""
                Improper repository format.
                Provide the repository name as: <user-name>/<repository-name>
                """)

    def __init_logger(self):
        """
        initializes a logger instance with some defaults
        :return: None
        """
        logging.basicConfig(filename='newfile.log', format='%(asctime)s %(message)s', filemode='w')
        self.logger = logging.getLogger()

    def __init_arg_parser(self):
        """
        initializes an arg_parser with
        --user/-u
        --repo/-r
        --type/-o
        flags
        :return: None
        """
        self.arg_parser = argparse.ArgumentParser(description='''
        gitcompare
        A CLI utility to compare the vital stats of GitHub repositories
        ''')

        self.arg_parser.add_argument('-u', '--user', type=str, nargs='+',
                                     metavar='user_name', default=None, dest='user_names',
                                     help='''
                                     -u, --user <username...>
                                     The GitHub username(s) to query against.
                                     Multiple usernames can be queried at a time by providing a space separated argument list.
                                     ''')

        self.arg_parser.add_argument('-r', '--repo', type=str, nargs='+',
                                     metavar='repo', default=None, dest='repo_names',
                                     help='''
                                     -r, --repo <repo>
                                     The public GitHub repository to query against where repo takes the form:
                                     <user/repo>
                                     Example: -r octocat/Spoon-Knife
                                     ''')

        self.arg_parser.add_argument('-t', '--type', type=str, nargs=1,
                                     metavar='output_dest', default=['cmd'], dest='out_type',
                                     help='''
                                     -t, --type <type>
                                     Default: cmd
                                     Choose the format of output. All output is dumped to STDOUT
                                     The types available are:
                                     cmd: Show the result as an ASCII table
                                     csv: Format the output to csv
                                     html: Show output as html
                                     json: Show the result as JSON
                                     ''')

        self.arg_parser.add_argument('-o', '--output', type=str, nargs=1, metavar='output_file',
                                     help='''
                                     -o, --output <file>
                                     Write the output to a file instead of STDOUT
                                     '''
                                     )
