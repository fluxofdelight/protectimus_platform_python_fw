from typing import Optional

import allure
import pyotp
from requests import Session

from src.api.pages.base_api import BaseAPI
from src.common import string_utils as s
from src.common.ocra import OCRA
from src.configs.config import Config


class Tokens(BaseAPI):
    def __init__(self, session: Optional[Session], config):
        self.session = session or Session()
        self.config = config or Config().api
        self.ocra = OCRA()
        super().__init__(self.session, self.config)

    @allure.step("Get secret of the token and generate OTP")
    def generate_otp_with_existing_token(self, token_id, challenge=None, expected_code=200):
        token_info = self.get_token_by_id(token_id, expected_code)
        secret = token_info["secret"]
        oath_type = token_info["unifyTokenType"]
        digits = token_info["digits"]
        algorithm = token_info["unifyKeyAlgo"]
        period = token_info["timeInterval"]
        if oath_type.upper() == "OATH_TOTP":
            otp = pyotp.TOTP(secret, digits=digits, digest=algorithm, interval=period).now()
            return otp
        if oath_type.upper() == "OATH_HOTP":
            counter = token_info["counter"]
            otp = pyotp.HOTP(secret, digits=digits, digest=algorithm, initial_count=counter).at(counter + 1)
            return otp
        if oath_type.upper() == "OATH_OCRA":
            otp = self.ocra.generate_ocra(secret, challenge, algorithm=algorithm)
            return otp

    @allure.step("Send an API request to /api/request")
    def get_tokens(self, response_size=1000, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.default,
            request_type or self.requests_type.GET,
            params=f"size={response_size}",
            expected_code=expected_code
        )
        return response

    @allure.step("Send an API request to /api/request")
    def get_tokens_quantity(self, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.count_total, request_type or self.requests_type.GET, expected_code=expected_code
        )
        return response

    @allure.step("Send a GET request to /api/request")
    def get_token_by_id(self, token_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.by_id.format(token_id=token_id),
            request_type or self.requests_type.GET,
            expected_code=expected_code,
        )
        return response

    def add_smart(
        self,
        name=("smart_" + s.random_name()),
        oath_type="totp",
        algorithm="HmacSHA256",
        issuer="Protectimus",
        period=30,
        digits=6,
        pin=None,
        pin_format=None,
        user_id=None,
        admin_id=None,
        max_attempts=10,
        timeout_seconds=9999,
        request_body=None,
        otp=None,
        expected_code=200,
    ):
        enrollment_data = (
            request_body
            if request_body
            else {
                "maxAttempts": max_attempts,
                "timeoutSeconds": timeout_seconds,
                "tokenRegistrationOptions": {
                    "name": name,
                    "type": self.token_type.software.SMART,
                    "otpCredentialParams": {
                        "issuer": issuer,
                        "type": oath_type.lower() if isinstance(oath_type, str) else oath_type,
                        "algorithm": algorithm,
                        "period": period,
                        "digits": digits,
                    },
                },
            }
        )
        if user_id or admin_id:
            enrollment_data["binding"] = {}
            if user_id:
                enrollment_data["binding"].update({"userId": user_id})
            if admin_id:
                enrollment_data["binding"].update({"clientStaffId": admin_id})
        if pin:
            enrollment_data["tokenRegistrationOptions"]["otpCredentialParams"].update(
                {"pin": pin, "pinFormat": pin_format}
            )
        enrollment_response = self.token_enrollment(enrollment_data, expected_code).json()
        if expected_code != 200:
            return enrollment_response
        enrollment_id = enrollment_response["enrollmentId"]
        uri = enrollment_response["request"]["qr"]
        secret_key = uri[((uri.find("secret=")) + 7):(uri.find("&issuer"))]
        if oath_type.lower() == "totp":
            otp = otp or pyotp.TOTP(secret_key, digits=digits, digest=algorithm[4:], interval=period).now()
            response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
            return {"response": response, "enrollment_id": enrollment_id}
        elif oath_type.lower() == "hotp":
            counter = int(uri[((uri.find("counter=")) + 8):])
            otp = otp or pyotp.HOTP(
                secret_key, digits=digits, digest=algorithm[4:], initial_count=counter
            ).at(counter + 1)
            response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
            return {"response": response, "enrollment_id": enrollment_id}
        elif oath_type.lower() == "ocra":
            challenge = enrollment_response["request"]["challenge"]
            otp = otp or self.ocra.generate_ocra(secret_key, challenge, algorithm=algorithm[4:])
            response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
            return {"response": response, "enrollment_id": enrollment_id}
        else:
            raise Exception(f"Invalid OATH type. Provided: {oath_type}. Can be TOTP, HOTP, OCRA")

    def add_google(
        self,
        name=("google_" + s.random_name()),
        pin=None,
        pin_format=None,
        user_id=None,
        admin_id=None,
        max_attempts=10,
        timeout_seconds=9999,
        request_body=None,
        expected_code=200,
        otp=None
    ):
        enrollment_data = (
            request_body
            if request_body
            else {
                "maxAttempts": max_attempts,
                "timeoutSeconds": timeout_seconds,
                "tokenRegistrationOptions": {
                    "name": name,
                    "type": self.token_type.software.GOOGLE,
                    "otpCredentialParams": {}
                },
            }
        )
        if user_id or admin_id:
            enrollment_data["binding"] = {}
            if user_id:
                enrollment_data["binding"].update({"userId": user_id})
            if admin_id:
                enrollment_data["binding"].update({"clientStaffId": admin_id})
        if pin:
            enrollment_data["tokenRegistrationOptions"]["otpCredentialParams"].update(
                {"pin": pin, "pinFormat": pin_format}
            )
        enrollment_response = self.token_enrollment(enrollment_data, expected_code).json()
        if expected_code != 200:
            return enrollment_response
        enrollment_id = enrollment_response["enrollmentId"]
        uri = enrollment_response["request"]["qr"]
        secret_key = uri[((uri.find("secret=")) + 7):(uri.find("&algorithm"))]
        otp = otp or pyotp.TOTP(secret_key).now()
        response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
        return {"response": response, "enrollment_id": enrollment_id}

    def add_mail(
        self,
        email=s.random_email(),
        name=("mail_" + s.random_name()),
        digits=6,
        pin=None,
        pin_format=None,
        user_id=None,
        admin_id=None,
        max_attempts=10,
        timeout_seconds=9999,
        request_body=None,
        expected_code=200,
        otp=None
    ):
        enrollment_data = (
            request_body
            if request_body
            else {
                "maxAttempts": max_attempts,
                "timeoutSeconds": timeout_seconds,
                "tokenRegistrationOptions": {
                    "name": name,
                    "type": self.token_type.software.MAIL,
                    "otpCredentialParams": {"digits": digits},
                    "deliverWith": {"mail": email},
                },
            }
        )
        if user_id or admin_id:
            enrollment_data["binding"] = {}
            if user_id:
                enrollment_data["binding"].update({"userId": user_id})
            if admin_id:
                enrollment_data["binding"].update({"clientStaffId": admin_id})
        if pin:
            enrollment_data["tokenRegistrationOptions"]["otpCredentialParams"].update(
                {"pin": pin, "pinFormat": pin_format}
            )
        enrollment_response = self.token_enrollment(enrollment_data, expected_code).json()
        if expected_code != 200:
            return enrollment_response
        enrollment_id = enrollment_response["enrollmentId"]
        otp_email = self.mailhog.get_last_mail_by_title_kind_and_target(
            self.mailhog.enum.TO, email, "Protectimus. OTP Authentication"
        )
        otp = otp or self.mailhog.get_otp_from_email(otp_email, digits)
        response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
        return {"response": response, "enrollment_id": enrollment_id}

    def add_sms(
        self,
        phone=s.random_phone(),
        name=("sms_" + s.random_name()),
        digits=6,
        pin=None,
        pin_format=None,
        user_id=None,
        admin_id=None,
        max_attempts=10,
        timeout_seconds=9999,
        request_body=None,
        expected_code=200,
        otp=None
    ):
        enrollment_data = (
            request_body
            if request_body
            else {
                "maxAttempts": max_attempts,
                "timeoutSeconds": timeout_seconds,
                "tokenRegistrationOptions": {
                    "name": name,
                    "type": self.token_type.software.SMS,
                    "otpCredentialParams": {"digits": digits},
                    "deliverWith": {"phoneNumber": phone},
                },
            }
        )
        if user_id or admin_id:
            enrollment_data["binding"] = {}
            if user_id:
                enrollment_data["binding"].update({"userId": user_id})
            if admin_id:
                enrollment_data["binding"].update({"clientStaffId": admin_id})
        if pin:
            enrollment_data["tokenRegistrationOptions"]["otpCredentialParams"].update(
                {"pin": pin, "pinFormat": pin_format}
            )
        enrollment_response = self.token_enrollment(enrollment_data, expected_code).json()
        if expected_code != 200:
            return enrollment_response
        enrollment_id = enrollment_response["enrollmentId"]
        otp = otp or self.sms.get_otp(phone)
        response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
        return {"response": response, "enrollment_id": enrollment_id}

    def add_bot(
        self,
        name=("bot_" + s.random_name()),
        messenger="telegram",
        digits=6,
        pin=None,
        pin_format=None,
        user_id=None,
        admin_id=None,
        max_attempts=10,
        timeout_seconds=9999,
        request_body=None,
        expected_code=200,
        otp=None
    ):
        enrollment_data = (
            request_body
            if request_body
            else {
                "maxAttempts": max_attempts,
                "timeoutSeconds": timeout_seconds,
                "tokenRegistrationOptions": {
                    "name": name,
                    "type": self.token_type.software.BOT,
                    "otpCredentialParams": {"digits": digits},
                    "deliverWith": {"platform": messenger.lower() if isinstance(messenger, str) else messenger},
                },
            }
        )
        if user_id or admin_id:
            enrollment_data["binding"] = {}
            if user_id:
                enrollment_data["binding"].update({"userId": user_id})
            if admin_id:
                enrollment_data["binding"].update({"clientStaffId": admin_id})
        if pin:
            enrollment_data["tokenRegistrationOptions"]["otpCredentialParams"].update(
                {"pin": pin, "pinFormat": pin_format}
            )
        enrollment_response = self.token_enrollment(enrollment_data, expected_code).json()
        if expected_code != 200:
            return enrollment_response
        enrollment_id = enrollment_response["enrollmentId"]
        otp = self.bot.get_otp(messenger.lower(), enrollment_response["serial"])
        response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
        return {"response": response, "enrollment_id": enrollment_id}

    def add_universal(
        self,
        name=("uni_" + s.random_name()),
        oath_type="totp",
        algorithm="HmacSHA256",
        issuer="Protectimus",
        period=30,
        digits=6,
        secret=None,
        secret_encode=None,
        serial=(s.random_name()),
        counter=256,
        validation_window=1,
        ocra_suite="OCRA-1:HOTP-SHA1-6:QN8",
        pin=None,
        pin_format=None,
        user_id=None,
        admin_id=None,
        max_attempts=10,
        timeout_seconds=9999,
        request_body=None,
        expected_code=200,
    ):
        enrollment_data = (
            request_body
            if request_body
            else {
                "maxAttempts": max_attempts,
                "timeoutSeconds": timeout_seconds,
                "tokenRegistrationOptions": {
                    "name": name,
                    "type": self.token_type.universal,
                    "otpCredentialParams": {
                        "issuer": issuer,
                        "type": oath_type.lower() if isinstance(oath_type, str) else oath_type,
                        "algorithm": algorithm,
                        "period": period,
                        "digits": digits,
                        "counter": counter,
                        "serialNumber": serial,
                        "validationWindow": validation_window,
                    },
                },
            }
        )
        if user_id or admin_id:
            enrollment_data["binding"] = {}
            if user_id:
                enrollment_data["binding"].update({"userId": user_id})
            if admin_id:
                enrollment_data["binding"].update({"clientStaffId": admin_id})
        if pin:
            enrollment_data["tokenRegistrationOptions"]["otpCredentialParams"].update(
                {"pin": pin, "pinFormat": pin_format}
            )
        if secret:
            enrollment_data["tokenRegistrationOptions"]["otpCredentialParams"].update(
                {"secret": secret, "secretEncoding": secret_encode}
            )
        enrollment_response = self.token_enrollment(enrollment_data, expected_code).json()
        if expected_code != 200:
            return enrollment_response
        enrollment_id = enrollment_response["enrollmentId"]
        uri = enrollment_response["request"]["qr"]
        secret_key = uri[((uri.find("secret=")) + 7):(uri.find("&issuer"))]
        if oath_type.lower() == "totp":
            otp = pyotp.TOTP(secret_key, digits=digits, digest=algorithm[4:], interval=period).now()
            response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
            return {"response": response, "enrollment_id": enrollment_id}
        elif oath_type.lower() == "hotp":
            otp = pyotp.HOTP(secret_key, digits=digits, digest=algorithm[4:], initial_count=counter).at(counter + 1)
            response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
            return {"response": response, "enrollment_id": enrollment_id}
        elif oath_type.lower() == "ocra":
            challenge = enrollment_response["request"]["challenge"]
            otp = self.ocra.generate_ocra(secret_key, challenge, ocra_suite, algorithm[4:], counter)
            response = self.finish_token_creation(enrollment_id, otp, expected_code).json()
            return {"response": response, "enrollment_id": enrollment_id}
        else:
            raise Exception(f"Invalid OATH type. Provided: {oath_type}. Can be TOTP, HOTP, OCRA")

    @allure.step("Send an API request to /api/request")
    def token_enrollment(self, enrollment_data, expected_code, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.enrollment,
            request_type or self.requests_type.POST,
            json=enrollment_data,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def finish_token_creation(self, enrollment_id, otp, expected_code, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.finish.format(enrollment_id=enrollment_id),
            request_type or self.requests_type.POST,
            json={"otp": otp},
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def get_token_creation_status(self, enrollment_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.status.format(enrollment_id=enrollment_id),
            request_type or self.requests_type.GET,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def get_token_creation_info(self, enrollment_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.enrollment_info.format(enrollment_id=enrollment_id),
            request_type or self.requests_type.GET,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def delete_token(self, token_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.by_id.format(token_id=token_id),
            request_type or self.requests_type.DELETE,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def block_token(self, token_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.block.format(token_id=token_id),
            request_type or self.requests_type.POST,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def unblock_token(self, token_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.unblock.format(token_id=token_id),
            request_type or self.requests_type.POST,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def activate_bypass(self, token_id, period=None, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.bypass_activate.format(token_id=token_id),
            request_type or self.requests_type.POST,
            params=f"period={period}" if period else None,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def deactivate_bypass(self, token_id, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.bypass_deactivate.format(token_id=token_id),
            request_type or self.requests_type.POST,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def rename_token(self, token_id, name, expected_code=200, request_type=None):
        response = self.make_request(
            self.endpoints.tokens.rename.format(token_id=token_id),
            request_type or self.requests_type.PATCH,
            data=name,
            expected_code=expected_code,
        )
        return response

    def check_otp(self, token_id, otp, timeout_seconds=300, max_attempts=10, request_body=None, expected_code=200):
        auth_response = (self.start_check_otp(token_id, timeout_seconds, max_attempts, request_body, expected_code)
                         .json())
        response = self.finish_check_otp(auth_response["authenticationId"], otp, expected_code).json()
        return response

    @allure.step("Send an API request to /api/request")
    def start_check_otp(
            self,
            token_id,
            timeout_seconds=300,
            max_attempts=10,
            request_body=None,
            expected_code=200,
            request_type=None
    ):
        data = (
            request_body
            if request_body
            else {"tokenId": token_id, "timeoutSeconds": timeout_seconds, "maxAttempts": max_attempts}
        )
        response = self.make_request(
            self.endpoints.tokens.auth,
            request_type or self.requests_type.POST,
            json=data,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def finish_check_otp(self, auth_id, otp, expected_code=200, request_type=None):
        data = {"otp": otp}
        response = self.make_request(
            self.endpoints.tokens.finish_auth.format(auth_id=auth_id),
            request_type or self.requests_type.POST,
            json=data,
            expected_code=expected_code,
        )
        return response

    @allure.step("Send an API request to /api/request")
    def sync_token(
        self,
        token_id,
        otp,
        challenge="",
        validation_window=10,
        request_body=None,
        expected_code=200,
        request_type=None
    ):
        data = (
            request_body
            if request_body
            else {"challenge": challenge, "validationWindow": validation_window, "otp": otp}
        )
        response = self.make_request(
            self.endpoints.tokens.sync.format(token_id=token_id),
            request_type or self.requests_type.POST,
            json=data,
            expected_code=expected_code,
        )
        return response
