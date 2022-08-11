import requests
from requests import JSONDecodeError


class ApiAdapter:
    session = requests.session()

    def __int__(self, logger=None):
        self.logger = logger

    @classmethod
    def make_request(cls, method, url, passed_params=None, passed_headers=None):
        req = cls.session.request(method, url, params=passed_params, headers=passed_headers)
        if req.status_code == 200:
            try:
                return req.json()
            except JSONDecodeError:
                return None
        else:
            cls.logger.error(f"Failed to get url {url}")
            return None
