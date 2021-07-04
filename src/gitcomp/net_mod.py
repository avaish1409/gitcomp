from urllib3.connectionpool import HTTPSConnectionPool, HTTPResponse
from typing import Dict


class NetMod:
    _instance = None
    _pool: HTTPSConnectionPool
    __pool_size: int = 5
    __api_base: str = 'api.github.com'
    __port: int = 443
    __timeout: float = 5.0

    """
    explicitly request v3 of the API
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api#current-version
    """
    __headers: Dict[str, str] = {
        'Accept': 'application/vnd.github.v3+json'
    }
    """
    referenced from
    https://python-patterns.guide/gang-of-four/singleton/
    """

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._pool = HTTPSConnectionPool(host=NetMod.__api_base, maxsize=NetMod.__pool_size, headers=NetMod.__headers,
                                         timeout=NetMod.__timeout, port=NetMod.__port)

    def make_request(self, method: str, api_route: str) -> HTTPResponse:
        return self._pool.request(method, api_route)
