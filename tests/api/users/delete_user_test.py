import allure
import pytest

from src.api.responses.base import ErrorResponse


@allure.suite("Delete user tests")
class TestDeleteUser:
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_delete_user(self, api, db):
        """
        Steps:
            1. Get a random user from the DB
            2. Send a DELETE request to /api/request/{user_id} to delete the user
            3. Validate the response status
            4. Make sure that user doesn't exist in the DB

        Expected result:
            1. User was successfully deleted
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        response = api.users.delete_user(user_id)
        assert response.reason == "OK", "FAILED"
        db_response = db.users.get_all_user_info_by_id(user_id)
        assert not db_response, f"FAILED. User wasn't deleted, DB response: {db_response}"

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [0, 99999999])
    def test_delete_user_by_non_existing_id(self, api, db, user_id, expected_code=400):
        f"""
        Steps:
            1. Send a DELETE request to /api/request/{user_id} with non-existing ID
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
        response = api.users.delete_user(user_id, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)
