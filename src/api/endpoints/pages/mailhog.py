from attr import Factory, attrib, attrs, validators

from src.configs.config import MailhogConfig


@attrs
class MailhogEndpoints:
    configs: MailhogConfig = attrib(validator=validators.instance_of(MailhogConfig))
    base_url = attrib(default=Factory(lambda self: self.configs.base_url, takes_self=True))

    def __attrs_post_init__(self):
        self.search = self.base_url + "api/v2/search"
        self.messages = self.base_url + "api/v2/messages"
