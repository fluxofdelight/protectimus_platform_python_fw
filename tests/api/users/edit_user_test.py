import allure
import pytest

from src.api.responses.base import ErrorResponse
from src.api.responses.users.users import SuccessUser
from src.common import string_utils as s


@allure.suite("Edit user tests")
class TestEditUser:
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_edit_all_user_settings(
        self,
        api,
        db,
        login=f"new_login{s.random_name(4)}",
        alias=f"new_alias{s.random_name(4)}",
        email=s.random_email(),
        phone=s.random_phone(),
        password=s.random_password(),
        first_name=f"Name_{s.random_name(4)}",
        last_name=f"Last_name_{s.random_name(4)}"
    ):
        """
        Steps:
            1. Get ID of a random user in the DB
            2. Get info of not edited user from the DB
            3. Send a PUT request to /api/request/{user_id} to edit all available user settings
            4. Get info of edited user from the DB
            5. Validate response
            6. Validate user password with 'not edited' and 'edited' DB response
            7. Verify the DB response with the API response

        Expected result:
            1. All settings of the user were successfully edited
        """
        db_response_not_edited = db.users.get_random_user(json_output=True)[0]
        user_id = db_response_not_edited["id"]
        response = api.users.edit_user(
            user_id=user_id,
            login=login,
            alias=alias,
            email=email,
            phone_number=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        ).json()
        db_response_edited = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        expected_response = SuccessUser(
            user_id=user_id,
            login=login,
            alias=alias,
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            hash_=db_response_edited["hash"]
        ).body
        assert response == expected_response, "FAILED"
        assert db_response_not_edited["password"] != db_response_edited["password"], "FAILED"
        assert (
            (
                db_response_edited["id"],
                db_response_edited["login"],
                db_response_edited["alias"],
                db_response_edited["email"],
                db_response_edited["phone_number"],
                db_response_edited["first_name"],
                db_response_edited["second_name"]
            ) == (
                response["id"],
                response["login"],
                response["alias"],
                response["email"],
                response["phoneNumber"],
                response["firstName"],
                response["secondName"]
            )
        ), "FAILED"

    @pytest.mark.regress
    @pytest.mark.smoke
    def test_edit_user_delete_all_settings(self, api, db):
        """
        Steps:
            1. Get ID of a random user in the DB
            2. Get info of not edited user from the DB
            3. Send a PUT request to /api/request/{user_id} to remove all available user settings except
               login and full name
            4. Get info of edited user from the DB
            5. Validate response
            6. Validate user password with 'not edited' and 'edited' DB response
            7. Verify the DB response with the API response

        Expected result:
            1. All settings of the user were successfully edited
        """
        db_response_not_edited = db.users.get_random_user(json_output=True)[0]
        user_id = db_response_not_edited["id"]
        response = api.users.edit_user(
            user_id=user_id,
            alias=None,
            email=None,
            phone_number=None,
            password=None
        ).json()
        db_response_edited = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        expected_response = SuccessUser(
            user_id=user_id,
            login=db_response_not_edited["login"],
            alias=None,
            email=None,
            phone=None,
            hash_=db_response_not_edited["hash"]
        ).body
        assert response == expected_response, "FAILED"
        assert (db_response_edited["password"] is None
                or db_response_edited["password"] != db_response_not_edited["password"]), "FAILED"
        assert (
            (
                db_response_edited["id"],
                db_response_edited["alias"],
                db_response_edited["email"],
                db_response_edited["phone_number"]
            ) == (
                response["id"],
                response["alias"],
                response["email"],
                response["phoneNumber"]
            )
        ), "FAILED"

    @pytest.mark.negative
    def test_edit_user_with_empty_payload(self, api, db, expected_code=400):
        """
        Steps:
            1. Send a PUT request to /api/request to edit a user with an empty payload
            2. Validate error response

        Expected result:
            1. User cannot be created with an empty payload
        """
        db_response_not_edited = db.users.get_random_user(json_output=True)[0]
        user_id = db_response_not_edited["id"]
        endpoint = api.users.endpoints.users.by_id.format(user_id=user_id)
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.edit_user(
            user_id=user_id, expected_code=expected_code, request_body=" ", negative=True
        ).json()
        api.users.validate_error_response(response, expected_response)
        db_response_edited = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response_not_edited == db_response_edited, \
            (f"FAILED\nUser was edited. DB response not edited: {db_response_not_edited}\n"
             f"DB response edited: {db_response_edited}")

    @pytest.mark.negative
    def test_edit_user_existing_login(
        self,
        api,
        db,
        login="existing_login_edit",
        expected_code=400
    ):
        """
        Steps:
            1. Send a POST request to /api/request to create a default user with the login "{login}"
            2. Validate response
            3. Send a PUT request to /api/request/{user_id} to edit user login and change it to an existing "{login}"
            4. Validate error response
            5. Verify that edited user doesn't have login "{login}" in the DB

        Expected result:
            1. User cannot be created with an existing login
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        response_create_user = api.users.add_user(login=login).json()
        expected_response_create_user = SuccessUser(
            user_id=response_create_user["id"],
            login=login,
            hash_=response_create_user["hash"]
        ).body
        assert response_create_user == expected_response_create_user, "FAILED"
        endpoint = api.users.endpoints.users.by_id.format(user_id=user_id)
        expected_response_edit_user = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response_edit_user = api.users.edit_user(user_id=user_id, login=login, expected_code=expected_code).json()
        api.users.validate_error_response(response_edit_user, expected_response_edit_user)
        db_response = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response["login"] != login, f"FAILED\nLogin was changed to existing one. DB response: {db_response}"

    @pytest.mark.negative
    def test_edit_user_with_same_login_and_alias(
        self,
        api,
        db,
        login="same_login_and_alias_edit",
        alias="same_login_and_alias_edit",
        expected_code=400
    ):
        """
        Steps:
            1. Send a PUT request to /api/request/{user_id} to create a user with the same login and alias
            2. Validate error response
            3. Verify that a user wasn't edited in the DB

        Expected result:
            1. User cannot be edited with the same login and alias
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.users.by_id.format(user_id=user_id)
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.edit_user(user_id=user_id, login=login, alias=alias, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)
        db_response = db.users.get_all_user_info_by_id(user_id)
        assert (db_response["login"], db_response["alias"]) != (login, alias), \
            f"User was created. DB response: {db_response}"

    @pytest.mark.negative
    def test_edit_user_without_full_name(self, api, db, expected_code=400):
        """
        Steps:
            1. Send a PUT request to /api/request/{user_id} to edit user full name without specifying it
            2. Validate response
            3. Verify a user hasn't been edited in DB

        Expected result:
            1. User cannot be edited without specifying full name
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        endpoint = api.users.endpoints.users.by_id.format(user_id=user_id)
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.edit_user(
            user_id=user_id, first_name=None, last_name=None, expected_code=expected_code
        ).json()
        api.users.validate_error_response(response, expected_response)
        db_response = db.users.get_all_user_info_by_id(user_id, json_output=True)[0]
        assert db_response["first_name"] and db_response["last_name"] is not None, \
            f"User was edited. DB response: {db_response}"
