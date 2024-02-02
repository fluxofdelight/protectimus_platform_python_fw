import allure

from src.ui.locators.global_locators import GlobalLocators
from src.ui.pages.base_page import BasePage


class Global(BasePage, GlobalLocators):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Click on the "Users" button')
    def open_users_page(self):
        self.driver.ui_element(self.USERS_BUTTON).should(self.be.visible).click()
        return self

    @allure.step('Click on the "Resources" button')
    def open_resources_page(self):
        self.driver.ui_element(self.RESOURCES_BUTTON).should(self.be.visible).click()
        return self

    @allure.step("Click the dropdown to set up a number of objects displayed in the table")
    def click_number_of_objects_dropdown(self, bottom_dropdown=False):
        if bottom_dropdown:
            self.driver.ui_element(self.ELEMENTS_NUM_BTM_DROPDOWN).should(self.be.visible).click()
        else:
            self.driver.ui_element(self.ELEMENTS_NUM_TOP_DROPDOWN).should(self.be.visible).click()
        return self

    @allure.step("Select an option in the number of objects displayed in the table dropdown")
    def select_option_in_number_of_objects_dropdown(self, number_of_objects, bottom_dropdown=False):
        if number_of_objects not in [5, 10, 15, 20, 25, 50]:
            raise Exception(
                f'Invalid value for the "number_of_objects" parameter'
                f"\nCurrent value: {number_of_objects}. Expected: 5, 10, 15, 20, 25, or 50"
            )
        if number_of_objects == 5:
            (
                self.driver.ui_element(self.OPTION_5_BTM if bottom_dropdown else self.OPTION_5_TOP)
                .should(self.be.visible)
                .click()
            )
        if number_of_objects == 10:
            (
                self.driver.ui_element(self.OPTION_10_BTM if bottom_dropdown else self.OPTION_10_TOP)
                .should(self.be.visible)
                .click()
            )
        if number_of_objects == 15:
            (
                self.driver.ui_element(self.OPTION_15_BTM if bottom_dropdown else self.OPTION_15_TOP)
                .should(self.be.visible)
                .click()
            )
        if number_of_objects == 20:
            (
                self.driver.ui_element(self.OPTION_20_BTM if bottom_dropdown else self.OPTION_20_TOP)
                .should(self.be.visible)
                .click()
            )
        if number_of_objects == 25:
            (
                self.driver.ui_element(self.OPTION_25_BTM if bottom_dropdown else self.OPTION_25_TOP)
                .should(self.be.visible)
                .click()
            )
        if number_of_objects == 50:
            (
                self.driver.ui_element(self.OPTION_50_BTM if bottom_dropdown else self.OPTION_50_TOP)
                .should(self.be.visible)
                .click()
            )
        return self

    @allure.step('Click the "Next (>)" button in the pagination')
    def click_next_button_of_pagination(self, bottom_pagination=False):
        if bottom_pagination:
            self.driver.ui_element(self.RIGHT_ARROW_BTM).should(self.be.visible).click()
        else:
            self.driver.ui_element(self.RIGHT_ARROW_TOP).should(self.be.visible).click()
        return self

    @allure.step("Check if current page is the last one")
    def check_if_the_last_page(self, bottom_pagination=False):
        if bottom_pagination:
            self.driver.ui_element(self.RIGHT_ARROW_BTM).should(self.be.visible).should(self.not_.clickable)
        else:
            self.driver.ui_element(self.RIGHT_ARROW_TOP).should(self.be.visible).should(self.not_.clickable)
        return self

    @allure.step("Open the filters accordion")
    def open_filters(self):
        self.driver.ui_element(self.FILTERS_ACCORDION).should(self.be.visible).click()
        return self

    @allure.step('Click on the "Apply" button to apply filters')
    def apply_filters(self):
        self.driver.ui_element(self.APPLY_BTN_FILTER).should(self.be.visible).click()
        return self

    @allure.step('Search an object and press the "Enter" key')
    def search_objects(self, value):
        self.driver.ui_element(self.SEARCH_FIELD).should(self.be.visible).set_value(value)
        self.driver.ui_element(self.SEARCH_FIELD).should(self.be.visible).press_enter()
        return self

    @allure.step('Clear the "Search" field')
    def clear_search_field(self):
        self.driver.ui_element(self.SEARCH_FIELD).clear()
        return self

    @allure.step('Click the "Yes" button in the dialog for deletion')
    def click_yes_button_delete_dialog(self):
        self.driver.ui_element(self.DELETE_DIALOG_YES_BTN).should(self.be.visible).click()
        return self

    @allure.step("Verify the text in the deletion dialog")
    def verify_delete_dialog_text(self, delete_dialog_text):
        self.driver.ui_element(self.CENTER_DIALOG).should(self.be.visible).should(self.have.text(delete_dialog_text))
        return self

    @allure.step("Verify the text in the toast after deletion")
    def verify_toast_text(self, toast_text):
        self.driver.ui_element(self.TOAST_CONTAINER).should(self.be.visible).should(self.have.text(toast_text))
        return self

    @allure.step("Verify the URL of the element")
    def verify_url_of_element(self, locator, expected_url):
        self.driver.ui_element(locator).should(self.have.attribute("href").value(expected_url))
        return self
