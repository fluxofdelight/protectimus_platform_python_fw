from typing import Union

from loguru import logger as log
from selene import Browser, Config
from selene.common.helpers import to_by
from selene.core.locator import Locator
from selenium import webdriver

from src.common.singleton import singleton
from src.configs.config import Config as ProjectConfig
from src.ui.driver.element import ProvidableElement
from src.ui.locators.locators_provider import LocatorsProvider


@singleton
class Driver(Browser):
    browser = None

    @classmethod
    def start_from_configs(cls, configs: ProjectConfig):
        driver = None
        cls.configs = configs
        cls.browser = configs.web.browser
        supported_browsers = ["chrome", "headlesschrome", "hlc", "firefox", "headlessfirefox", "hlf", "edge", "safari"]

        if cls.browser.lower() not in supported_browsers:
            raise Exception(
                f'Provided browser "{cls.browser}" is not one of the supported.' f"Supported are: {supported_browsers}"
            )
        elif cls.browser.lower() == supported_browsers[0]:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--window-size=1920,1080")
            log.info("Stating 'Chrome' for UI tests...")
            driver = webdriver.Chrome(options=chrome_options)
        elif cls.browser.lower() in supported_browsers[1:3]:
            hlc_options = webdriver.ChromeOptions()
            hlc_options.add_argument("--disable-gpu")
            hlc_options.add_argument("--no-sandbox")
            hlc_options.add_argument("--disable-extensions")
            hlc_options.add_argument("headless")
            log.info("Stating 'Headless Chrome' for UI tests...")
            driver = webdriver.Chrome(options=hlc_options)
        elif cls.browser.lower() == supported_browsers[3]:
            ff_options = webdriver.FirefoxOptions()
            ff_options.add_argument("--disable-extensions")
            ff_options.add_argument("--window-size=1920,1080")
            log.info("Stating 'Firefox' for UI tests...")
            driver = webdriver.Firefox(options=ff_options)
        elif cls.browser.lower() in supported_browsers[4:6]:
            hlf_options = webdriver.FirefoxOptions()
            hlf_options.add_argument("--disable-gpu")
            hlf_options.add_argument("--no-sandbox")
            hlf_options.add_argument("--disable-extensions")
            hlf_options.add_argument("headless")
            log.info("Stating 'Headless Firefox' for UI tests...")
            driver = webdriver.Firefox(options=hlf_options)
        elif cls.browser.lower() == supported_browsers[6]:
            log.info("Stating 'Edge' for UI tests...")
            driver = webdriver.Edge()
        elif cls.browser.lower() == supported_browsers[7]:
            log.info("Stating 'Safari' for UI tests...")
            driver = webdriver.Safari()

        log.info("Browser started")
        driver.maximize_window()
        driver.get(configs.web.base_url)
        driver = cls(Config(driver=driver, timeout=5))
        return driver

    def element(self, css_or_xpath_or_by: Union[str, tuple]) -> ProvidableElement:
        by = to_by(css_or_xpath_or_by)

        return ProvidableElement(
            Locator(f"{self}.element({by})", lambda: self.driver.find_element(*by)),
            self.config,
        )

    def ui_element(self, selector: LocatorsProvider) -> ProvidableElement:
        if not isinstance(selector, LocatorsProvider):
            raise Exception
        return self.element(getattr(selector, "web"))

    @property
    def driver(self) -> webdriver.Chrome:
        return self.config.driver
