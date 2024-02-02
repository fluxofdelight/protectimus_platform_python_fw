import base64
import binascii
import datetime
import hashlib
import hmac

from pyotp import TOTP


class OCRA:
    def __init__(self):
        self.DIGITS_POWER = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
        self.totp = TOTP

    @staticmethod
    def hmac_(crypto, key_bytes, text):
        try:
            hmac_hash = hmac.new(key_bytes, text, getattr(hashlib, crypto))
            return hmac_hash.digest()
        except Exception as e:
            raise e

    @staticmethod
    def get_time_step_info_from_ocra_suite(ocra_suite):
        if "-T" in ocra_suite or ":T" in ocra_suite:
            time_info_index = ocra_suite.find("-T")
            if time_info_index < 0:
                time_info_index = ocra_suite.find(":T")
            return ocra_suite[time_info_index + 1:]
        else:
            return None

    def get_time_step(self, secret, ocra_suite):
        time_info = self.get_time_step_info_from_ocra_suite(ocra_suite)
        if time_info:
            interval = int(time_info[1])
            unit = time_info[2]
            if unit.upper() == "S":
                time_step = self.totp(secret, interval=interval).timecode(datetime.datetime.now())
                return time_step
            elif unit.upper() == "M":
                interval = interval * 60
                time_step = self.totp(secret, interval=interval).timecode(datetime.datetime.now())
                return time_step
            elif unit.upper() == "M":
                interval = (interval * 60) * 60
                time_step = self.totp(secret, interval=interval).timecode(datetime.datetime.now())
                return time_step
            else:
                raise Exception("Invalid unit. Can be S, M, or H")
        else:
            return None

    def generate_ocra(  # noqa: C901
        self,
        secret_key,
        challenge: str,
        ocra_suite="OCRA-1:HOTP-SHA1-6:QN8",
        algorithm=None,
        counter="",
        session_information="",
        time_step=None,
    ):
        time_step = time_step if time_step else self.get_time_step(secret_key.upper(), ocra_suite)
        ocra_suite = ocra_suite.upper()
        challenge = binascii.hexlify(challenge.encode()).decode()
        code_digits = int(ocra_suite.split("-")[3].split(":")[0])
        try:
            secret_bytes = bytes.fromhex(secret_key.upper())
        except ValueError:
            secret_key = base64.b32decode(secret_key.upper()).hex()
            secret_bytes = bytes.fromhex(secret_key)
        if algorithm and "SHA1" in ocra_suite:
            if algorithm.upper() == "SHA1":
                crypto = "sha1"
            elif algorithm.upper() == "SHA256":
                ocra_suite.replace("SHA1", "SHA256")
                crypto = "sha256"
            elif algorithm.upper() == "SHA512":
                ocra_suite.replace("SHA1", "SHA512")
                crypto = "sha512"
            else:
                raise ValueError("Couldn't determine crypto algorithm")
        else:
            if "HOTP-SHA1" in ocra_suite:
                crypto = "sha1"
            elif "HOTP-SHA256" in ocra_suite:
                crypto = "sha256"
            elif "HOTP-SHA512" in ocra_suite:
                crypto = "sha512"
            else:
                raise ValueError("Couldn't determine crypto algorithm in the specified OCRA-suite")
        ocra_suite_length = len(ocra_suite.encode())
        counter_length = 0
        challenge_length = 0
        password_length = 0
        session_information_length = 0
        time_stamp_length = 0
        password = ""
        time_step_hex = None
        if ":C" in ocra_suite:
            counter = counter.zfill(16)
            counter_length = 8
        if (":Q" in ocra_suite) or ("-Q" in ocra_suite):
            challenge = challenge.ljust(256, "0")
            challenge_length = 128
        if (":P" in ocra_suite) or ("-P" in ocra_suite):
            if "PSHA256" in ocra_suite:
                password_length = 32
            elif "PSHA512" in ocra_suite:
                password_length = 64
            else:
                password_length = 20
            password = password.zfill(password_length * 2)
        if (":S" in ocra_suite.split("SHA")[1]) or ("-S" in ocra_suite.split("SHA")[1]):
            session_information = session_information.zfill(128)
            session_information_length = 64
        if time_step:
            time_step_hex = hex(time_step)[2:].zfill(16)
            time_stamp_length = 8
        b_array = ocra_suite.encode()
        msg = bytearray(
            ocra_suite_length
            + counter_length
            + challenge_length
            + password_length
            + session_information_length
            + time_stamp_length
            + 1
        )
        msg[:len(b_array)] = b_array
        msg[len(b_array)] = 0x00
        if counter_length > 0:
            b_array = bytearray.fromhex(counter)
            for i in range(len(b_array)):
                msg[i + len(b_array) + 1] = b_array[i]
        if len(challenge) > 0:
            b_array = bytearray.fromhex(challenge)
            for i in range(len(b_array)):
                msg[i + ocra_suite_length + 1 + counter_length] = b_array[i]
        if password and password_length > 0:
            b_array = bytearray.fromhex(password)
            for i in range(len(b_array)):
                msg[i + ocra_suite_length + 1 + counter_length + challenge_length] = b_array[i]
        if session_information_length > 0:
            b_array = bytearray.fromhex(session_information)
            for i in range(min(128, len(b_array))):
                msg[i + ocra_suite_length + 1 + counter_length + challenge_length + password_length] = b_array[i]
        if time_step_hex and time_stamp_length > 0:
            b_array = bytearray.fromhex(time_step_hex)
            for i in range(min(8, len(b_array))):
                msg[
                    i
                    + ocra_suite_length
                    + 1
                    + counter_length
                    + challenge_length
                    + password_length
                    + session_information_length
                ] = b_array[i]
        hash_result = self.hmac_(crypto, secret_bytes, msg)
        offset = hash_result[-1] & 0xF
        binary = (
            ((hash_result[offset + 0] & 0x7F) << 24)
            | ((hash_result[offset + 1] & 0xFF) << 16)
            | ((hash_result[offset + 2] & 0xFF) << 8)
            | (hash_result[offset + 3] & 0xFF)
        )
        otp = binary % self.DIGITS_POWER[code_digits]
        result = str(otp).zfill(code_digits)
        return result
