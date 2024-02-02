from attr import attrib, attrs

from src.configs.config import Config


@attrs
class SuccessLogin:
    access_token = attrib(default=None)
    refresh_token = attrib(default=None)

    @property
    def body(self):
        return {
            'access': self.access_token,
            'refresh': self.refresh_token
        }


@attrs
class SuccessAuthMe:
    user_id = attrib(default=1)
    auth_source = attrib(default="staff")
    client_id = attrib(default=1)
    login = attrib(default=Config().api.api_login)
    roles = attrib(default=[])
    company = attrib(default=None)

    @property
    def body(self):
        return {
            'userId': self.user_id,
            'authSource': self.auth_source,
            'clientId': self.client_id,
            'login': self.login,
            'companyName': self.company
        }
