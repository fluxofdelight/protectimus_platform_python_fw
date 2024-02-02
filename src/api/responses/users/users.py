from attr import attrib, attrs

from src.common.enum_common.block_type import BlockType
from src.configs.config import Config


@attrs
class SuccessUser:
    user_id = attrib(default=None)
    user_type = attrib(default="USER")
    login = attrib(default=None)
    alias = attrib(default=None)
    password = attrib(default="**********")
    email = attrib(default=None)
    phone = attrib(default=None)
    first_name = attrib(default="John")
    last_name = attrib(default="Doe")
    login_failed_attempts = attrib(default=0)
    otp_failed_attempts = attrib(default=0)
    email_failed_attempts = attrib(default=0)
    pin_failed_attempts = attrib(default=0)
    block = attrib(default=BlockType.NONE_BLOCKED)
    block_time = attrib(default=None)
    has_tokens = attrib(default=False)
    client_id = attrib(default=1)
    creator_name = attrib(default=Config().api.api_login)
    creator_id = attrib(default=1)
    hash_ = attrib(default=None)
    hash_env = attrib(default=None)
    password_encoding_type = attrib(default=None)
    password_encoding_format = attrib(default=None)
    sent_sms_number = attrib(default=0)
    sms_prepare_time = attrib(default=None)

    @property
    def body(self):
        return {
            'id': self.user_id,
            'type': self.user_type,
            'login': self.login,
            'alias': self.alias,
            'password': self.password,
            'email': self.email,
            'phone': self.phone,
            'firstName': self.first_name,
            'secondName': self.last_name,
            'loginFailedAttempts': self.login_failed_attempts,
            'otpFailedAttempts': self.otp_failed_attempts,
            'emailFailedAttempts': self.email_failed_attempts,
            'pinFailedAttempts': self.pin_failed_attempts,
            'block': self.block,
            'blockTime': self.block_time,
            'hasToken': self.has_tokens,
            'client': self.client_id,
            'creator': self.creator_name,
            'creatorId': self.creator_id,
            'hash': self.hash_,
            'userEnv': self.hash_env,
            'passwordEncodeType': self.password_encoding_type,
            'passwordEncodeFormat': self.password_encoding_format,
            'sentSms': self.sent_sms_number,
            'smsPrepareOtpTime': self.sms_prepare_time
        }
