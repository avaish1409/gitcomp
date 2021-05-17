import argparse
import json
import re
import logging
import urllib.request
from user import User
from repository import Repository


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
    user_data: {str: User}
    repo_data: {str: Repository}
    __username_regex = r'^[a-zA-Z0-9]+'
    __repo_regex = r'^[A-Za-z0-9]+/[A-Za-z0-9]+'

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
        self.__validate_user_names()
        api_route = 'users/'
        for user in self.users:
            req = urllib.request.Request(url=f'{self.api_base}{api_route}{user}', headers=GitCompare.headers)
            self.user_data[user] = User(GitCompare.__make_request(request=req))

    def __validate_user_names(self):
        for user in self.users:
            if not re.match(GitCompare.__username_regex, user):
                raise ValueError(f"""
                Improper username {user} 
                """)

    def __fetch_repo_data(self):
        api_route = 'repos/'
        self.__validate_repo_string()
        for repo in self.repos:
            req = urllib.request.Request(url=f'{self.api_base}{api_route}{repo}', headers=GitCompare.headers)
            self.repo_data[repo] = Repository(GitCompare.__make_request(request=req))

    def __validate_repo_string(self):
        for repo in self.repos:
            if not re.match(GitCompare.__repo_regex, repo):
                raise ValueError("""
                Improper repository format.
                Provide the repository name as: <user-name>/<repository-name>
                """)

    @staticmethod
    def __make_request(request: urllib.request.Request):
        with urllib.request.urlopen(request) as req:
            data = json.loads(req.read().decode())
            return data

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
                                     Multiple usernames can be queried at a time by providing a space separated argument
                                      list.
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
