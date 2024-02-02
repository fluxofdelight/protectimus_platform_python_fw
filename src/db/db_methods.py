from src.db.pages.tokens.tokens_page import TokensPageDB
from src.db.pages.users.users_page import UsersPageDB


class DatabaseMethods:
    def __init__(self):
        self.users = UsersPageDB()
        self.tokens = TokensPageDB()
