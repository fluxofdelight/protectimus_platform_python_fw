from attr import Factory, attrib, attrs, validators

from src.configs.config import ApiConfig


@attrs
class BaseEndpoints:
    configs: ApiConfig = attrib(validator=validators.instance_of(ApiConfig))
    base_url = attrib(default=Factory(lambda self: self.configs.api_url + "api/v1/", takes_self=True))
