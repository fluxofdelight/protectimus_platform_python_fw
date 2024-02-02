from attr import attrs

from src.api.endpoints.base import BaseEndpoints


@attrs
class TokensEndpoints(BaseEndpoints):
    def __attrs_post_init__(self):
        self.default = self.base_url + "t"
        self.by_id = self.default + "/{token_id}"

        self.enrollment = self.default + "/enroll"
        self.enrollment_info = self.enrollment + "/enrollment_id"
        self.cancel = self.enrollment + "/cancel"
        self.finish = self.enrollment + "/{enrollment_id}/finish"
        self.status = self.enrollment + "/{enrollment_id}/status"

        self.block = self.by_id + "/disable"
        self.unblock = self.by_id + "/enable"
        self.bypass_activate = self.by_id + "/pass/activate"
        self.bypass_deactivate = self.by_id + "/pass/deactivate"
        self.rename = self.by_id + "/name"

        self.count_total = self.default + "/count"
        self.auth = self.default + "/auth"
        self.finish_auth = self.auth + "/{auth_id}/finish"
        self.sync = self.by_id + "/sync"
