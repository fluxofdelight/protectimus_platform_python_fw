import allure
import pytest

from src.api.responses.base import ErrorResponse
from src.common.enum_common.http_request_type import HttpRequestType


@allure.suite("Get tokens tests")
class TestGetTokens:
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_get_all_tokens_and_verify_quantity(self, api, db):
        """
        Steps:
            1. Send a GET request to /api/request to get all tokens
            2. Get quantity of tokens from the DB
            3. Make sure that quantity is the same both in API and DB responses

        Expected result:
            1. Get all tokens API request returns all tokens
        """
        response = api.tokens.get_tokens().json()
        tokens_num_db = db.tokens.get_number_of_tokens()
        assert len(response) == int(tokens_num_db), \
            f"FAILED\nExpected quantity: {tokens_num_db}. Actual: {len(response)}"

    def test_verify_tokens_quantity(self, api, db):
        """
        Steps:
            1. Send a GET request to /api/request/count to get tokens quantity
            2. Get quantity of tokens from the DB
            3. Make sure that quantity is the same both in API and DB responses

        Expected result:
            1. Get tokens quantity API request returns a correct number of tokens
        """
        response = api.tokens.get_tokens_quantity().json()
        tokens_num_db = db.tokens.get_number_of_tokens()
        assert int(response) == int(tokens_num_db), f"FAILED\nExpected quantity: {tokens_num_db}. Actual: {response}"

    @pytest.mark.negative
    @pytest.mark.parametrize("request_type", [HttpRequestType.DELETE, HttpRequestType.PUT, HttpRequestType.PATCH])
    def test_get_all_tokens_with_unsupported_request_type(self, api, db, request_type, expected_code=405):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        endpoint = api.tokens.endpoints.tokens.default
        expected_response = ErrorResponse(
            error=api.tokens.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.tokens.api_utils.path_cutter(endpoint)
        ).body
        response = api.tokens.get_tokens(expected_code=expected_code, request_type=request_type).json()
        api.tokens.validate_error_response(response, expected_response)

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
    def test_get_tokens_quantity_with_unsupported_request_type(self, api, db, request_type, expected_code=405):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request/count
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        endpoint = api.tokens.endpoints.tokens.count_total
        expected_response = ErrorResponse(
            error=api.tokens.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.tokens.api_utils.path_cutter(endpoint)
        ).body
        response = api.tokens.get_tokens_quantity(expected_code=405, request_type=request_type).json()
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize("token_id", [0, 99999999])
    def test_get_token_by_non_existing_id(self, api, db, token_id):
        f"""
        Steps:
            1. Send a GET request to /api/request/{token_id} with non-existing ID
            2. Validate response

        Expected result:
            1. Returns an empty response
        """
        expected_response = None
        response = api.tokens.get_token_by_id(token_id=token_id).json()
        assert response == expected_response, "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize("token_id", [-1, 0.5, "x"])
    def test_get_token_by_negative_id(self, api, db, token_id, expected_code=400):
        f"""
        Steps:
            1. Send a GET request to /api/request/{token_id} with negative ID
            2. Validate error response

        Expected result:
            1. Returns the correct error response
        """
        endpoint = api.tokens.endpoints.tokens.by_id.format(token_id=token_id)
        expected_response = ErrorResponse(
            error=api.tokens.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.tokens.api_utils.path_cutter(endpoint)
        ).body
        response = api.tokens.get_token_by_id(token_id=token_id, expected_code=expected_code).json()
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize("request_type", [HttpRequestType.PATCH, HttpRequestType.POST, HttpRequestType.PUT])
    def test_get_token_by_id_with_unsupported_request_type(self, api, db, request_type, expected_code=405):
        f"""
        Steps:
            1. Send a {request_type} request to /api/request/<token_id>
            2. Validate error response

        Expected result:
            1. {request_type} request type is unsupported
        """
        token_id = db.tokens.get_random_token(json_output=True)[0]["id"]
        endpoint = api.tokens.endpoints.tokens.by_id.format(token_id=token_id)
        expected_response = ErrorResponse(
            error=api.tokens.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.tokens.api_utils.path_cutter(endpoint)
        ).body
        response = api.tokens.get_token_by_id(token_id=token_id, expected_code=405, request_type=request_type).json()
        api.tokens.validate_error_response(response, expected_response)
