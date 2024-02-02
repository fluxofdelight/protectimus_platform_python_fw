from src.api.endpoints.pages.auth.auth import AuthEndpoints
from src.api.endpoints.pages.tokens.tokens import TokensEndpoints
from src.api.endpoints.pages.users.users import UsersEndpoints


class ApiEndpoints:
    def __init__(self, config):
        self.auth = AuthEndpoints(config)
        self.users = UsersEndpoints(config)
        self.tokens = TokensEndpoints(config)
