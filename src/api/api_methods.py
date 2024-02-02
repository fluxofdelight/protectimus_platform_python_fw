from requests import Session

from src.api.pages.auth.auth import Auth
from src.api.pages.tokens.tokens import Tokens
from src.api.pages.users.users import Users


class ApiMethods:
    def __init__(self, config, session=None):
        self.session = session or Session()
        self.auth = Auth(self.session, config)
        self.users = Users(self.session, config)
        self.tokens = Tokens(self.session, config)
