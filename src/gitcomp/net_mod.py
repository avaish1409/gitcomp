import json
from urllib3.connectionpool import HTTPSConnectionPool, HTTPResponse
from typing import Dict, List, Any
from string import Template


class NetMod:
    _instance = None
    _pool: HTTPSConnectionPool
    __pool_size: int = 5
    __api_base: str = 'api.github.com'
    __port: int = 443
    __timeout: float = 5.0
    __repo_route: Template = Template('/repos/$repo')
    __user_route: Template = Template('/users/$user')
    __org_route: Template = Template('/users/$user/orgs')

    """
    explicitly request v3 of the API
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api#current-version
    """
    __headers: Dict[str, str] = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Python-urllib/3'
    }
    """
    referenced from
    https://python-patterns.guide/gang-of-four/singleton/
    """

    """
    "html_url": "https://github.com/Rohitrajak1807",
    "followers_url": "https://api.github.com/users/Rohitrajak1807/followers",
    "following_url": "https://api.github.com/users/Rohitrajak1807/following{/other_user}",
    "gists_url": "https://api.github.com/users/Rohitrajak1807/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/Rohitrajak1807/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/Rohitrajak1807/subscriptions",
    "organizations_url": "https://api.github.com/users/Rohitrajak1807/orgs",
    "repos_url": "https://api.github.com/users/Rohitrajak1807/repos",
    "events_url": "https://api.github.com/users/Rohitrajak1807/events{/privacy}",
    "received_events_url": "https://api.github.com/users/Rohitrajak1807/received_events",
    
    
    "url": "https://api.github.com/users/Rohitrajak1807",
    "html_url": "https://github.com/Rohitrajak1807",
    "followers_url": "https://api.github.com/users/Rohitrajak1807/followers",
    "following_url": "https://api.github.com/users/Rohitrajak1807/following{/other_user}",
    "gists_url": "https://api.github.com/users/Rohitrajak1807/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/Rohitrajak1807/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/Rohitrajak1807/subscriptions",
    "organizations_url": "https://api.github.com/users/Rohitrajak1807/orgs",
    "repos_url": "https://api.github.com/users/Rohitrajak1807/repos",
    "events_url": "https://api.github.com/users/Rohitrajak1807/events{/privacy}",
    "received_events_url": "https://api.github.com/users/Rohitrajak1807/received_events",
    
    "html_url": "https://github.com/Rohitrajak1807/algorithms",
    "url": "https://api.github.com/repos/Rohitrajak1807/algorithms",
    "forks_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/forks",
    "keys_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/teams",
    "hooks_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/hooks",
    "issue_events_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/issues/events{/number}",
    "events_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/events",
    "assignees_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/assignees{/user}",
    "branches_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/branches{/branch}",
    "tags_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/tags",
    "blobs_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/languages",
    "stargazers_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/stargazers",
    "contributors_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/contributors",
    "subscribers_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/subscribers",
    "subscription_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/subscription",
    "commits_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/contents/{+path}",
    "compare_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/merges",
    "archive_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/downloads",
    "issues_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/issues{/number}",
    "pulls_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/labels{/name}",
    "releases_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/releases{/id}",
    "deployments_url": "https://api.github.com/repos/Rohitrajak1807/algorithms/deployments",
    "git_url": "git://github.com/Rohitrajak1807/algorithms.git",
    "ssh_url": "git@github.com:Rohitrajak1807/algorithms.git",
    "clone_url": "https://github.com/Rohitrajak1807/algorithms.git",
    "svn_url": "https://github.com/Rohitrajak1807/algorithms",
    """

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NetMod, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._pool = HTTPSConnectionPool(host=NetMod.__api_base, maxsize=NetMod.__pool_size, headers=NetMod.__headers,
                                         timeout=NetMod.__timeout, port=NetMod.__port, block=True)

    def __make_request(self, api_route: str, method: str = 'get') -> HTTPResponse:
        return self._pool.request(method, api_route)

    def fetch_repos_data(self, repos: List[str]) -> Dict[str, Any]:
        results = {}
        for repo in repos:
            api_route = self.__repo_route.substitute(repo=repo)
            results[repo] = self.__fetch_one_and_decode(api_route)
        return results

    def fetch_users_data(self, users: List[str]) -> Dict[str, Any]:
        results = {}
        for user in users:
            api_route = self.__user_route.substitute(user=user)
            results[user] = self.__fetch_one_and_decode(api_route)
        return results

    def fetch_org_data(self, user: str) -> Dict[str, Any]:
        api_route = self.__org_route.substitute(user=user)
        return self.__fetch_one_and_decode(api_route)

    def __fetch_one_and_decode(self, api_route: str) -> Dict[str, Any]:
        res = self.__make_request(api_route)
        return json.loads(res.data)
