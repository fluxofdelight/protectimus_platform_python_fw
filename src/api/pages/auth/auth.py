from typing import Optional

import allure
from requests import Session

from src.api.pages.base_api import BaseAPI
from src.configs.config import Config


class Auth(BaseAPI):
    def __init__(self, session: Optional[Session], config):
        self.session = session or Session()
        self.config = config or Config().api
        super().__init__(self.session, self.config)

    @allure.step("Send a POST request to /api/request")
    def login(self, email, password, request_body=None, expected_code=200):
        data = request_body if request_body else {"login": email, "password": password}
        response = self.make_request(
            self.endpoints.auth.login, self.requests_type.POST, json=data, expected_code=expected_code, token=False
        )
        return response

    @allure.step("Send a GET request to /api/request")
    def auth_me(self, expected_code=200):
        response = self.make_request(self.endpoints.auth.auth_me, self.requests_type.GET, expected_code=expected_code)
        return response

    @allure.step("Send an API request to /api/request")
    def assign(self, payload, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.auth.assign,
            request_type or self.requests_type.POST,
            json=payload,
            expected_code=expected_code
        )
        return response

    @allure.step("Send an API request to /api/request")
    def revoke(self, payload, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.auth.revoke,
            request_type or self.requests_type.POST,
            json=payload,
            expected_code=expected_code
        )
        return response


if __name__ == "__main__":
    api = Auth(None, None)
    t = api.assign({"userId": 2, "tokenId": 5})
    import pprint; pprint.pp(t)  # noqa: E702
