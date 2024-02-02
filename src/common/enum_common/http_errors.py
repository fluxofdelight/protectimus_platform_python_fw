from common.enum_common.base_enum import EnumMetaclass


class HttpErrors(metaclass=EnumMetaclass):

    bad_request = "Bad Request"
    unauthorized = "Unauthorized"
    forbidden = "Forbidden"
    not_found = "Not Found"
    method_not_allowed = "Method Not Allowed"
    request_timeout = "Request Timeout"
    unsupported_media = "Unsupported Media Type"
    too_many_requests = "Too Many Requests"

    internal_server = "Internal Server Error"
    not_implemented = "Not Implemented"
    bad_gateway = "Bad Gateway"
    service_unavailable = "Service Unavailable"

    __all__ = [bad_request, unauthorized, forbidden, not_found, method_not_allowed, request_timeout,
               unsupported_media, too_many_requests, internal_server, not_implemented, bad_gateway, too_many_requests]

    code_to_error = {
        400: bad_request,
        401: unauthorized,
        403: forbidden,
        404: not_found,
        405: method_not_allowed,
        408: request_timeout,
        415: unsupported_media,
        429: too_many_requests,
        500: internal_server,
        501: not_implemented,
        502: bad_gateway,
        503: service_unavailable
    }

    def get_error_from_code(self, expected_code):
        if expected_code not in self.code_to_error.keys():
            raise Exception(f"Unknown status code. Provided: {expected_code}. Available: {self.code_to_error.keys()}")
        else:
            for code, error in self.code_to_error.items():
                if code == expected_code:
                    return error
