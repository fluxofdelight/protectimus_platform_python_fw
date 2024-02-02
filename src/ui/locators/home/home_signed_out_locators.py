from selenium.webdriver.common.by import By

from src.ui.locators.locators_provider import LocatorsProvider


class HomeSignedOutLocators:

    LOGIN_EMAIL = LocatorsProvider(web=(By.NAME, "login"))
    LOGIN_BUTTON = LocatorsProvider(web=(By.CSS_SELECTOR, 'button[type="submit"]'))

    PASSWORD = LocatorsProvider(web=(By.NAME, "password"))  # Same for both login and registration

    LOGIN_TAB = LocatorsProvider(web=(By.CSS_SELECTOR, "li.nav-item:nth-child(1) > a.router-link-active"))
    REGISTER_TAB = LocatorsProvider(web=(By.CSS_SELECTOR, "li.nav-item:nth-child(2) > a.router-link-active"))

    REGISTER_EMAIL = LocatorsProvider(web=(By.NAME, "email"))
    PASSWORD_CONFIRM = LocatorsProvider(web=(By.NAME, "passwordConfirmation"))
    TERMS_CHECKBOX = LocatorsProvider(web=(By.CSS_SELECTOR, 'input[id^="checkbox"]'))
    REGISTER_BUTTON = LocatorsProvider(web=(By.CSS_SELECTOR, 'button[type="submit"]'))
