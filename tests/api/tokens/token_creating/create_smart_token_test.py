import allure
import pytest

from src.api.responses.base import ErrorResponse
from src.api.responses.db_to_api_format import tokens_db_to_api_format as _format
from src.api.responses.tokens.tokens import InvalidOtpEnrollmentFinish, SuccessEnrollmentFinish
from src.common import string_utils as s


@allure.suite("Smart token creating tests")
class TestCreateSmart:
    @pytest.mark.regress
    @pytest.mark.smoke
    def test_create_default_smart(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Smart token has been created in DB
            4. Validate several fields in DB

        Expected result:
            1. Smart token has been successfully created
        """
        response = api.tokens.add_smart()["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert (
            (
                db_response["type"],
                db_response["unify_key_algo"],
                db_response["unify_token_type"],
                db_response["serial_number"][:6],
                db_response["digits"],
                db_response["time_interval"],
                db_response["enabled"],
                db_response["pin"]
            ) == (
                _format.token_type["PROTECTIMUS_SMART"],
                _format.unify_key_algo["SHA256"],
                _format.unify_token_type["OATH_TOTP"],
                "SMT:1-",
                6,  # digits
                30,  # time_interval
                True,  # enabled
                None  # pin
            )
        ), "FAILED"

    @pytest.mark.parametrize("period", [60, 90, 86370, 86400])  # 30 is in the case above
    def test_create_smart_totp_with_valid_period(self, api, db, period):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Smart token has been created in DB
            4. Validate the period in DB

        Expected result:
            1. Smart token has been successfully created with a valid period
        """
        response = api.tokens.add_smart(period=period)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert db_response["time_interval"] == period, "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "period",
        [
            None,
            "",
            " ",
            "x",
            0,
            1,
            29,
            45,
            86401,
            86430
        ]
    )
    def test_create_smart_totp_with_invalid_period(self, api, db, period, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
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
        response = api.tokens.add_smart(period=period, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    def test_create_smart_hotp_8otp_sha512(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Smart token has been created in DB
            4. Validate several fields in DB

        Expected result:
            1. Smart token has been successfully created
        """
        response = api.tokens.add_smart(oath_type="hotp", algorithm="HmacSHA512", digits=8)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert (
            (
                db_response["type"],
                db_response["unify_key_algo"],
                db_response["unify_token_type"],
                db_response["serial_number"][:6],
                db_response["digits"],
                db_response["enabled"],
                db_response["pin"]
            ) == (
                _format.token_type["PROTECTIMUS_SMART"],
                _format.unify_key_algo["SHA512"],
                _format.unify_token_type["OATH_HOTP"],
                "SMT:1-",
                8,  # digits
                True,  # enabled
                None  # pin
            )
        ), "FAILED"

    @pytest.mark.negative
    def test_create_smart_hotp_with_custom_period(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Smart token has been created in DB
            4. Validate the period in DB

        Expected result:
            1. HOTP Smart token has been successfully created with a custom period
        """
        response = api.tokens.add_smart(oath_type="hotp", period=150)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert db_response["time_interval"] == 150, "FAILED"

    def test_create_smart_ocra_sha1(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Smart token has been created in DB
            4. Validate several fields in DB

        Expected result:
            1. Smart token has been successfully created
        """
        response = api.tokens.add_smart(
            oath_type="ocra",
            algorithm="HmacSHA1"
        )["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert (
            (
                db_response["type"],
                db_response["unify_key_algo"],
                db_response["unify_token_type"],
                db_response["serial_number"][:6],
                db_response["enabled"],
                db_response["pin"]
            ) == (
                _format.token_type["PROTECTIMUS_SMART"],
                _format.unify_key_algo["SHA1"],
                _format.unify_token_type["OATH_OCRA"],
                "SMT:1-",
                True,  # enabled
                None  # pin
            )
        ), "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize("otp", [12345678, 1, 123456789, 1234567, 12345, "x", " "])
    def test_create_smart_invalid_otp(self, api, db, otp):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment with invalid OTP
            2. Validate the error response

        Expected result:
            1. Returns the correct error response about invalid OTP
        """
        response = api.tokens.add_smart(otp=otp)["response"]
        expected_response = InvalidOtpEnrollmentFinish().body
        assert response == expected_response, "FAILED"

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
    def test_create_smart_with_invalid_length(self, api, db, length, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
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
        response = api.tokens.add_smart(digits=length, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "oath_type",
        [
            None,
            "",
            " ",
            "test",
            "otp",
            0,
            1
        ]
    )
    def test_create_smart_with_invalid_oath_type(self, api, db, oath_type, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
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
        response = api.tokens.add_smart(oath_type=oath_type, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "algorithm",
        [
            None,
            "",
            " ",
            "test",
            "HmacMD5",
            "HmacSHA3",
            "HmacSHA3-256",
            "HmacSHA224",
            "HMACSHA1",
            "SHA1",
            "SHA256",
            "SHA512",
            "MD5",
            0,
            1
        ]
    )
    def test_create_smart_with_invalid_algorithm(self, api, db, algorithm, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
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
        response = api.tokens.add_smart(algorithm=algorithm, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.parametrize(
        "pin, pin_format",
        [
            ("1234", "PIN_AFTER_OTP"),
            ("0000", "PIN_AFTER_OTP"),
            ("9999", "PIN_AFTER_OTP"),
            ("1234", "PIN_BEFORE_OTP"),
            ("0000", "PIN_BEFORE_OTP"),
            ("9999", "PIN_BEFORE_OTP")
        ]
    )
    def test_create_smart_with_valid_pin(self, api, db, pin, pin_format):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Smart token has been created in DB
            4. Validate the PIN in DB

        Expected result:
            1. Smart token has been successfully created with a valid PIN
        """
        response = api.tokens.add_smart(pin=pin, pin_format=pin_format)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert (db_response["pin"], db_response["pin_otp_format"]) == (pin, _format.get_db_pin_format(pin_format)), \
            "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "pin, pin_format",
        [
            ("1", "PIN_AFTER_OTP"),
            ("12", "PIN_AFTER_OTP"),
            ("123", "PIN_AFTER_OTP"),
            ("12345", "PIN_AFTER_OTP"),
            ("123x", "PIN_AFTER_OTP"),
            ("test", "PIN_AFTER_OTP"),
            ("    ", "PIN_AFTER_OTP"),
            ("1", "PIN_BEFORE_OTP"),
            ("12", "PIN_BEFORE_OTP"),
            ("123", "PIN_BEFORE_OTP"),
            ("12345", "PIN_BEFORE_OTP"),
            ("123x", "PIN_BEFORE_OTP"),
            ("test", "PIN_BEFORE_OTP"),
            ("    ", "PIN_BEFORE_OTP"),
            ("1234", "PIN_IN_OTP"),
            ("1234", "PIN"),
            ("1234", 1),
            ("1234", 0),
            ("1234", " "),
            ("1234", ""),
            ("1234", None)
        ]
    )
    def test_create_smart_with_invalid_pin(self, api, db, pin, pin_format, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
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
        response = api.tokens.add_smart(pin=pin, pin_format=pin_format, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.parametrize(
        "name",
        [
            f"{s.random_name(50)}",
            f"{s.random_name(1)}",
            "_-.@",
            f"smart {s.random_name(3)} {s.random_name(5)}",
            f"{s.random_name(4)}_смарт"
            "",
            None,
        ]
    )
    def test_create_smart_with_valid_name(self, api, db, name):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Smart token has been created in DB
            4. Validate the name in DB

        Expected result:
            1. Smart token has been successfully created with a valid PIN
        """
        response = api.tokens.add_smart(name=name)["response"]
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
            f"  {s.random_name()}  ",
            f"smart_{s.random_name(4)}_?",
            f"smart_{s.random_name(4)}_/",
            f"smart_{s.random_name(4)}_>",
            f"smart_{s.random_name(4)}_<",
            f"smart_{s.random_name(4)}_%"
        ]
    )
    def test_create_smart_with_invalid_name(self, api, db, name, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
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
        response = api.tokens.add_smart(name=name, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)

    @pytest.mark.regress
    def test_create_smart_with_user_assignment(self, api, db):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
               send a POST request to /api/request/{enrollment_id}/finish to finish enrollment
            2. Validate the response
            3. Verify a Smart token has been created in DB
            4. Validate that the token has been assigned to the user in the DB

        Expected result:
            1. Smart token has been successfully created and assigned to the user
        """
        user_id = db.users.get_random_user(json_output=True)[0]["id"]
        response = api.tokens.add_smart(user_id=user_id)["response"]
        expected_response = SuccessEnrollmentFinish(token_id=response["tokenId"]).body
        assert response == expected_response, "FAILED"
        db_response = db.tokens.get_all_token_info_by_id(response["tokenId"], json_output=True)[0]
        assert db_response, "Token wasn't created"
        assert db_response["user_id"] == user_id, "FAILED"

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [" ", "x", 9999999, -1])
    def test_create_smart_with_user_assignment_negative(self, api, db, user_id, expected_code=400):
        """
        Steps:
            1. Send a POST request to /api/request to enroll Smart token creation and
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
        response = api.tokens.add_smart(user_id=user_id, expected_code=expected_code)
        api.tokens.validate_error_response(response, expected_response)
