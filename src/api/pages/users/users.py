from typing import Optional

import allure
from requests import Session

from src.api.pages.auth.auth import Auth
from src.api.pages.base_api import BaseAPI
from src.common import string_utils as s
from src.configs.config import Config


class Users(BaseAPI):
    def __init__(self, session: Optional[Session], config):
        self.session = session or Session()
        self.config = config or Config().api
        self.auth = Auth(self.session, self.config)
        super().__init__(self.session, self.config)

    @allure.step("Send an API request to /api/request")
    def get_users(self, response_size=1000, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.users.default,
            request_type or self.requests_type.GET,
            params=f"size={response_size}",
            expected_code=expected_code
        )
        return response

    @allure.step("Send an API request to /api/request")
    def get_users_quantity(self, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.users.count_total, request_type or self.requests_type.GET, expected_code=expected_code
        )
        return response

    @allure.step("Send a API request to /api/request")
    def get_user_by_id(self, user_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.users.by_id.format(user_id=user_id),
            request_type or self.requests_type.GET,
            expected_code=expected_code
        )
        return response

    @allure.step("Send a POST request to /api/request to create a user")
    def add_user(
        self,
        login=("user_" + s.random_name()),
        first_name="John",
        last_name="Doe",
        alias=None,
        email=None,
        phone_number=None,
        password=None,
        block=None,
        block_time=None,
        request_body=None,
        expected_code=200,
    ):
        data = (
            request_body
            if request_body
            else {
                "login": login,
                "firstName": first_name,
                "secondName": last_name,
                "alias": alias,
                "email": email,
                "phoneNumber": phone_number,
                "password": password,
                "block": block,
                "blockTime": block_time,
                "type": "CLIENT_USER",
            }
        )
        response = self.make_request(
            self.endpoints.users.default, self.requests_type.POST, json=data, expected_code=expected_code
        )
        return response

    @allure.step("Send a PUT request to /api/request to edit the user")
    def edit_user(
        self,
        user_id,
        login="",
        first_name="",
        last_name="",
        alias="",
        email="",
        phone_number="",
        password="",
        block="",
        block_time="",
        request_body=None,
        expected_code=200,
        negative=False
    ):
        data = self.get_user_by_id(user_id).json()
        if negative and request_body:
            data = request_body
        elif request_body:
            data = {**data, **request_body}
        else:
            fields = {
                "login": login,
                "firstName": first_name,
                "secondName": last_name,
                "alias": alias,
                "email": email,
                "phoneNumber": phone_number,
                "password": password,
                "block": block,
                "blockTime": block_time,
            }
            data.update({field: value for field, value in fields.items() if value or value is None})
        response = self.make_request(
            self.endpoints.users.by_id.format(user_id=user_id),
            self.requests_type.PUT,
            json=data,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send a DELETE request to /api/request")
    def delete_user(self, user_id, expected_code=200):
        response = self.make_request(
            self.endpoints.users.by_id.format(user_id=user_id),
            self.requests_type.DELETE,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send a API request to /api/request")
    def block_user(self, user_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.users.block.format(user_id=user_id),
            request_type or self.requests_type.POST,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send a API request to /api/request")
    def unblock_user(self, user_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.users.unblock.format(user_id=user_id),
            request_type or self.requests_type.POST,
            expected_code=expected_code,
        )
        return response

    def assign_token(self, user_id, token_id, request_body=None, expected_code=200, request_type=None):
        data = request_body if request_body else {"userId": user_id, "tokenId": token_id}
        response = self.auth.assign(data, expected_code, request_type)
        return response

    def revoke_token(self, user_id, token_id, request_body=None, expected_code=200, request_type=None):
        data = request_body if request_body else {"userId": user_id, "tokenId": token_id}
        response = self.auth.revoke(data, expected_code, request_type)
        return response
