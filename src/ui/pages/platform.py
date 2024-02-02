from src.ui.pages.home.home_signed_out import HomeSignedOut
from src.ui.pages.resources.resources_page import ResourcesPage
from src.ui.pages.users.users_page import UsersPage


class Platform:
    def __init__(self, driver):
        self.login = HomeSignedOut(driver)
        self.registration = HomeSignedOut(driver)
        self.users = UsersPage(driver)
        self.resources = ResourcesPage(driver)
