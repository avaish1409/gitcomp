import json
import re
import urllib.request
from user import User
from repository import Repository
from typing import List, Dict
from prettytable import PrettyTable, ALL


class GitCompare:
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
    display_type: str

    def __init__(self, users: List[str] = None, repos: List[str] = None, display_type: str = 'cmd'):
        self.users = users
        self.repos = repos
        self.display_type = display_type
        self.user_data = {}
        if self.users is not None:
            self.user_data = {}
            self.__fetch_user_data()
            self.table = self.create_user_table()
        if self.repos is not None:
            self.repo_data = {}
            self.__fetch_repo_data()
            self.table = self.create_repo_table()

    def __fetch_user_data(self):
        self.__validate_user_names()
        api_route = 'users/'
        for user in self.users:
            req = urllib.request.Request(url=f'{self.__api_base}{api_route}{user}', headers=GitCompare.__headers)
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
            req = urllib.request.Request(url=f'{self.__api_base}{api_route}{repo}', headers=GitCompare.__headers)
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

    def create_repo_table(self):
        rows = []
        for attr in Repository.display_rows:
            row = [len(rows), attr]
            for repo in self.repo_data.values():
                row.append(repo.__dict__[attr])
            rows.append(row)

        x = PrettyTable()
        x.field_names = ["S.No.", "Arg"] + self.repos
        x.add_rows(rows)
        x.sortby = None
        x.hrules = ALL
        return self.get_result(x)

    def create_user_table(self):
        rows = []
        for attr in User.display_rows:
            row = [len(rows), attr]
            for user in self.user_data.values():
                row.append(user.__dict__[attr])
            rows.append(row)

        x = PrettyTable()
        x.field_names = ["S.No.", "Arg"] + self.users
        x.add_rows(rows)
        x.sortby = None
        x.hrules = ALL
        return self.get_result(x)

    def get_result(self, x):
        if self.display_type == 'cmd':
            return x.get_string()
        elif self.display_type == 'csv':
            return x.get_csv_string()
        elif self.display_type == 'html':
            return x.get_html_string()
        elif self.display_type == 'json':
            return x.get_json_string()
        return

    def get_table(self):
        try:
            return self.table
        except:
            pass
