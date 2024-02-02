import allure
import pytest

from src.api.responses.base import ErrorResponse
from src.api.responses.users.users import SuccessUser
from src.common import string_utils as s


@allure.suite("User creating tests")
class TestCreateUser:
    @pytest.mark.regress
    def test_create_default_user(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to create a default user
            2. Validate response
            3. Verify a user has been created in DB

        Expected result:
            1. User was successfully created
        """
        response = api.users.add_user().json()
        expected_response = SuccessUser(user_id=response["id"], login=response["login"], hash_=response["hash"]).body
        assert response == expected_response, "FAILED"
        assert db.users.get_all_user_info_by_id(response["id"]), f"User '{response['login']}' wasn't created"

    @pytest.mark.negative
    def test_create_user_with_empty_payload(self, api, db, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to create a user with an empty payload
            2. Validate error response

        Expected result:
            1. User cannot be created with an empty payload
        """
        endpoint = api.users.endpoints.users.default
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.add_user(request_body=" ", expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)

    @pytest.mark.smoke
    @pytest.mark.regress
    def test_create_user_with_all_settings(
        self,
        api,
        db,
        alias=f"user_alias_{s.random_name(4)}",
        email=s.random_email(),
        phone=s.random_phone(),
        password=s.random_password()
    ):
        """
        Steps:
            1. Send a POST request to /api/request to create a user with all available settings
            2. Validate response
            3. Verify a user has been created in DB
            4. Verify the DB response with the API response

        Expected result:
            1. User was successfully created with all settings
        """
        response = api.users.add_user(
            alias=alias,
            email=email,
            phone_number=phone,
            password=password,
        ).json()
        expected_response = SuccessUser(
            user_id=response["id"],
            login=response["login"],
            alias=alias,
            email=email,
            phone=phone,
            hash_=response["hash"]
        ).body
        assert response == expected_response, "FAILED"
        db_response = db.users.get_all_user_info_by_id(response["id"], json_output=True)[0]
        assert db_response, f"User '{response['login']}' wasn't created"
        assert (
            (
                db_response["id"],
                db_response["login"],
                db_response["alias"],
                db_response["email"],
                db_response["phone_number"]
            ) == (
                response["id"],
                response["login"],
                response["alias"],
                response["email"],
                response["phoneNumber"]
            )
        ), "FAILED"
        assert db_response["password"], "Password wasn't created"

    @pytest.mark.negative
    def test_create_user_with_same_login_and_alias(
        self,
        api,
        db,
        login="same_login_and_alias",
        alias="same_login_and_alias",
        expected_code=400
    ):
        f"""
        Steps:
            1. Send a POST request to /api/request to create a user with the same login and alias
            2. Validate error response
            3. Verify that a user with login "{login}" wasn't created in the DB

        Expected result:
            1. User cannot be created with the same login and alias
        """
        endpoint = api.users.endpoints.users.default
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.add_user(login=login, alias=alias, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)
        db_response = db.users.get_all_user_info_by_login(login)
        assert not db_response, f"User was created. DB response: {db_response}"

    @pytest.mark.negative
    def test_create_user_with_existing_login(
        self,
        api,
        db,
        login="existing_user_test",
        expected_code=400
    ):
        f"""
        Steps:
            1. Send a POST request to /api/request to create a default user with the login "{login}"
            2. Validate response
            3. Send a POST request to /api/request to create a user with an existing login "{login}"
            4. Validate error response
            5. Verify there is only one user with login "{login}" in DB

        Expected result:
            1. User cannot be created with an existing login
        """
        response_user1 = api.users.add_user(login=login).json()
        expected_response_user1 = SuccessUser(
            user_id=response_user1["id"],
            login=login,
            hash_=response_user1["hash"]
        ).body
        assert response_user1 == expected_response_user1, "FAILED"
        endpoint = api.users.endpoints.users.default
        expected_response_user2 = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response_user2 = api.users.add_user(login=login, expected_code=expected_code).json()
        api.users.validate_error_response(response_user2, expected_response_user2)
        db_response = db.users.get_all_user_info_by_login(login)
        assert len(db_response) == 1, f"Second user was created. DB response: {db_response}"

    @pytest.mark.negative
    def test_create_user_with_existing_alias(
        self,
        api,
        db,
        alias="existing_alias_test",
        expected_code=400
    ):
        f"""
        Steps:
            1. Send a POST request to /api/request to create a default user with the alias "{alias}"
            2. Validate response
            3. Send a POST request to /api/request to create a user with an existing alias "{alias}"
            5. Validate error response
            6. Verify there is only one user with alias "{alias}" in DB

        Expected result:
            1. User cannot be created with an existing alias
        """
        response_user1 = api.users.add_user(alias=alias).json()
        expected_response_user1 = SuccessUser(
            user_id=response_user1["id"],
            login=response_user1["login"],
            alias=alias,
            hash_=response_user1["hash"]
        ).body
        assert response_user1 == expected_response_user1, "FAILED"
        endpoint = api.users.endpoints.users.default
        expected_response_user2 = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response_user2 = api.users.add_user(alias=alias, expected_code=expected_code).json()
        api.users.validate_error_response(response_user2, expected_response_user2)
        db_response = db.users.get_all_user_info_by_alias(alias)
        assert len(db_response) == 1, f"Second user was created. DB response: {db_response}"

    @pytest.mark.negative
    def test_create_user_with_existing_email(
        self,
        api,
        db,
        email="existing_email@test.co",
        expected_code=400
    ):
        f"""
        Steps:
            1. Send a POST request to /api/request to create a default user with the email "{email}"
            2. Validate response
            3. Send a POST request to /api/request to create a user with an existing email "{email}"
            5. Validate error response
            6. Verify there is only one user with email "{email}" in DB

        Expected result:
            1. User cannot be created with an existing email
        """
        response_user1 = api.users.add_user(email=email).json()
        expected_response_user1 = SuccessUser(
            user_id=response_user1["id"],
            login=response_user1["login"],
            email=email,
            hash_=response_user1["hash"]
        ).body
        assert response_user1 == expected_response_user1, "FAILED"
        endpoint = api.users.endpoints.users.default
        expected_response_user2 = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response_user2 = api.users.add_user(email=email, expected_code=expected_code).json()
        api.users.validate_error_response(response_user2, expected_response_user2)
        db_response = db.users.get_all_user_info_by_email(email)
        assert len(db_response) == 1, f"Second user was created. DB response: {db_response}"

    @pytest.mark.negative
    def test_create_user_with_existing_phone(
        self,
        api,
        db,
        phone="123456789012345",
        expected_code=400
    ):
        f"""
        Steps:
            1. Send a POST request to /api/request to create a default user with the phone "{phone}"
            2. Validate response
            3. Send a POST request to /api/request to create a user with an existing phone "{phone}"
            5. Validate error response
            6. Verify there is only one user with phone "{phone}" in DB

        Expected result:
            1. User cannot be created with an existing phone
        """
        response_user1 = api.users.add_user(phone=phone).json()
        expected_response_user1 = SuccessUser(
            user_id=response_user1["id"],
            login=response_user1["login"],
            phone=phone,
            hash_=response_user1["hash"]
        ).body
        assert response_user1 == expected_response_user1, "FAILED"
        endpoint = api.users.endpoints.users.default
        expected_response_user2 = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response_user2 = api.users.add_user(phone=phone, expected_code=expected_code).json()
        api.users.validate_error_response(response_user2, expected_response_user2)
        db_response = db.users.get_all_user_info_by_phone(phone)
        assert len(db_response) == 1, f"Second user was created. DB response: {db_response}"

    @pytest.mark.parametrize(
        "login",
        [
            f"{s.random_name(4)}_-@~!#%+.$",
            f"{s.random_name(1)}",
            f"{s.random_name(50)}",
            f"{s.random_name(4)}_логин",
        ]
    )
    def test_create_user_with_different_login(self, login, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to create a user with different login
            2. Validate response
            3. Verify a user has been created in DB
            4. Verify the login of user in DB

        Expected result:
            1. User was successfully created with different login
        """
        response = api.users.add_user(login=login).json()
        expected_response = SuccessUser(user_id=response["id"], login=login, hash_=response["hash"]).body
        assert response == expected_response, "FAILED"
        db_response = db.users.get_all_user_info_by_id(response["id"], json_output=True)[0]
        assert db_response, f"User '{login}' wasn't created"
        assert db_response["login"] == login, f"FAILED. Expected login: {login}, actual login: {db_response['login']}"

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "login",
        [
            None,
            "",
            "   ",
            f"{s.random_name(51)}",
            f"  {s.random_name()}  ",
            f"{s.random_name(4)} l o g i n",
            f"{s.random_name(4)}_`",
            f"{s.random_name(4)}_:",
            f"{s.random_name(4)}_*",
            f"{s.random_name(4)}_&",
            f"{s.random_name(4)}_^",
            f"{s.random_name(4)}_%"
        ]
    )
    def test_create_user_with_different_login_negative(self, login, api, db, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to create a user with different negative login
            2. Validate response
            3. Verify a user hasn't been created in DB
            4. Verify the login of user in DB

        Expected result:
            1. User wasn't created with different negative login
        """
        endpoint = api.users.endpoints.users.default
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.add_user(login=login, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)
        db_response = db.users.get_all_user_info_by_login(login)
        assert not db_response, f"User was created. DB response: {db_response}"

    @pytest.mark.parametrize(
        "email",
        [
            f"{s.random_email('max')}",
            "a@b.co",
            f"{s.random_name().upper()}@protectimus.com",
            "test-1_email.lo+check@protectimus.com",
        ]
    )
    def test_create_user_with_different_email(self, email, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to create a user with different email
            2. Validate response
            3. Verify a user has been created in DB
            4. Verify the alias of user in DB

        Expected result:
            1. User was successfully created with different email
        """
        response = api.users.add_user(login=("user_" + s.random_name()), email=email).json()
        expected_response = SuccessUser(
            user_id=response["id"],
            login=response["login"],
            email=email,
            hash_=response["hash"]
        ).body
        assert response == expected_response, "FAILED"
        db_response = db.users.get_all_user_info_by_id(response["id"], json_output=True)[0]
        assert db_response, f"User with email '{email}' wasn't created"
        assert db_response["email"] == email, f"FAILED. Expected email: {email}, actual email: {db_response['email']}"

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "email",
        [
            "   ",
            "a@b.c",
            f"{s.random_email(85, negative=True)}",
            "name@domain.",
            f"  {s.random_email()}  ",
            "name@domain",
            "name@",
            "name@@domain.com",
            "почта@domain.com",
            "!na%m*e@dom&ain.co",
            "name@domain,com",
            f"{s.random_email(domain='-domain.co')}",
            ".name@domain.com",
            "name.@domain.com",
            "-name@domain.com",
            "name-@domain.com",
            "na me@domain.com",
        ]
    )
    def test_create_user_with_different_email_negative(self, email, api, db, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to create a user with different negative email
            2. Validate response
            3. Verify a user hasn't been created in DB
            4. Verify the email of user in DB

        Expected result:
            1. User wasn't created with different negative email
        """
        endpoint = api.users.endpoints.users.default
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.add_user(email=email, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)
        db_response = db.users.get_all_user_info_by_email(email)
        assert not db_response, f"User was created. DB response: {db_response}"

    @pytest.mark.negative
    def test_create_user_without_full_name(self, api, db, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to create a user without full name
            2. Validate response
            3. Verify a user hasn't been created in DB

        Expected result:
            1. User cannot be created without full name
        """
        login = f"user_{s.random_name()}"
        endpoint = api.users.endpoints.users.default
        expected_response = ErrorResponse(
            error=api.users.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.users.api_utils.path_cutter(endpoint)
        ).body
        response = api.users.add_user(login=login, first_name=None, last_name=None, expected_code=expected_code).json()
        api.users.validate_error_response(response, expected_response)
        db_response = db.users.get_all_user_info_by_login(login)
        assert not db_response, f"User was created. DB response: {db_response}"
