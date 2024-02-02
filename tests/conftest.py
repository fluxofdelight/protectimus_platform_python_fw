import allure
import pytest

from src.api.api_methods import ApiMethods
from src.common.logger import ConfigurateLogger
from src.configs.config import Config
from src.db.db_methods import DatabaseMethods
from src.db.prepare_env import PrepareEnv


@pytest.fixture(autouse=True, scope="session")
def prepare_env():
    prepare_env = PrepareEnv()
    prepare_env.drop_all_db_info()
    prepare_env.fill_out_db()


@pytest.fixture(autouse=True, scope="session")
def project_config():
    yield Config()


@pytest.fixture(autouse=True, scope="session")
def api(project_config):
    yield ApiMethods(config=project_config.api)


@pytest.fixture(autouse=True, scope="session")
def db():
    yield DatabaseMethods()


@pytest.fixture(autouse=True, scope="session")
def log(project_config):
    ConfigurateLogger(project_config)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Allure report with a screenshot
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        # check if test failed
        if (report.skipped and xfail) or (report.failed and not xfail):
            is_frontend_test = True if "init_driver" in item.fixturenames else False
            if is_frontend_test:
                driver_fixture = item.funcargs["request"]
                allure.attach(
                    driver_fixture.cls.driver.get_screenshot_as_png(),
                    name=item.name,
                    attachment_type=allure.attachment_type.PNG,
                )
