import re
from .user import User
from .repository import Repository
from typing import List, Dict
from .net_mod import NetMod


class GitComp:
    users: List[str]
    repos: List[str]
    user_data: Dict[str, User] = None
    repo_data: Dict[str, Repository] = None
    __username_regex = r'^[a-zA-Z0-9]+'
    __repo_regex = r'^[A-Za-z0-9]+/[A-Za-z0-9]+'

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
        self.__validate_user_names()
        response = NetMod().fetch_users_data(self.users)
        for user in response:
            self.user_data[user] = User(response[user])

    def __validate_user_names(self):
        for user in self.users:
            if not re.match(GitComp.__username_regex, user):
                raise ValueError(f"""
                Improper username {user} 
                """)

    def __fetch_repo_data(self):
        self.__validate_repo_string()
        response = NetMod().fetch_repos_data(self.repos)
        for repo in response:
            self.repo_data[repo] = Repository(response[repo])

    def __validate_repo_string(self):
        for repo in self.repos:
            if not re.match(GitComp.__repo_regex, repo):
                raise ValueError("""
                Improper repository format.
                Provide the repository name as: <user-name>/<repository-name>
                """)
