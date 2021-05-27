import json
import re
import urllib.request
from .user import User
from .repository import Repository
from typing import List, Dict


class GitComp:
    __api_base: str = 'https://api.github.com/'
    """
    explicitly request v3 of the API
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api#current-version
    """
    __headers: Dict[str, str] = {
        'Accept': 'application/vnd.github.v3+json'
    }
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
        api_route = 'users/'
        for user in self.users:
            req = urllib.request.Request(url=f'{self.__api_base}{api_route}{user}', headers=GitComp.__headers)
            self.user_data[user] = User(GitComp.__make_request(request=req))

    def __validate_user_names(self):
        for user in self.users:
            if not re.match(GitComp.__username_regex, user):
                raise ValueError(f"""
                Improper username {user} 
                """)

    def __fetch_repo_data(self):
        api_route = 'repos/'
        self.__validate_repo_string()
        for repo in self.repos:
            req = urllib.request.Request(url=f'{self.__api_base}{api_route}{repo}', headers=GitComp.__headers)
            self.repo_data[repo] = Repository(GitComp.__make_request(request=req))

    def __validate_repo_string(self):
        for repo in self.repos:
            if not re.match(GitComp.__repo_regex, repo):
                raise ValueError("""
                Improper repository format.
                Provide the repository name as: <user-name>/<repository-name>
                """)

    @staticmethod
    def __make_request(request: urllib.request.Request):
        with urllib.request.urlopen(request) as req:
            data = json.loads(req.read().decode())
            return data
