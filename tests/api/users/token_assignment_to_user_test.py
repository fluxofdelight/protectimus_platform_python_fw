import allure
import pytest

from common.enum_common.http_request_type import HttpRequestType
from src.api.responses.base import ErrorResponse


@allure.suite("Assignment of token to the user tests")
class TestTokenAssignmentToUser:
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_assign_token_to_user(self, api, db):
        """
        Steps:
            1. Get a random user from the DB
            2. Get a random token not assigned to any user from the DB
            3. Send a POST request to /api/request/assign to assign token to the user
            4. Validate the response status
            5. Make sure the token was assigned to the user in the DB

        Expected result:
            1. Token was successfully assigned to the user
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        token_id = db.tokens.get_random_token_not_assigned_to_user(json_output=True)[0]["id"]
        response = api.users.assign_token(user_id, token_id)
        assert response.reason == "OK", "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(token_id, json_output=True)[0]
        assert db_response["user_id"] == user_id, f"FAILED. Token wasn't assigned, DB response:\n{db_response}"

    @pytest.mark.negative
    def test_assign_assigned_token_to_user(self, api, db, expected_code=400):
        """
        Steps:
            1. Get a random user from the DB
            2. Get a random token assigned to a user from the DB
            3. Send a POST request to /api/request/assign to assign token to the user
            4. Validate the error response
            5. Make sure the token wasn't assigned to the user in the DB

        Expected result:
            1. Token cannot be assigned to the user, if it is already assigned
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        token_id = db.tokens.get_random_token_assigned_to_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.auth.assign
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.assign_token(user_id, token_id, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)
        db_response = db.tokens.get_all_token_info_by_id(token_id, json_output=True)[0]
        assert db_response["user_id"] != user_id, f"FAILED. Token wasn't assigned, DB response:\n{db_response}"

    @pytest.mark.negative
    @pytest.mark.parametrize("token_id", [0, 99999999])
    def test_assign_non_existing_token_to_user(self, api, db, token_id, expected_code=400):
        """
        Steps:
            1. Get a random user from the DB
            2. Send a POST request to /api/request/assign to assign non-existing token to the user
            3. Validate the error response

        Expected result:
            1. Returns the correct error response
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.auth.assign
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.assign_token(user_id, token_id, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [0, 99999999])
    def test_assign_token_to_non_existing_user(self, api, db, user_id, expected_code=400):
        """
        Steps:
            1. Get a random token from the DB
            2. Send a POST request to /api/request/assign to assign token to non-existing user
            3. Validate the error response

        Expected result:
            1. Returns the correct error response
        """
        token_id = db.tokens.get_random_token_not_assigned_to_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.auth.assign
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.assign_token(user_id, token_id, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.negative
    def test_assign_same_token_to_user(self, api, db, expected_code=400):
        """
        Steps:
            1. Get a random token assigned to a user from the DB
            2. Send a POST request to /api/request/assign to assign token to the user it is assigned
            3. Validate the error response

        Expected result:
            1. Same token cannot be assigned to the user that it is already assigned
        """
        token_data = db.tokens.get_random_token_assigned_to_user(json_output=True)[0]
        token_id = token_data["id"]
        user_id = token_data["user_id"]
        endpoint = api.users.endpoints.auth.assign
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.assign_token(user_id, token_id, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "request_type",
        [
            HttpRequestType.GET,
            HttpRequestType.DELETE,
            HttpRequestType.PATCH,
            HttpRequestType.PUT
        ]
    )
    def test_assign_token_to_user_with_unsupported_request_type(
        self,
        api,
        db,
        request_type,
        expected_code=405
    ):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request/assign
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        token_id = db.tokens.get_random_token_not_assigned_to_user(json_output=True)[0]["id"]
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.auth.assign
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.assign_token(
            user_id, token_id, expected_code=expected_code, request_type=request_type
        ).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.regress
    @pytest.mark.smoke
    def test_revoke_token_from_user(self, api, db):
        """
        Steps:
            1. Get a random token assigned to user from the DB
            2. Send a POST request to /api/request/revoke to revoke token from the user
            3. Validate the response status
            4. Make sure the token was revoked from the user in the DB

        Expected result:
            1. Token was successfully revoked from the user
        """
        token_data = db.tokens.get_random_token_assigned_to_user(json_output=True)[0]
        token_id = token_data["id"]
        user_id = token_data["user_id"]
        response = api.users.revoke_token(user_id, token_id)
        assert response.reason == "OK", "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(token_id, json_output=True)[0]
        assert db_response["user_id"] is None, f"FAILED. Token wasn't revoked, DB response:\n{db_response}"

    @pytest.mark.negative
    def test_revoke_revoked_token_from_user(self, api, db, expected_code=400):
        """
        Steps:
            1. Get a random token assigned to user from the DB
            2. Send a POST request to /api/request/revoke to revoke token from the user
            3. Validate the response status
            4. Make sure the token was revoked from the user in the DB
            5. Send a POST request to /api/request/revoke to revoke token from the user again
            6. Validate the error response

        Expected result:
            1. Token cannot be revoked from the user, if it is already revoked
        """
        token_data = db.tokens.get_random_token_assigned_to_user(json_output=True)[0]
        token_id = token_data["id"]
        user_id = token_data["user_id"]
        response = api.users.revoke_token(user_id, token_id)
        assert response.reason == "OK", "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(token_id, json_output=True)[0]
        assert db_response["user_id"] is None, f"FAILED. Token wasn't revoked, DB response:\n{db_response}"
        endpoint = api.users.endpoints.auth.revoke
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.revoke_token(user_id, token_id, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "request_type",
        [
            HttpRequestType.GET,
            HttpRequestType.DELETE,
            HttpRequestType.PATCH,
            HttpRequestType.PUT
        ]
    )
    def test_revoke_token_to_user_with_unsupported_request_type(
        self,
        api,
        db,
        request_type,
        expected_code=405
    ):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request/revoke
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        token_id = db.tokens.get_random_token_not_assigned_to_user(json_output=True)[0]["id"]
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.auth.revoke
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.revoke_token(
            user_id, token_id, expected_code=expected_code, request_type=request_type
        ).json()
        api.users.validate_error_response(response, expected_response)
