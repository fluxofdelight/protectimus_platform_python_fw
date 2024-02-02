import allure
import pytest

from common.enum_common.http_request_type import HttpRequestType
from src.api.responses.base import ErrorResponse


@allure.suite("User blocking tests")
class TestBlockUser:
    @pytest.mark.regress
    def test_block_user(self, api, db):
        """
        Steps:
            1. Get a random user from the DB
            2. Send a POST request to /api/request/{user_id}/disable to block user
            3. Validate the response status
            4. Make sure user is blocked in the DB

        Expected result:
            1. User was successfully blocked
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        response = api.users.block_user(user_id)
        assert response.reason == "OK", "FAILED"
        db_response = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response["block"] == 1, f"FAILED. User wasn't blocked, DB response:\n{db_response}"

    @pytest.mark.regress
    def test_unblock_user(self, api, db):
        """
        Steps:
            1. Get a random user from the DB
            2. Send a POST request to /api/request/{user_id}/disable to block user
            3. Validate the response status
            4. Make sure user is blocked in the DB
            5. Send a POST request to /api/request/{user_id}/enable to unblock user
            6. Validate the response status
            7. Make sure user is unblocked in the DB

        Expected result:
            1. User was successfully unblocked
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        block_response = api.users.block_user(user_id)
        assert block_response.reason == "OK", "FAILED"
        db_response_block = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response_block["block"] == 1, f"FAILED. User wasn't blocked, DB response:\n{db_response_block}"
        response = api.users.unblock_user(user_id)
        assert response.reason == "OK", "FAILED"
        db_response = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response["block"] != db_response_block["block"], \
            f"FAILED. User wasn't unblocked, DB response:\n{db_response}"

    @pytest.mark.negative
    def test_block_blocked_user(self, api, db):
        """
        Steps:
            1. Get a random user from the DB
            2. Send a POST request to /api/request/{user_id}/disable to block user
            3. Validate the response status
            4. Make sure user is blocked in the DB
            5. Send a POST request to /api/request/{user_id}/disable to block user again
            6. Validate the response

        Expected result:
            1. Blocked user can be blocked again
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        response = api.users.block_user(user_id)
        assert response.reason == "OK", "FAILED"
        db_response = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response["block"] == 1, f"FAILED. User wasn't blocked, DB response:\n{db_response}"
        response = api.users.block_user(user_id)
        assert response.reason == "OK", "FAILED"

    @pytest.mark.negative
    def test_unblock_unblocked_user(self, api, db):
        """
        Steps:
            1. Get a random user from the DB
            2. Send a POST request to /api/request/{user_id}/enable to unblock user
            3. Validate the response status
            4. Make sure user is blocked in the DB
            5. Send a POST request to /api/request/{user_id}/enable to unblock user again
            6. Validate the error response

        Expected result:
            1. Unblocked user can be unblocked again
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        block_response = api.users.block_user(user_id)
        assert block_response.reason == "OK", "FAILED"
        db_response_block = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response_block["block"] == 1, f"FAILED. User wasn't blocked, DB response:\n{db_response_block}"
        unblock_response = api.users.unblock_user(user_id)
        assert unblock_response.reason == "OK", "FAILED"
        db_response_unblock = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response_unblock["block"] != db_response_block["block"], \
            f"FAILED. User wasn't unblocked, DB response:\n{db_response_unblock}"
        response = api.users.unblock_user(user_id)
        assert response.reason == "OK", "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [0, 99999999])
    def test_block_user_by_non_existing_id(self, api, db, user_id, expected_code=400):
        f"""
        Steps:
            1. Send a POST request to /api/request/{user_id}/disable with non-existing ID
            2. Validate error response

        Expected result:
            1. Returns the correct error response
        """
        endpoint = api.users.endpoints.users.block
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.block_user(user_id, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "request_type",
        [
            HttpRequestType.DELETE,
            HttpRequestType.PUT,
            HttpRequestType.PATCH,
            HttpRequestType.GET
        ]
    )
    def test_unblock_user_with_unsupported_request_type(
        self,
        api,
        db,
        request_type,
        expected_code=405
    ):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request/<user_id>/enable
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.users.unblock
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.unblock_user(user_id, expected_code=expected_code, request_type=request_type).json()
        api.users.validate_error_response(response, expected_response)
