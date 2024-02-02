import time

import allure

from src.ui.locators.home.home_signed_out_locators import HomeSignedOutLocators
from src.ui.pages.base_page import BasePage


class HomeSignedOut(BasePage, HomeSignedOutLocators):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Fill in email for login")
    def fill_in_login_email(self, email):
        self.driver.ui_element(self.LOGIN_EMAIL).should(self.be.visible).set_value(email)
        return self

    @allure.step("Fill in password")
    def fill_in_password(self, password):
        self.driver.ui_element(self.PASSWORD).should(self.be.visible).set_value(password)
        return self

    @allure.step('Click the "Login" button')
    def click_login_button(self, success_click=True):
        self.driver.ui_element(self.LOGIN_BUTTON).should(self.be.visible).click()
        if success_click:
            time.sleep(2)  # TODO: add Loader instead
            self.driver.ui_element(self.LOGIN_BUTTON).should(self.not_.visible)
        return self

    def login(self, email, password):
        self.fill_in_login_email(email)
        self.fill_in_password(password)
        self.click_login_button()
        return self

    @allure.step('Click the "Register" button')
    def click_register_tab(self):
        reg_tab_class = "router-link-active router-link-exact-active nav-link active"
        (
            self.driver.ui_element(self.REGISTER_TAB)
            .should(self.be.visible)
            .click()
            .should(self.have.css_class(reg_tab_class))
        )
        return self

    @allure.step("Fill in email for registration")
    def fill_in_register_email(self, email):
        self.driver.ui_element(self.REGISTER_EMAIL).should(self.be.visible).set_value(email)
        return self

    @allure.step("Fill in password confirmation")
    def fill_in_password_confirm(self, password):
        self.driver.ui_element(self.PASSWORD_CONFIRM).should(self.be.visible).set_value(password)
        return self

    @allure.step("Tick on the 'Terms of use' checkbox")
    def tick_on_terms(self):
        self.driver.ui_element(self.TERMS_CHECKBOX).should(self.be.visible).click().should(self.be.selected)
        return self

    @allure.step("Click register button")
    def click_register_button(self, success_click=True):
        self.driver.ui_element(self.REGISTER_BUTTON).should(self.be.visible).click()
        if success_click:
            self.driver.ui_element(self.REGISTER_BUTTON).should(self.not_.visible)
        return self

    @allure.step("Registration")
    def registration(self, email, password):
        self.click_register_tab()
        self.fill_in_register_email(email)
        self.fill_in_password(password)
        self.fill_in_password_confirm(password)
        self.tick_on_terms()
        self.click_register_button()
        return self
