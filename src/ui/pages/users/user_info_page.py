import allure

from src.common.entry_data import EntryData
from src.ui.locators.global_locators import GlobalLocators
from src.ui.locators.users.user_info_locators import UserInfoLocators
from src.ui.pages.base_page import BasePage
from src.ui.pages.global_ import Global


class UserInfoPage(BasePage, UserInfoLocators, GlobalLocators):
    def __init__(self, driver):
        super().__init__(driver)
        self.glob = Global(driver)
        self.test_data = EntryData()
        self.user_id = self.test_data.user_id_to_open_user_info
        self.endpoint = f"users/{self.user_id}/"

    @allure.step('Open the "User Info" page via URL')
    def open_user_info_page(self, url):
        self.driver.get(url + self.endpoint)
        return self

    @allure.step('Delete the user on the "User Info" page')
    def delete_user(self, user_login):
        expected_dialog_text = f"Do you really want to delete user '{user_login}'?"
        self.driver.ui_element(self.DELETE_BTN).should(self.be.visible).click()
        self.glob.verify_delete_dialog_text(expected_dialog_text)
        self.glob.click_yes_button_delete_dialog()
        return self

    @allure.step("Verify the user login")
    def verify_user_login(self, login):
        self.driver.ui_element(self.USER_LOGIN).should(self.be.visible).should(self.have.text(login))
        return self
