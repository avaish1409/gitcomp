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
    open_issues: int
    network_count: int
    subscribers_count: int
    git_score: int
    license: str = None
    display_rows = ['full_name', 'forks', 'open_issues', 'watches', 'network_count', 'subscribers_count', 'git_score']
    __date_fmt = '%Y-%m-%dT%H:%M:%SZ'
    __total_weight = 100 / 16

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
        self.open_issues = repo_data['open_issues']
        self.network_count = repo_data['network_count']
        self.subscribers_count = repo_data['subscribers_count']
        if repo_data['license'] is not None:
            self.license = repo_data['license']['name']
        self.git_score = self.get_score()

    def feature_score(self, name, val, weight=1, metric={}):
        """
            calculate score based upon val as compared to metric 
            Metric caonains max bounds for each value range and corresponing score
        """
        fscore = 0
        for i in metric:
            if val <= i:
                fscore = metric[i]
                break
        return weight * fscore

    def get_score(self):
        score = 0
        score += self.feature_score('is_forked', self.forked, 1, {False: 4, True: 1})
        score += self.feature_score('num_forks', self.forks, 1, {0: 1, 3: 2, 10: 3, sys.maxsize: 4})
        score += self.feature_score('stars', self.stars, 1, {0: 1, 3: 2, 10: 3, sys.maxsize: 4})
        score += self.feature_score('watchers', self.watches, 1, {0: 1, 3: 2, 10: 3, sys.maxsize: 4})
        return int(score * Repository.__total_weight)
