from attr import attrs

from src.api.endpoints.base import BaseEndpoints


@attrs
class UsersEndpoints(BaseEndpoints):
    def __attrs_post_init__(self):
        self.default = self.base_url + "u"
        self.by_id = self.default + "/{user_id}"
        self.block = self.by_id + "/disable"
        self.unblock = self.by_id + "/enable"
        self.count_total = self.default + "/count"
