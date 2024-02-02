import pytest

from src.ui.pages.home.home_signed_in import HomeSignedIn


@pytest.fixture(scope="session", autouse=True)
def basic_login(driver):
    return


@pytest.fixture(scope="class", autouse=True)
def home_signed_in_page(driver):
    yield HomeSignedIn(driver)
