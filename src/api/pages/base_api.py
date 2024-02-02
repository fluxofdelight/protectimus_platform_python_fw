import allure
from loguru import logger as log
from requests import Session

from src.api.endpoints.api_endpoints import ApiEndpoints
from src.api.pages.mailhog import Mailhog
from src.common.api_utils import APIUtils
from src.common.enum_common.http_errors import HttpErrors
from src.common.enum_common.http_request_type import HttpRequestType
from src.common.enum_common.token_type import TokenType
from src.configs.config import Config


class BaseAPI:
    def __init__(self, session: Session, config):
        self.session = session or Session()
        self.config = config or Config().api
        self.endpoints = ApiEndpoints(config)
        self.requests_type = HttpRequestType
        self.token_type = TokenType
        self.mailhog = Mailhog(self.session, Config().mailhog)
        self.api_utils = APIUtils()
        self.http_errors = HttpErrors()

    def get_access_token(self, expected_code=200):
        data = {"login": self.config.api_login, "password": self.config.password}
        response = self.session.post(self.endpoints.auth.login, json=data)
        self.validate_http_status_code(response, self.endpoints.auth.login, expected_code)
        token = response.json()["accessToken"]
        return f"Bearer {token}"

    @allure.step("Make an API request")
    def make_request(
        self,
        url: str,
        request_type: str,
        data=None,
        json=None,
        file=None,
        headers=None,
        params=None,
        expected_code=200,
        token=True
    ):
        if token:
            token = self.get_access_token()
            auth_header = {"Authorization": token}
            if headers:
                headers = {**auth_header, **headers}
            else:
                headers = auth_header
        log.info(
            f">>>>> Request with type [{request_type}] will be sent to url - [{url}].\nProperties: data - {data},"
            f" json - {json}, file - {file}, params - {params}"
        )
        if request_type == "post":
            response = self.session.post(url, data=data, json=json, headers=headers, files=file, params=params)
        elif request_type == "patch":
            response = self.session.patch(url, data=data, json=json, headers=headers, files=file, params=params)
        elif request_type == "put":
            response = self.session.put(url, data=data, json=json, headers=headers, files=file, params=params)
        elif request_type == "get":
            response = self.session.get(url, data=data, json=json, headers=headers, files=file, params=params)
        elif request_type == "delete":
            response = self.session.delete(url, data=data, json=json, headers=headers, files=file, params=params)
        else:
            raise ValueError(f"Unsupported request with type - {request_type}. Please validate or update method")
        log.info(
            f"<<<<< Response received. HTTP status code - [{response.status_code}]. Response - \n[{response.content}]"
        )
        self.validate_http_status_code(response, url, expected_code)
        return response

    @staticmethod
    @allure.step("Validate actual and expected HTTP status code")
    def validate_http_status_code(response, url, expected_code: int = 200):
        if expected_code != response.status_code:
            if response.status_code == 500:
                raise ConnectionError(
                    f"Expected status code - {expected_code} != {response.status_code} - "
                    f"actual HTTP response code from endpoint {url}\nResponse content - {response.content}"
                )
            else:
                raise Exception(
                    f"Expected status code - {expected_code} != {response.status_code} - "
                    f"actual HTTP response code from endpoint {url}\nResponse content - {response.content}"
                )

    @allure.step("Validate actual and expected error responses")
    def validate_error_response(self, actual, expected):
        # Cut down the timestamp because of the difference in seconds
        actual["timestamp"] = actual["timestamp"][:-13]
        if actual["timestamp"] != expected["timestamp"]:
            expected["timestamp"] = expected["timestamp"][:-1] + str(int(expected["timestamp"][-1]) + 1)
            if actual["timestamp"] != expected["timestamp"]:
                raise Exception(f'Cannot validate timestamp. Actual: {actual["timestamp"]}. '
                                f'Expected: {expected["timestamp"]}\nExpected result have to be specified before the'
                                f'actual response in negative cases. Check the test for errors')
            else:
                assert actual == expected, "FAILED"
        else:
            assert actual == expected, "FAILED"
