import allure
import pytest

from src.api.responses.base import ErrorResponse
from src.api.responses.db_to_api_format import tokens_db_to_api_format as _format
from src.api.responses.tokens.tokens import InvalidOtpEnrollmentFinish, SuccessEnrollmentFinish
from src.common import string_utils as s


@allure.suite("Mail token creating tests")
class TestCreateMailToken:
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_create_default_mail(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Mail token has been created in DB
            4. Validate several fields in DB

        Expected result:
            1. Mail token has been successfully created
        """
        response = api.tokens.add_mail()["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert (
            (
                db_response["type"],
                db_response["digits"],
                db_response["enabled"],
                db_response["pin"]
            ) == (
                _format.token_type["MAIL"],
                6,  # digits
                True,  # enabled
                None  # pin
            )
        ), "FAILED"

    @pytest.mark.parametrize(
        "name",
        [
            f"{s.random_name(50)}",
            f"{s.random_name(1)}",
            "_-.@",
            f"mail {s.random_name(3)} {s.random_name(5)}",
            None,
        ]
    )
    def test_create_mail_with_valid_name(self, api, db, name):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Mail token has been created in DB
            4. Validate the name in DB

        Expected result:
            1. Mail token has been successfully created with a valid name
        """
        response = api.tokens.add_mail(email=s.random_email(), name=name)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert db_response["name"] == name, "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "name",
        [
            "   ",
            f"{s.random_name(51)}",
            f"mail_{s.random_name(4)}_%"
        ]
    )
    def test_create_mail_with_invalid_name(self, api, db, name, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the error response

        Expected result:
            1. Returns the correct error response
        """
        endpoint = api.tokens.endpoints.tokens.enrollment
        expected_response = ErrorResponse(
            error=api.tokens.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.tokens.api_utils.path_cutter(endpoint)
        ).body
        response = api.tokens.add_mail(name=name, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.parametrize(
        "email",
        [
            f"{s.random_email('max')}",
            "a@b.co",
            f"{s.random_name().upper()}@protectimus.com",
            "test-1_email.lo+check@protectimus.com"
        ]
    )
    def test_create_mail_with_valid_email(self, api, db, email):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Mail token has been created in DB
            4. Validate the email in DB

        Expected result:
            1. Mail token has been successfully created with different email
        """
        response = api.tokens.add_mail(email=email)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert db_response["serial_number"] == email, "FAILED"

    @pytest.mark.negative
    def test_create_mail_with_exiting_email(self, api, db, email="existing_email@protectimus.com", expected_code=400):
        f"""
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation with an email "{email}" and
               send a POST request to /api/request/<enrollment_id>/finish to finish enrollment
            2. Validate the response
            3. Send a POST request to /api/request to enroll Mail token creation with the same email "{email}"
            4. Validate error response
            5. Verify there is only one token with email "{email}" in DB

        Expected result:
            1. Mail token cannot be created with an existing email
        """
        response_token1 = api.tokens.add_mail(email=email)["response"]
        expected_response_token1 = SuccessEnrollmentFinish(token_id=response_token1["tokenId"]).body
        assert response_token1 == expected_response_token1, "FAILED"
        endpoint = api.tokens.endpoints.tokens.enrollment
        expected_response_token2 = ErrorResponse(
            error=api.tokens.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.tokens.api_utils.path_cutter(endpoint)
        ).body
        response_token2 = api.tokens.add_mail(email=email, expected_code=expected_code)
        api.tokens.validate_error_response(response_token2, expected_response_token2)
        db_response = db.tokens.get_all_token_info_by_serial(email)
        assert len(db_response) == 1, f"Second token was created. DB response: {db_response}"

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "email",
        [
            None,
            "",
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
    def test_create_mail_with_invalid_email(self, api, db, email, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the error response

        Expected result:
            1. Returns the correct error response
        """
        endpoint = api.tokens.endpoints.tokens.enrollment
        expected_response = ErrorResponse(
            error=api.tokens.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.tokens.api_utils.path_cutter(endpoint)
        ).body
        response = api.tokens.add_mail(email=email, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize("otp", ["000000", 12345, 1234567, " "])
    def test_create_mail_invalid_otp(self, api, db, otp):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment with invalid OTP
            2. Validate the error response

        Expected result:
            1. Returns the correct error response about invalid OTP
        """
        response = api.tokens.add_mail(otp=otp)["response"]
        expected_response = InvalidOtpEnrollmentFinish().body
        assert response == expected_response, "FAILED"

    @pytest.mark.regress
    def test_create_mail_8otp(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Mail token has been created in DB
            4. Validate 'digits' field in the DB

        Expected result:
            1. Mail token has been successfully created
        """
        response = api.tokens.add_mail(digits=8)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert db_response["digits"] == 8, "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "length",
        [
            None,
            "",
            " ",
            "x",
            0,
            1,
            5,
            7,
            9
        ]
    )
    def test_create_mail_with_invalid_length(self, api, db, length, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the error response

        Expected result:
            1. Returns the correct error response
        """
        endpoint = api.tokens.endpoints.tokens.enrollment
        expected_response = ErrorResponse(
            error=api.tokens.http_errors.get_error_from_code(expected_code),
            status=expected_code,
            path=api.tokens.api_utils.path_cutter(endpoint)
        ).body
        response = api.tokens.add_mail(digits=length, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    def test_create_mail_with_user_and_admin_assignment(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Mail token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Mail token has been created in DB
            4. Validate that the token has been assigned to the admin and user in the DB

        Expected result:
            1. Mail token has been successfully created and assigned to the admin and user
        """
        admin_id = db.admins.get_random_admin(json_output=True)[0]["id"]
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        response = api.tokens.add_mail(admin_id=admin_id, user_id=user_id)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert (db_response["client_staff_id"], db_response["user_id"]) == (admin_id, user_id), "FAILED"
