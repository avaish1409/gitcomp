import json
from concurrent.futures import ThreadPoolExecutor, Future
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
        'User-Agent': 'Python-urllib/3',
        'Authorization': ''
    }

    """
    referenced from
    https://python-patterns.guide/gang-of-four/singleton/
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
        api_routes = [self.__user_route.substitute(repo=repo) for repo in repos]
        return self.__fetch_all__concurrent(repos, api_routes)

    def fetch_users_data(self, users: List[str]) -> Dict[str, Any]:
        api_routes = [self.__user_route.substitute(user=user) for user in users]
        return self.__fetch_all__concurrent(users, api_routes)

    def fetch_org_data(self, user: str) -> Dict[str, Any]:
        api_route = self.__org_route.substitute(user=user)
        return self.__fetch_one_and_decode(api_route)

    def __fetch_all__concurrent(self, entries: List[str], api_routes: List[str]) -> Dict[str, Any]:
        max_workers = max(len(entries), self.__pool_size)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            res: Dict[str, Future[Dict[str, Any]]] = {entry: executor.submit(self.__fetch_one_and_decode, route) for
                                                      entry, route in
                                                      zip(entries, api_routes)}
        return {user: data.result() for user, data in res.items()}

    def __fetch_one_and_decode(self, api_route: str) -> Dict[str, Any]:
        res = self.__make_request(api_route)
        return json.loads(res.data)
