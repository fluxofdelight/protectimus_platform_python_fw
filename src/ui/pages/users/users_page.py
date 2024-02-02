import allure
from loguru import logger as log

from src.api.api_methods import ApiMethods
from src.common import string_utils as s
from src.common.general_utils import GeneralUtils
from src.configs.config import Config
from src.db.db_methods import DatabaseMethods
from src.ui.locators.users.users_page_locators import UsersPageLocators
from src.ui.pages.base_page import BasePage
from src.ui.pages.global_ import Global, GlobalLocators


class UsersPage(BasePage, UsersPageLocators, GlobalLocators):
    def __init__(self, driver):
        super().__init__(driver)
        self.config = Config()
        self.endpoint = "users/"
        self.db = DatabaseMethods().users
        self.api = ApiMethods(self.config.api).users
        self.glob = Global(driver)
        self.g = GeneralUtils(driver)

    @allure.step('Open the "Users" page via URL')
    def open_users_url(self, url):
        self.driver.get(url + self.endpoint)
        return self

    @allure.step('Click the "Add user" button')
    def click_add_user_button(self):
        self.driver.ui_element(self.ADD_USER_BUTTON).should(self.be.visible).click()
        return self

    @allure.step('Fill in the "Login" field')
    def fill_in_login_field(self, login, edit_user=False):
        (self.driver.ui_element(self.LOGIN_FLD_EDIT_USER if edit_user else self.LOGIN_FLD_ADD_USER)
         .should(self.be.visible).set_value(login))
        return self

    @allure.step('Fill in the "Alias" field')
    def fill_in_alias_field(self, alias, edit_user=False):
        (self.driver.ui_element(self.ALIAS_FLD_EDIT_USER if edit_user else self.ALIAS_FLD_ADD_USER)
         .should(self.be.visible).set_value(alias))
        return self

    @allure.step('Fill in the "Password" field')
    def fill_in_password_field(self, password, edit_user=False):
        (self.driver.ui_element(self.PASS_FLD_EDIT_USER if edit_user else self.PASS_FLD_ADD_USER)
         .should(self.be.visible).set_value(password))
        return self

    @allure.step('Fill in the "Password Confirmation" field')
    def fill_in_password_confirm_field(self, password, edit_user=False):
        (self.driver.ui_element(self.PASS_CONF_FLD_EDIT_USER if edit_user else self.PASS_CONF_FLD_ADD_USER)
         .should(self.be.visible).set_value(password))
        return self

    @allure.step('Fill in the "First Name" field')
    def fill_in_first_name_field(self, first_name, edit_user=False):
        (self.driver.ui_element(self.FIRST_NAME_FLD_EDIT_USER if edit_user else self.FIRST_NAME_FLD_ADD_USER)
         .should(self.be.visible).set_value(first_name))
        return self

    @allure.step('Fill in the "Last Name" field')
    def fill_in_last_name_field(self, last_name, edit_user=False):
        (self.driver.ui_element(self.LAST_NAME_FLD_EDIT_USER if edit_user else self.LAST_NAME_FLD_ADD_USER)
         .should(self.be.visible).set_value(last_name))
        return self

    @allure.step('Fill in the "E-Mail Address" field')
    def fill_in_email_field(self, email, edit_user=False):
        (self.driver.ui_element(self.EMAIL_FLD_EDIT_USER if edit_user else self.EMAIL_FLD_ADD_USER)
         .should(self.be.visible).set_value(email))
        return self

    @allure.step('Fill in the "Phone Number" field')
    def fill_in_phone_field(self, phone, edit_user=False):
        (self.driver.ui_element(self.PHONE_FLD_EDIT_USER if edit_user else self.PHONE_FLD_ADD_USER)
         .should(self.be.visible).set_value(phone))
        return self

    @allure.step('Click the "Create" button in the "Add User" dialog')
    def click_create_button_add_user(self):
        self.driver.ui_element(self.CREATE_BTN_ADD_USER).should(self.be.visible).click()
        return self

    @allure.step('Click the "Save" button in the "Edit User" dialog')
    def click_save_button_edit_user(self):
        self.driver.ui_element(self.SAVE_BTN_EDIT_USER).should(self.be.visible).click()
        return self

    def create_valid_user(
        self,
        login=("user_" + s.random_name()),
        first_name="John",
        last_name="Doe",
        alias=False,
        password=False,
        email=False,
        phone=False,
    ):
        (
            self.click_add_user_button()
            .fill_in_login_field(login)
            .fill_in_first_name_field(first_name)
            .fill_in_last_name_field(last_name)
        )
        if alias:
            self.fill_in_alias_field(alias)
        if password:
            self.fill_in_password_field(password)
            self.fill_in_password_confirm_field(password)
        if email:
            self.fill_in_email_field(email)
        if phone:
            self.fill_in_phone_field(phone)
        self.click_create_button_add_user()
        return self

    def verify_user_creating(self, user_login):
        toast_text = f"User '{user_login}' was successfully created."
        self.glob.verify_toast_text(toast_text)
        return self

    def edit_first_user(
        self,
        login=("user_" + s.random_name()),
        first_name="Paul",
        last_name=s.random_name().capitalize,
        alias=False,
        password=False,
        email=False,
        phone=False,
    ):
        (self.click_three_dots_button_first_user().click_edit_button_first_user())
        if login:
            self.fill_in_login_field(login, edit_user=True)
        if first_name:
            self.fill_in_first_name_field(first_name, edit_user=True)
        if last_name:
            self.fill_in_last_name_field(last_name, edit_user=True)
        if alias:
            self.fill_in_alias_field(alias, edit_user=True)
        if password:
            self.fill_in_password_field(password, edit_user=True)
            self.fill_in_password_confirm_field(password, edit_user=True)
        if email:
            self.fill_in_email_field(email, edit_user=True)
        if phone:
            self.fill_in_phone_field(phone, edit_user=True)
        self.click_save_button_edit_user()
        return self

    def verify_user_edit(self, user_login):
        toast_text = f"User '{user_login}' was successfully updated."
        self.glob.verify_toast_text(toast_text)
        return self

    def get_first_user_login(self):
        return self.db.get_first_user_login()

    def get_first_user_id(self):
        return self.db.get_first_user_id()

    @allure.step("Verify a login of the first user in the table")
    def verify_first_user_login(self, expected_login):
        (
            self.driver.ui_element(self.LOGIN_LINK_FIRST_USER)
            .should(self.be.visible)
            .should(self.have.text(expected_login))
        )
        return self

    @allure.step("Verify the full name of the first user in the table")
    def verify_first_user_full_name(self, first_name, last_name):
        (
            self.driver.ui_element(self.NAME_FIRST_USER)
            .should(self.be.visible)
            .should(self.have.text(first_name + " " + last_name))
        )
        return self

    @allure.step("Verify an email of the first user in the table")
    def verify_first_user_email(self, email):
        self.driver.ui_element(self.EMAIL_FIRST_USER).should(self.be.visible).should(self.have.text(email))
        return self

    @allure.step("Verify a phone of the first user in the table")
    def verify_first_user_phone(self, phone):
        self.driver.ui_element(self.PHONE_FIRST_USER).should(self.be.visible).should(self.have.text(phone))
        return self

    @allure.step("Verify an alias of the first user in the table")
    def verify_first_user_alias(self, alias):
        self.driver.ui_element(self.ALIAS_FLD_EDIT_USER).should(self.be.visible).should(self.have.value(alias))
        return self

    @allure.step("Verify an alias of the first user in the table")
    def verify_first_user_has_password(self):
        self.driver.ui_element(self.ALIAS_FLD_EDIT_USER).should(self.be.visible).should(self.not_.blank)
        return self

    @allure.step("Verify the ID of the first user in the table checking the full URL")
    def verify_first_user_id_via_full_url(self, user_id):
        self.glob.verify_url_of_element(
            self.LOGIN_LINK_FIRST_USER, (self.config.web.base_url + self.endpoint + user_id)
        )
        return self

    # Delete in the future
    def get_first_user_and_create_if_not_exist(self, login=False, first_name=False, last_name=False):
        first_user = self.get_first_user_login()
        if first_user:
            self.driver.ui_element(self.LOGIN_LINK_FIRST_USER).should(self.have.text(first_user))
            log.info(f"User exists. User's login '{first_user}'")
            return first_user
        else:
            log.info("Creating a new user...")
            random_login = "user_" + s.random_name()
            self.api.add_user(
                login=(login if login else random_login),
                first_name=(first_name if first_name else "John"),
                second_name=(last_name if last_name else "Doe"),
            )
            if login:
                return login
            else:
                return random_login

    @allure.step('Open the "User Info" page')
    def open_first_user_info_page(self):
        self.driver.ui_element(self.LOGIN_LINK_FIRST_USER).should(self.be.visible).click()
        return self

    @allure.step('Click the "Three dots" button of the first user')
    def click_three_dots_button_first_user(self):
        self.driver.ui_element(self.THREE_DOTS_FIRST_USER).should(self.be.visible).click()
        return self

    @allure.step('Click the "Delete" button in the dropdown')
    def click_delete_button_first_user(self):
        self.driver.ui_element(self.DELETE_BTN_DROPDOWN).should(self.be.visible).click()
        return self

    @allure.step('Click the "Edit" button in the dropdown')
    def click_edit_button_first_user(self):
        self.driver.ui_element(self.EDIT_BTN_DROPDOWN).should(self.be.visible).click()
        return self

    def delete_first_user(self, user_login=None):
        if user_login:
            delete_dialog_text = f"Do you really want to delete user '{user_login}'?"
        else:
            first_user_login = self.get_first_user_login()
            delete_dialog_text = f"Do you really want to delete user '{first_user_login}'?"
        self.click_three_dots_button_first_user()
        self.click_delete_button_first_user()
        self.glob.verify_delete_dialog_text(delete_dialog_text)
        self.glob.click_yes_button_delete_dialog()
        return self

    def verify_user_deletion(self, user_login):
        toast_text = f"User '{user_login}' was successfully deleted."
        self.glob.verify_toast_text(toast_text)
        return self

    @allure.step("Verify that the first user in the table is visible")
    def check_first_user_visibility(self):
        self.driver.ui_element(self.LOGIN_LINK_FIRST_USER).should(self.be.visible)
        return self

    @allure.step('Fill in the "Login" field in the filters')
    def fill_in_login_filter(self, login):
        self.driver.ui_element(self.LOGIN_FLD_FILTER).should(self.be.visible).set_value(login)
        return self

    @allure.step('Fill in the "Email" field in the filters')
    def fill_in_email_filter(self, email):
        self.driver.ui_element(self.EMAIL_FLD_FILTER).should(self.be.visible).set_value(email)
        return self

    @allure.step('Fill in the "ID" field in the filters')
    def fill_in_id_filter(self, user_id):
        self.driver.ui_element(self.ID_FLD_FILTER).should(self.be.visible).set_value(user_id)
        return self

    @allure.step('Fill in the "First name" field in the filters')
    def fill_in_first_name_filter(self, first_name):
        self.driver.ui_element(self.FIRST_NAME_FLD_FILTER).should(self.be.visible).set_value(first_name)
        return self

    @allure.step('Fill in the "Last name" field in the filters')
    def fill_in_last_name_filter(self, last_name):
        self.driver.ui_element(self.LAST_NAME_FLD_FILTER).should(self.be.visible).set_value(last_name)
        return self

    @allure.step('Fill in the "Resource" field in the filters')
    def fill_in_resource_filter(self, resource):
        self.driver.ui_element(self.RESOURCE_FLD_FILTER).should(self.be.visible).set_value(resource)
        return self

    @allure.step('Select block option in the "Block" dropdown in the filters')
    def select_block_filter(self, block_option=None):
        block_option = block_option if block_option else self.OPTION_NOT_BLOCKED_DROP
        self.driver.ui_element(self.BLOCK_DROPDOWN_FILTER).should(self.be.visible).click()
        self.driver.ui_element(block_option).should(self.be.visible).click()
        return self

    def filter_users(
        self,
        login=False,
        email=False,
        user_id=False,
        first=False,
        last=False,
        block=False,
        block_option=None,
        resource=False,
    ):
        self.glob.open_filters()

        if login:
            self.fill_in_login_filter(login)
        if email:
            self.fill_in_email_filter(email)
        if user_id:
            self.fill_in_id_filter(user_id)
        if first:
            self.fill_in_first_name_filter(first)
        if last:
            self.fill_in_last_name_filter(last)
        if block:
            self.select_block_filter(block_option)
        if resource:
            self.fill_in_resource_filter(resource)
        if not any([login, email, user_id, first, last, block, resource]):
            log.info("No filters selected")
            raise ValueError("Select at least one filter")
        self.glob.apply_filters()
        return self

    @allure.step("Disable API support of the first user in the table")
    def block_first_user(self):
        try:
            if self.g.verify_css_property(self.API_FIRST_USER, "rgba(52, 178, 226, 1)"):
                self.driver.ui_element(self.API_FIRST_USER).should(self.be.visible).click()
                return self
        except AssertionError:
            if self.g.verify_css_property(self.API_FIRST_USER, "rgba(255, 255, 255, 1)"):
                log.info("User is already blocked")
                return self

    @allure.step("Verify that the first user in the table is blocked")
    def verify_first_user_blocked(self):
        self.g.verify_css_property(self.API_FIRST_USER, "rgba(255, 255, 255, 1)")
        return self
