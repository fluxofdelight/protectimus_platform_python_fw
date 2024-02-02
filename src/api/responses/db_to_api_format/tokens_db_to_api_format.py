block_type = {
    "NONE_BLOCKED": 0,
    "BLOCKED_BY_ADMIN": 1,
}

token_type = {
    "TOKEN_1": 0,
    "TOKEN_2": 1,
    "TOKEN_3": 2,
    "TOKEN_4": 3,
    "TOKEN_5": 4,
    "TOKEN_6": 5,
    "TOKEN_7": 6,
    "TOKEN_8": 7,
    "TOKEN_9": 8,
    "TOKEN_10": 9,
    "TOKEN_11": 10,
    "TOKEN_12": 11,
    "TOKEN_13": 12,
    "TOKEN_14": 13,
    "TOKEN_15": 14,
    "TOKEN_16": 15,
    "TOKEN_17": 16
}

unify_token_type = {
    "OATH_HOTP": 0,
    "OATH_TOTP": 1,
    "OATH_OCRA": 2
}

unify_key_algo = {
    "SHA1": 0,
    "SHA256": 1,
    "SHA512": 2
}

unify_key_format = {
    "HEX": 0,
    "BASE32": 1,
    "BASE64": 2
}

pin_format = {
    "PIN_BEFORE_OTP": 0,
    "PIN_AFTER_OTP": 1
}


def get_api_value(_dict, db_value):
    if db_value not in _dict.values():
        return None
    else:
        for api, db in _dict.items():
            if db == db_value:
                return api


def get_api_block_type(db_value):
    return get_api_value(block_type, db_value)


def get_api_token_type(db_value):
    return get_api_value(token_type, db_value)


def get_api_unify_token_type(db_value):
    return get_api_value(unify_token_type, db_value)


def get_api_unify_key_algo(db_value):
    return get_api_value(unify_key_algo, db_value)


def get_api_unify_key_format(db_value):
    return get_api_value(unify_key_format, db_value)


def get_api_pin_format(db_value):
    return get_api_value(pin_format, db_value)


def get_db_value(_dict, api_value):
    if api_value not in _dict.keys():
        return None
    else:
        for api, db in _dict.items():
            if api == api_value:
                return db


def get_db_pin_format(api_value):
    return get_db_value(pin_format, api_value)
