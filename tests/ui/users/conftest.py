import pytest

from src.common.entry_data import EntryData
from src.db.pages.users.users_page import UsersPageDB
from src.ui.locators.users.users_page_locators import UsersPageLocators
from src.ui.pages.users.user_info_page import UserInfoPage
from src.ui.pages.users.users_page import UsersPage


@pytest.fixture(scope="class", autouse=True)
def users_page(driver):
    yield UsersPage(driver)


@pytest.fixture(scope="class", autouse=True)
def users_page_locators():
    yield UsersPageLocators()


@pytest.fixture(scope="class", autouse=True)
def user_info_page(driver):
    yield UserInfoPage(driver)


@pytest.fixture(scope="class", autouse=True)
def db():
    yield UsersPageDB()


@pytest.fixture(scope="class", autouse=True)
def entry_data():
    yield EntryData()


@pytest.fixture(scope="class", autouse=True)
def open_users_page(global_):
    yield global_.open_users_page()
