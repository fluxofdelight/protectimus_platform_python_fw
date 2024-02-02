from selenium.webdriver.common.by import By

from src.ui.locators.locators_provider import LocatorsProvider


class UserInfoLocators:

    USER_LOGIN = LocatorsProvider(web=(By.CSS_SELECTOR, "h4.mt-3"))

    DELETE_BTN = LocatorsProvider(web=(By.CSS_SELECTOR, "div:nth-child(8) > button.btn"))
