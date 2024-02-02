from attr import attrib, attrs

from src.common.enum_common.token_type import TokenType
from src.configs.config import Config


@attrs
class SuccessToken:
    token_id = attrib(default=None)
    name = attrib(default=None)
    type = attrib(default=None)  # tokens_db_to_api_format.get_api_token_type
    serial_number = attrib(default=None)
    creation_date = attrib(default=None)
    secret = attrib(default=None)
    counter = attrib(default=0)
    digits = attrib(default=6)
    ocra_question = attrib(default=None)
    ocra_token_activation_code = attrib(default=None)
    pin = attrib(default=None)
    pin_otp_format = attrib(default=None)
    enabled = attrib(default=True)
    disabled_until = attrib(default=None)
    last_otp = attrib(default=None)
    personal_token = attrib(default=False)
    status = attrib(default=None)
    failed_attempts = attrib(default=0)
    failed_sync_attempts = attrib(default=0)
    block = attrib(default="NONE_BLOCKED")  # tokens_db_to_api_format.get_api_block_type
    block_time = attrib(default=None)
    generations = attrib(default=0)
    color = attrib(default=None)
    user_id = attrib(default=None)
    username = attrib(default=None)
    client_staff_id = attrib(default=None)
    client_staff_username = attrib(default=None)
    creator_name = attrib(default=Config().api.api_login)
    creator_id = attrib(default=1)
    client_id = attrib(default=1)
    reserved_for_client_id = attrib(default=None)
    unify_token_type = attrib(default="OATH_TOTP")  # tokens_db_to_api_format.get_api_unify_token_type
    unify_key_algo = attrib(default="SHA256")  # tokens_db_to_api_format.get_api_unify_key_algo
    unify_key_format = attrib(default=None)  # get_api_unify_key_format
    prepare_auth_otp_time = attrib(default=None)
    unify_key_id = attrib(default=None)
    manufacturer = attrib(default=None)
    suite = attrib(default=None)
    time = attrib(default=0)
    time_drift = attrib(default=0)
    time_interval = attrib(default=None)
    validation_window = attrib(default=1)
    ocra_pin = attrib(default="NULL::character varying")
    # Have to be deleted
    secret_encoded = attrib(default=None)
    secret_not_encoded = attrib(default=False)
    counter_initialization = attrib(default=False)
    counter_sync = attrib(default=False)
    not_check_pin = attrib(default=False)
    failed_attempts_before_lock = attrib(default=0)
    check_failed_attempts = attrib(default=False)
    resource_id = attrib(default=None)
    sms_recipient = attrib(default=None)
    resending = attrib(default=False)
    response_encoding = attrib(default=None)
    response_check_digit = attrib(default=False)
    ocra_challenge_encoding = attrib(default=None)
    ocra_challenge_check_digit = attrib(default=False)
    min_ocra_challenge_size = attrib(default=0)
    max_ocra_challenge_size = attrib(default=0)
    ocra_pin_key_id = attrib(default=None)
    attributes = attrib(default={})

    @property
    def body(self):
        return {
            'id': self.token_id,
            'name': self.name,
            'type': self.type,
            'serial': self.serial_number,
            'creationDate': self.creation_date,
            'secret_key': self.secret,
            'counter': self.counter,
            'digits': self.digits,
            'ocraChallenge': self.ocra_question,
            'ocraActivationCode': self.ocra_token_activation_code,
            'pinCode': self.pin,
            'pinFormat': self.pin_otp_format,
            'enabled': self.enabled,
            'disabledUntil': self.disabled_until,
            'lastOtp': self.last_otp,
            'personal': self.personal_token,
            'status': self.status,
            'failedAttempts': self.failed_attempts,
            'failedSynchronizationAttempts': self.failed_sync_attempts,
            'block': self.block,
            'blockTime': self.block_time,
            'generations': self.generations,
            'color': self.color,
            'userId': self.user_id,
            'username': self.username,
            'staffId': self.client_staff_id,
            'staffUsername': self.client_staff_username,
            'creatorName': self.creator_name,
            'creatorId': self.creator_id,
            'clientId': self.client_id,
            'reservedForClient': self.reserved_for_client_id,
            'unifyType': self.unify_token_type,
            'unifyKeyAlgo': self.unify_key_algo,
            'unifyKeyFormat': self.unify_key_format,
            'prepareAuthTime': self.prepare_auth_otp_time,
            'unifyKeyId': self.unify_key_id,
            'manufacturer': self.manufacturer,
            'suite': self.suite,
            'time': self.time,
            'timeDrift': self.time_drift,
            'period': self.time_interval,
            'validationWindows': self.validation_window,
            'ocraPinCode': self.ocra_pin,
            'secretEncode': self.secret_encoded,
            'secretNotEncode': self.secret_not_encoded,
            'counterInitializ': self.counter_initialization,
            'counterSync': self.counter_sync,
            'notCheckPinCode': self.not_check_pin,
            'failedAttemptsBeforeLocked': self.failed_attempts_before_lock,
            'checkFailedAttemptsNumber': self.check_failed_attempts,
            'resourceId': self.resource_id,
            'smsRecipientId': self.sms_recipient,
            'resendingOtp': self.resending,
            'responseEncodingType': self.response_encoding,
            'responseCheckDigits': self.response_check_digit,
            'ocraChallengeCheckDigits': self.ocra_challenge_check_digit,
            'ocraChallengeEncodingType': self.ocra_challenge_encoding,
            'minOcraChallenge': self.min_ocra_challenge_size,
            'maxOcraChallenge': self.max_ocra_challenge_size,
            'ocraPinKey': self.ocra_pin_key_id,
            'attributes': self.attributes
        }


@attrs
class SuccessEnrollmentSmart:
    enrollment_id = attrib(default=None)
    message = attrib(default='Download the Protectimus Smart OTP app ...')
    request = attrib(default={"qr": "{qr}"})
    serial_number = attrib(default=None)
    token_type = attrib(default=TokenType.software.SMART)

    @property
    def body(self):
        return {
            'enrollmentId': self.enrollment_id,
            'message': self.message,
            'request': self.request,
            'serialNumber': self.serial_number,
            'tokenType': self.token_type
        }


@attrs
class SuccessEnrollmentGoogle:
    enrollment_id = attrib(default=None)
    message = attrib(default='Download the Google Authenticator app ...')
    request = attrib(default={"qr": "{qr}"})
    serial_number = attrib(default=None)
    token_type = attrib(default=TokenType.software.GOOGLE)

    @property
    def body(self):
        return {
            'enrollmentId': self.enrollment_id,
            'message': self.message,
            'request': self.request,
            'serialNumber': self.serial_number,
            'tokenType': self.token_type
        }


@attrs
class SuccessEnrollmentMail:
    enrollment_id = attrib(default=None)
    message = attrib(default='Enter the OTP code that was sent to {email}')
    request = attrib(default={})
    serial_number = attrib(default="{email}")
    token_type = attrib(default=TokenType.software.MAIL)

    @property
    def body(self):
        return {
            'enrollmentId': self.enrollment_id,
            'message': self.message,
            'request': self.request,
            'serialNumber': self.serial_number,
            'tokenType': self.token_type
        }


@attrs
class SuccessEnrollmentSms:
    enrollment_id = attrib(default=None)
    message = attrib(default='Enter the OTP code that was sent to {phone}')
    request = attrib(default={})
    serial_number = attrib(default="{phone}")
    token_type = attrib(default=TokenType.software.SMS)

    @property
    def body(self):
        return {
            'enrollmentId': self.enrollment_id,
            'message': self.message,
            'request': self.request,
            'serialNumber': self.serial_number,
            'tokenType': self.token_type
        }


@attrs
class SuccessEnrollmentBot:
    enrollment_id = attrib(default=None)
    message = attrib(default='Scan the QR code above to register bot authenticator')
    request = attrib(default={"qr": "{qr}"})
    serial_number = attrib(default=None)
    token_type = attrib(default=TokenType.software.BOT)

    @property
    def body(self):
        return {
            'enrollmentId': self.enrollment_id,
            'message': self.message,
            'request': self.request,
            'serialNumber': self.serial_number,
            'tokenType': self.token_type
        }


@attrs
class SuccessEnrollmentUniversal:
    enrollment_id = attrib(default=None)
    message = attrib(default='Open your authentication app and scan the QR code above')
    request = attrib(default={"qr": "{qr}"})
    serial_number = attrib(default=None)
    token_type = attrib(default=TokenType.universal)

    @property
    def body(self):
        return {
            'enrollmentId': self.enrollment_id,
            'message': self.message,
            'request': self.request,
            'serialNumber': self.serial_number,
            'tokenType': self.token_type
        }


@attrs
class SuccessEnrollmentFinish:
    error_message = attrib(default=None)
    succeeded = attrib(default=True)
    token_id = attrib(default=None)

    @property
    def body(self):
        return {
            'errorMessage': self.error_message,
            'succeeded': self.succeeded,
            'tokenId': self.token_id
        }


@attrs
class InvalidOtpEnrollmentFinish:
    error_message = attrib(default="Invalid otp")
    succeeded = attrib(default=False)
    token_id = attrib(default=None)

    @property
    def body(self):
        return {
            'errorMessage': self.error_message,
            'succeeded': self.succeeded,
            'tokenId': self.token_id
        }


@attrs
class SuccessEnrollmentStatus:
    status = attrib(default="SUCCEEDED")
    result = attrib(default="SUCCEEDED")

    @property
    def body(self):
        return {
            'status': self.status,
            'result': self.result
        }


@attrs
class PendingEnrollmentStatus:
    status = attrib(default="STARTED")
    result = attrib(default="PENDING")

    @property
    def body(self):
        return {
            'status': self.status,
            'result': self.result
        }


@attrs
class FailedEnrollmentStatus:
    status = attrib(default="FAILED")
    result = attrib(default="FAILED")

    @property
    def body(self):
        return {
            'status': self.status,
            'result': self.result
        }


@attrs
class SuccessEnrollmentInfo:
    enrollment_id = attrib(default=None)
    status = attrib(default="SUCCEEDED")
    result = attrib(default="SUCCEEDED")
    client_id = attrib(default=1)
    client_staff_id = attrib(default=1)
    started_at = attrib(default=None)
    finished_at = attrib(default=None)
    token_id = attrib(default=None)

    @property
    def body(self):
        return {
            'id': self.enrollment_id,
            'status': self.status,
            'result': self.result,
            'clientId': self.client_id,
            'clientStaffId': self.client_staff_id,
            'startedAt': self.started_at,
            'finishedAt': self.finished_at,
            'enrolledTokenId': self.token_id
        }


@attrs
class FailedEnrollmentInfo:
    enrollment_id = attrib(default=None)
    status = attrib(default="FAILED")
    result = attrib(default="FAILED")
    client_id = attrib(default=1)
    client_staff_id = attrib(default=1)
    started_at = attrib(default=None)
    finished_at = attrib(default=None)
    token_id = attrib(default=None)

    @property
    def body(self):
        return {
            'id': self.enrollment_id,
            'status': self.status,
            'result': self.result,
            'clientId': self.client_id,
            'clientStaffId': self.client_staff_id,
            'startedAt': self.started_at,
            'finishedAt': self.finished_at,
            'enrolledTokenId': self.token_id
        }


@attrs
class SuccessStartCheckOtpSmart:
    auth_id = attrib(default=None)
    message = attrib(default='Enter OTP code from your Protectimus Smart app')
    request = attrib(default={})
    token_type = attrib(default=TokenType.software.SMART)

    @property
    def body(self):
        return {
            'authenticationId': self.auth_id,
            'message': self.message,
            'request': self.request,
            'tokenType': self.token_type
        }


@attrs
class SuccessStartCheckOtpSmartOcra:
    auth_id = attrib(default=None)
    message = attrib(default='Enter OTP code from your Protectimus Smart app')
    request = attrib(default={'challenge': "{challenge}"})
    token_type = attrib(default=TokenType.software.SMART)

    @property
    def body(self):
        return {
            'authenticationId': self.auth_id,
            'message': self.message,
            'request': self.request,
            'tokenType': self.token_type
        }


@attrs
class SuccessStartCheckOtpGoogle:
    auth_id = attrib(default=None)
    message = attrib(default='Enter OTP code from your Google Authenticator app')
    request = attrib(default={})
    token_type = attrib(default=TokenType.software.GOOGLE)

    @property
    def body(self):
        return {
            'authenticationId': self.auth_id,
            'message': self.message,
            'request': self.request,
            'tokenType': self.token_type
        }


@attrs
class SuccessStartCheckOtpMail:
    auth_id = attrib(default=None)
    message = attrib(default='Enter the OTP code that was sent to {email}')
    request = attrib(default={})
    token_type = attrib(default=TokenType.software.MAIL)

    @property
    def body(self):
        return {
            'authenticationId': self.auth_id,
            'message': self.message,
            'request': self.request,
            'tokenType': self.token_type
        }


@attrs
class SuccessStartCheckOtpSms:
    auth_id = attrib(default=None)
    message = attrib(default='Enter the OTP code that was sent to {phone}')
    request = attrib(default={})
    token_type = attrib(default=TokenType.software.SMS)

    @property
    def body(self):
        return {
            'authenticationId': self.auth_id,
            'message': self.message,
            'request': self.request,
            'tokenType': self.token_type
        }


@attrs
class SuccessStartCheckOtpBot:
    auth_id = attrib(default=None)
    message = attrib(default='Enter OTP code from your bot authenticator')
    request = attrib(default={})
    token_type = attrib(default=TokenType.software.BOT)

    @property
    def body(self):
        return {
            'authenticationId': self.auth_id,
            'message': self.message,
            'request': self.request,
            'tokenType': self.token_type
        }


@attrs
class SuccessStartCheckOtpUniversal:
    auth_id = attrib(default=None)
    message = attrib(default='Enter OTP code from your Authenticator app')
    request = attrib(default={})
    token_type = attrib(default=TokenType.universal)

    @property
    def body(self):
        return {
            'authenticationId': self.auth_id,
            'message': self.message,
            'request': self.request,
            'tokenType': self.token_type
        }


@attrs
class SuccessStartCheckOtpPush:
    auth_id = attrib(default=None)
    message = attrib(default='Approve access using your Protectimus Smart app')
    request = attrib(default={})
    token_type = attrib(default=TokenType.software.PUSH)

    @property
    def body(self):
        return {
            'authenticationId': self.auth_id,
            'message': self.message,
            'request': self.request,
            'tokenType': self.token_type
        }


@attrs
class SuccessFinishCheckOtp:
    succeeded = attrib(default=True)
    error_message = attrib(default=None)

    @property
    def body(self):
        return {
            'succeeded': self.succeeded,
            'errorMessage': self.error_message
        }


@attrs
class ErrorFinishCheckOtp:
    succeeded = attrib(default=False)
    error_message = attrib(default='Invalid otp')

    @property
    def body(self):
        return {
            'succeeded': self.succeeded,
            'errorMessage': self.error_message
        }
