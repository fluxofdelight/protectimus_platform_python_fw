from datetime import datetime, timezone

from attr import attrib, attrs

from common.enum_common.http_errors import HttpErrors


# noqa
def contains_in_http_errors_enum_validator(instance, attribute, value: str):
    assert value in HttpErrors


@attrs
class ErrorResponse:
    error = attrib(validator=contains_in_http_errors_enum_validator,
                   on_setattr=contains_in_http_errors_enum_validator)
    # Shortened timestamp because of the difference in seconds
    timestamp = attrib(default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"))
    status: int = attrib(default=None)
    message = attrib(default="")
    path = attrib(default=None)

    @property
    def body(self):
        return {
            'timestamp': self.timestamp,
            'status': self.status,
            'error': self.error,
            'message': self.message,
            'path': self.path
        }
