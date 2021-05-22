from datetime import datetime
from dataclasses import dataclass
import sys


@dataclass(repr=True)
class Repository:
    name: str
    full_name: str
    private: bool
    web_url: str
    description: str
    forked: str
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    clone_url: str
    stars: int
    watches: int
    language: str
    forks: int
    archived: bool
    owner: str
    license: str = None
    __date_fmt = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, repo_data: dict):
        self.name = repo_data['name']
        self.full_name = repo_data['full_name']
        self.private = repo_data['private']
        self.web_url = repo_data['html_url']
        self.description = repo_data['description']
        self.forked = repo_data['fork']
        self.created_at = datetime.strptime(repo_data['created_at'], Repository.__date_fmt)
        self.updated_at = datetime.strptime(repo_data['updated_at'], Repository.__date_fmt)
        self.pushed_at = datetime.strptime(repo_data['pushed_at'], Repository.__date_fmt)
        self.clone_url = repo_data['clone_url']
        self.stars = repo_data['stargazers_count']
        self.watches = repo_data['watchers_count']
        self.language = repo_data['language']
        self.forks = repo_data['forks_count']
        self.archived = repo_data['archived']
        self.owner = repo_data['owner']['login']
        self.license = ''
        if repo_data['license'] is not None:
            self.license = repo_data['license']['name']
        self.score = self.getScore()
        print(self.name, self.score)


    def featureScore(self, name, val, weight=1, metric={}):
        fscore = 0
        for i in metric:
            if val<=i:
                fscore = metric[i]
                break
        return weight*fscore

    def getScore(self):
        score=0
        score += self.featureScore('is_forked', self.forked, 1, {False: 4, True: 1})
        score += self.featureScore('num_forks', self.forks, 1, {0: 1, 3: 2, 10: 3, sys.maxsize: 4})
        score += self.featureScore('stars', self.stars, 1, {0: 1, 3: 2, 10: 3, sys.maxsize: 4})
        score += self.featureScore('watchers', self.watches, 1, {0: 1, 3: 2, 10: 3, sys.maxsize: 4})
        return (score*100)//16
