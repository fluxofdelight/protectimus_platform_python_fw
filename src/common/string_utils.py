import math
import random
import string


def random_email(email_len=10, domain: str = "protectimus.com", negative=False):
    email_len = (100 - (len(domain) + 1)) if str(email_len).lower() == "max" else email_len
    s = string.ascii_lowercase
    r_num = random.randint(1, 999)
    if 1 <= email_len < 4:
        r_s = "".join(random.choice(s) for i in range(email_len))
        email = r_s + domain
    elif email_len <= 0:
        raise Exception("Length cannot be <= 0")
    elif (email_len + len(domain)) > 100 and not negative:
        raise Exception(f"Email length cannot be > 100. Current length: {email_len + len(domain)}")
    else:
        r_s = "".join(random.choice(s) for i in range(email_len - len(str(r_num))))
        email = f"{r_s}{str(r_num)}@{domain}"

    return email


def random_password(pass_len=16, negative=False):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    sp_symbols = "~!@#$%^&*()_+-=,./?*|"
    password = ""

    if pass_len < 6 and not negative:
        raise Exception("Min length is 6")
    elif pass_len > 100 and not negative:
        raise Exception("That's too big. Max length is 100")
    else:
        for i in range(math.ceil(pass_len / 4)):
            r_num = random.randint(0, 9)
            r_lower = "".join(random.choice(lower))
            r_upper = "".join(random.choice(upper))
            r_sp = "".join(random.choice(sp_symbols))
            password += str(r_num) + r_lower + r_sp + r_upper

    return password[:pass_len]


def random_name(name_len=8):
    s = "".join(random.choice(string.ascii_lowercase) for i in range(name_len))
    name = str(random.randint(0, 999)) + s

    return name[:name_len]


def random_phone(phone_len=None, with_plus=False):
    """
    :param phone_len: if None - will create with random length from 10 to 15
    :param with_plus: add + at the beginning
    """
    if phone_len:
        phone = ("+" if with_plus else "") + ''.join(random.choice(string.digits) for i in range(phone_len))
        return phone
    else:
        phone = (("+" if with_plus else "") + ''.join(
            random.choice(string.digits) for i in range(random.randint(10, 15))
        ))
        return phone
