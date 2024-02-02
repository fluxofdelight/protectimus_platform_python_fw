from typing import Optional

from requests import Session

from src.api.endpoints.pages.mailhog import MailhogEndpoints
from src.common.enum_common.mailhog import MailhogKindEnum


class Mailhog:
    def __init__(self, session: Optional[Session], config):
        self.session = session or Session()
        self.endpoints = MailhogEndpoints(config)
        self.enum = MailhogKindEnum

    def search_messages_by(self, kind: MailhogKindEnum, target: str, start=0, limit=10):
        params = {"kind": kind, "query": target, "start": start, "limit": limit}
        response = self.session.get(self.endpoints.search, params=params)
        assert response.status_code == 200
        return response.json()["items"]

    @staticmethod
    def get_body_from_mail(mail):
        return mail["Content"]["Body"]

    def get_certain_mail_by_title_kind_and_target(self, kind, target, title, raise_if_not_found=True):
        mail_list = self.search_messages_by(kind=kind, target=target)
        mails = [mail for mail in mail_list if mail["title"] == title]
        if len(mails) == 1:
            return mails[0]
        elif len(mails) == 0:
            if not raise_if_not_found:
                return None
            else:
                raise Exception(
                    f"Empty result at searching emails in mailhog with params [{kind} {target} with title - {title}]"
                )
        else:
            raise Exception(f"Expected len of results - 1. Actual len - [{len(mails)}]. Mailhog result - [{mails}]")

    def get_last_mail_by_title_kind_and_target(self, kind, target, title, raise_if_not_found=True):
        mail_list = self.search_messages_by(kind=kind, target=target)
        mails = [mail for mail in mail_list if title in mail["Content"]["Headers"]["Subject"]]
        mails.sort(key=lambda mail: mail["Created"])
        if mails:
            return mails[-1]
        else:
            if not raise_if_not_found:
                return None
            else:
                raise Exception(
                    f"Empty result at searching emails in mailhog with params [{kind} {target} with title - {title}]"
                )

    def get_otp_from_email(self, mail, otp_length=6):
        body = self.get_body_from_mail(mail)
        index = (body.find("<b><u>")) + 6
        otp = body[index:(index + 6 if otp_length == 6 else index + 8)]
        return otp
