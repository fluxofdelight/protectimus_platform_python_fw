import allure
import pytest

from common.enum_common.http_request_type import HttpRequestType
from src.api.responses.base import ErrorResponse
from src.api.responses.users.users import SuccessUser


@allure.suite("Get users tests")
class TestGetUsers:
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_get_all_users_and_verify_quantity(self, api, db):
        """
        Steps:
            1. Send a GET request to /api/request to get all users
            2. Get quantity of users from the DB
            3. Make sure that quantity is the same both in API and DB responses

        Expected result:
            1. Get all users API request returns all users
        """
        response = api.users.get_users().json()
        users_num_db = db.users.get_number_of_users()
        assert len(response) == int(users_num_db), f"FAILED\nExpected quantity: {users_num_db}. Actual: {len(response)}"

    def test_verify_users_quantity(self, api, db):
        """
        Steps:
            1. Send a GET request to /api/request/count to get users quantity
            2. Get quantity of users from the DB
            3. Make sure that quantity is the same both in API and DB responses

        Expected result:
            1. Get users quantity API request returns a correct number of users
        """
        response = api.users.get_users_quantity().json()
        users_num_db = db.users.get_number_of_users()
        assert int(response) == int(users_num_db), f"FAILED\nExpected quantity: {users_num_db}. Actual: {response}"

    def test_get_random_user_from_all_users_list(self, api, db):
        """
        Steps:
            1. Send a GET request to /api/request to get all users
            2. Get ID of random user in the DB
            3. Make sure that a user with such ID exists in the API response

        Expected result:
            1. Random user from the DB exists in the API response
        """
        response = api.users.get_users().json()
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        for user in response:
            if user["id"] == user_id:
                return True
        raise AssertionError(f"FAILED\nUser with ID '{user_id}' is not found in the API response")

    @pytest.mark.negative
    @pytest.mark.parametrize("request_type", [HttpRequestType.DELETE, HttpRequestType.PUT, HttpRequestType.PATCH])
    def test_get_all_users_with_unsupported_request_type(
        self,
        api,
        db,
        request_type,
        expected_code=405
    ):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        endpoint = api.users.endpoints.users.default
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.get_users(expected_code=expected_code, request_type=request_type).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "request_type",
        [
            HttpRequestType.POST,
            HttpRequestType.DELETE,
            HttpRequestType.PUT,
            HttpRequestType.PATCH
        ]
    )
    def test_get_users_quantity_with_unsupported_request_type(
        self,
        api,
        db,
        request_type,
        expected_code=405
    ):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request/count
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        endpoint = api.users.endpoints.users.default
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.get_users_quantity(expected_code=expected_code, request_type=request_type).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.regress
    @pytest.mark.smoke
    def test_get_and_verify_user_by_id(self, api, db):
        """
        Steps:
            1. Get ID of random user in the DB
            2. Get user info by ID from the DB
            3. Send an GET request to /api/request/{user_id}
            4. Validate response

        Expected result:
            1. Returns the correct user
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        db_response = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        response = api.users.get_user_by_id(user_id).json()
        expected_response = SuccessUser(
            user_id=user_id,
            login=db_response["login"],
            alias=db_response["alias"],
            email=db_response["email"],
            phone=db_response["phone_number"],
            first_name=db_response["first_name"],
            last_name=db_response["second_name"],
            login_failed_attempts=db_response["login_failed_attempts"],
            otp_failed_attempts=db_response["otp_failed_attempts"],
            email_failed_attempts=db_response["email_failed_attempts"],
            pin_failed_attempts=db_response["pin_failed_attempts"],
            block_time=db_response["block_time"],
            has_tokens=db_response["has_token"],
            hash_=db_response["hash"]
        ).body
        assert expected_response == response, "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [0, 99999999])
    def test_get_user_by_non_existing_id(self, api, db, user_id):
        f"""
        Steps:
            1. Send a GET request to /api/request/{user_id} with non-existing ID
            2. Validate response

        Expected result:
            1. Returns an empty response
        """
        expected_response = None
        response = api.users.get_user_by_id(user_id=user_id).json()
        assert response == expected_response, "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [-1, 0.5, "x"])
    def test_get_user_by_negative_id(self, api, db, user_id, expected_code=400):
        f"""
        Steps:
            1. Send a GET request to /api/request/{user_id} with negative ID
            2. Validate error response

        Expected result:
            1. Returns the correct error response
        """
        endpoint = api.users.endpoints.users.by_id.format(user_id=user_id)
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.get_user_by_id(user_id=user_id, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize("request_type", [HttpRequestType.PATCH, HttpRequestType.POST])
    def test_get_user_by_id_with_unsupported_request_type(
        self,
        api,
        db,
        request_type,
        expected_code=405
    ):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request/<user_id>
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.users.by_id.format(user_id=user_id)
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.get_user_by_id(
            user_id=user_id, expected_code=expected_code, request_type=request_type
        ).json()
        api.users.validate_error_response(response, expected_response)
