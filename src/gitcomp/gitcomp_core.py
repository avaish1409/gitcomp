import re
import sys

from .user import User
from .repository import Repository
from typing import List, Dict, Pattern
from .net_mod import NetMod


class GitComp:
    users: List[str]
    repos: List[str]
    user_data: Dict[str, User] = None
    repo_data: Dict[str, Repository] = None
    # GitHub usernames can be alpha numerical characters with at-most 1 - except in the beginning and the end
    # https://regex101.com/r/sYIEPE/2
    __username_regex: Pattern = re.compile(r'^([A-Za-z0-9])([A-Za-z0-9]*)(-)?([A-Za-z0-9]*)([A-Za-z0-9]$)')
    # Repository names are currently limited to 100 characters, some special names like . are reserved
    __repo_regex: Pattern = re.compile(
        r'^([A-Za-z0-9])([A-Za-z0-9]*)(-)?([A-Za-z0-9]*)([A-Za-z0-9])(/)((?=[^.])([^!#@%^&+=()]*)$|((\.{3,})(['
        r'^!#@%^&+=()]+)$))')

    def __init__(self, users: List[str] = None, repos: List[str] = None):
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
        try:
            self.__validate_user_names()
        except ValueError as e:
            sys.exit(e)
        response = NetMod().fetch_users_data(self.users)
        for user in response:
            self.user_data[user] = User(response[user])

    def __validate_user_names(self):
        for user in self.users:
            if not GitComp.__username_regex.fullmatch(user) is None:
                raise ValueError(f"""
                Improper username {user} 
                """)

    def __fetch_repo_data(self):
        try:
            self.__validate_repo_string()
        except ValueError as e:
            sys.exit(e)

        response = NetMod().fetch_repos_data(self.repos)
        for repo in response:
            self.repo_data[repo] = Repository(response[repo])

    def __validate_repo_string(self):
        for repo in self.repos:
            if not GitComp.__repo_regex.fullmatch(repo):
                print(re.match(GitComp.__repo_regex, repo))
                raise ValueError("""
                Improper repository format.
                Provide the repository name as: <user-name>/<repository-name>
                """)
