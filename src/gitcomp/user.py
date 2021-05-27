from dataclasses import dataclass
import sys


@dataclass(repr=True)
class User:
    login: str
    followers: int
    following: int
    site_admin: bool
    name: str
    company: str
    blog: str
    location: str
    public_repos: int
    public_gists: int
    git_score: int
    display_rows = ['login', 'followers', 'following', 'site_admin', 'name', 'company', 'blog', 'location',
                    'public_repos', 'public_gists', 'git_score']
    __total_weight = 100 / 16

    def __init__(self, user_data: dict):
        """
        setup a user object containing a user's vital stats, equivalent to using the CLI tool with the -u flag
        :param user_data: the json dictionary we get from calling the GitHub API
        """
        self.login = user_data['login']
        self.followers = user_data['followers']
        self.following = user_data['following']
        self.site_admin = user_data['site_admin']
        self.name = user_data['name']
        self.company = user_data['company']
        self.blog = user_data['blog']
        self.location = user_data['location']
        self.public_repos = user_data['public_repos']
        self.public_gists = user_data['public_gists']
        self.num_organizations = len(user_data['organizations_url'])
        # self.features = []
        self.git_score = self.get_score()

    def feature_score(self, name, val, weight=1, metric={}):
        fscore = 0
        for i in metric:
            if val <= i:
                fscore = metric[i]
                break
        return weight * fscore

    def get_score(self):
        score = 0
        score += self.feature_score('num_followers', self.followers, 1, {10: 1, 25: 2, 50: 3, sys.maxsize: 4})
        # todo-> contrib/ time
        score += self.feature_score('num_organizaitions', self.num_organizations, 1,
                                    {0: 1, 3: 2, 7: 4, 10: 3, sys.maxsize: 2})
        # todo-> repos: forked/org
        score += self.feature_score('num_gists', self.public_gists, 1, {0: 1, 4: 2, 10: 3, sys.maxsize: 4})
        # todo-> stars given
        # todo-> stars recieved
        try:
            score += self.feature_score('follow_ratio', self.followers / self.following, 1,
                                        {0.99: 1, 1: 2, 2: 3, sys.maxsize: 4})
        except ZeroDivisionError:
            pass
        return int(score * User.__total_weight)
