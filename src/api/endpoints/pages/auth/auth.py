from attr import attrs

from src.api.endpoints.base import BaseEndpoints


@attrs
class AuthEndpoints(BaseEndpoints):
    def __attrs_post_init__(self):
        self.default = self.base_url + "a"
        self.login = self.default + "/login"
        self.auth_me = self.default + "/me"
        self.binding = self.default + "/bind"
        self.assign = self.binding + "/assign"
        self.revoke = self.binding + "/revoke"
