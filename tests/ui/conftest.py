import time

import pytest

from src.ui.driver.driver import Driver
from src.ui.pages.global_ import Global
from src.ui.pages.home.home_signed_out import HomeSignedOut
from src.ui.pages.platform import Platform


@pytest.fixture(scope="session", autouse=True)
def driver(project_config):
    project_driver: Driver = Driver.start_from_configs(project_config)
    yield project_driver
    project_driver.quit()


@pytest.fixture(scope="session", autouse=True)
def platform(driver):
    yield Platform(driver)


@pytest.fixture(scope="session", autouse=True)
def basic_login(platform, project_config):
    platform.login.login(project_config.web.email, project_config.web.password)


@pytest.fixture(scope="function")
def refresh_page(driver):
    driver.driver.refresh()
    time.sleep(0.5)  # TODO: replace sleep with loader


@pytest.fixture(autouse=True, scope="class")
def home_signed_out_page(driver):
    yield HomeSignedOut(driver)


@pytest.fixture(scope="class", autouse=True)
def global_(driver):
    yield Global(driver)
