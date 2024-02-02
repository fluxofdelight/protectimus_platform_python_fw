import allure

from src.ui.locators.global_locators import GlobalLocators
from src.ui.locators.home.home_signed_in_locators import HomeSignedInLocators
from src.ui.pages.base_page import BasePage


class HomeSignedIn(BasePage, HomeSignedInLocators, GlobalLocators):
    @allure.step("Verify client's email")
    def verify_client_email(self, expected_email):
        self.driver.ui_element(self.CLIENT_EMAIL).should(self.be.visible).should(self.have.text(expected_email))
