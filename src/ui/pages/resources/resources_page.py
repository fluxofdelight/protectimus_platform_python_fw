import allure
from loguru import logger as log

from src.common import string_utils as s
from src.common.general_utils import GeneralUtils
from src.configs.config import Config
from src.db.db_methods import DatabaseMethods
from src.ui.locators.global_locators import GlobalLocators
from src.ui.locators.resources.resources_locators import ResourcesLocators
from src.ui.pages.base_page import BasePage
from src.ui.pages.global_ import Global


class ResourcesPage(BasePage, ResourcesLocators, GlobalLocators):
    def __init__(self, driver):
        super().__init__(driver)
        self.config = Config()
        self.endpoint = "resources/"
        self.db = DatabaseMethods().resources
        self.glob = Global(driver)
        self.g = GeneralUtils(driver)

    @allure.step('Open the "Resources" page via URL')
    def open_resources_url(self, url):
        self.driver.get(url + self.endpoint)
        return self

    @allure.step('Click the "Add resource" button')
    def click_add_resource_button(self):
        self.driver.ui_element(self.ADD_RESOURCE_BUTTON).should(self.be.visible).click()
        return self

    @allure.step('Fill in the "Resource name" field')
    def fill_in_resource_name_field(self, name, edit_resource=False):
        (self.driver.ui_element(self.NAME_FLD_EDIT_RESOURCE if edit_resource else self.NAME_FLD_ADD_RESOURCE)
         .should(self.be.visible).set_value(name))
        return self

    @allure.step('Fill in the "Failed Login Attempts Before Locking" field')
    def fill_in_login_attempts_field(self, attempts, edit_resource=False):
        (self.driver.ui_element(self.ATTEMPTS_FLD_EDIT_RESOURCE if edit_resource else self.ATTEMPTS_FLD_ADD_RESOURCE)
         .should(self.be.visible).set_value(attempts))
        return self

    @allure.step('Tick the "IP Verification Enabled" checkbox')
    def tick_ip_verification_checkbox(self, edit_resource=False):
        (self.driver.ui_element(self.IP_CHECKBOX_EDIT_RESOURCE if edit_resource else self.IP_CHECKBOX_ADD_RESOURCE)
         .should(self.be.visible).click())
        return self

    @allure.step('Fill in the "Enter IP address" field')
    def fill_in_ip_field(self, ip, edit_resource=False):
        (self.driver.ui_element(self.IP_FLD_EDIT_RESOURCE if edit_resource else self.IP_FLD_ADD_RESOURCE)
         .should(self.be.visible).set_value(ip))
        return self

    @allure.step('Click the "Add IP" button')
    def click_add_ip_button(self, edit_resource=False):
        (self.driver.ui_element(self.IP_BTN_EDIT_RESOURCE if edit_resource else self.IP_BTN_ADD_RESOURCE)
         .should(self.be.visible).click())
        return self

    @allure.step('Click the "Enabled" switch')
    def click_enabled_switch(self, edit_resource=False):
        self.driver.ui_element(self.ENABLED_SWITCH_EDIT_RESOURCE if edit_resource
                               else self.ENABLED_SWITCH_ADD_RESOURCE).should(self.be.visible).click()
        return self

    @allure.step('Click the "Create" button in the "Add resource" dialog')
    def click_create_button_add_resource(self):
        self.driver.ui_element(self.CREATE_BTN_ADD_RESOURCE).should(self.be.visible).click()
        return self

    @allure.step('Click the "Save" button in the "Edit resource" dialog')
    def click_save_button_edit_resource(self):
        self.driver.ui_element(self.SAVE_BTN_EDIT_RESOURCE).should(self.be.visible).click()
        return self

    @allure.step("Creating a valid resource")  # Maybe don't need this step name
    def create_valid_resource(
        self,
        name=("resource_" + s.random_name()),
        attempts=None,
        ip_enabled=False,
        ips: list = None,
        not_enabled=False,
    ):
        (self.click_add_resource_button().fill_in_resource_name_field(name))
        if attempts:
            self.fill_in_login_attempts_field(attempts)
        if ip_enabled and ips:
            self.tick_ip_verification_checkbox()
            for ip in ips:
                (self.fill_in_ip_field(ip).click_add_ip_button())
        if not_enabled:
            self.click_enabled_switch()
        self.click_create_button_add_resource()
        return self

    def verify_resource_creating(self, resource_name):
        toast_text = f"Resource '{resource_name}' was created successfully."
        self.glob.verify_toast_text(toast_text)
        return self

    @allure.step("Editing the resource")  # Maybe don't need this step name
    def edit_first_resource(
        self,
        name=("resource_" + s.random_name()),
        attempts=False,
        ip_verif_disable=False,
        ip_verif_enable=False,
        ips: list = False,
        enable_resource=False,
        disable_resource=False,
    ):
        first_resource_name = self.db.get_first_resource_name()
        (
            self.verify_first_resource_name(first_resource_name)
            .click_three_dots_button_first_resource()
            .click_edit_button_first_resource()
        )
        if name:
            self.fill_in_resource_name_filter(name)
        if attempts:
            self.fill_in_login_attempts_field(attempts)
        self.handle_ip_verification_edit_resource(first_resource_name, ip_verif_disable, ip_verif_enable, ips)
        self.handle_resource_state_edit_resource(first_resource_name, enable_resource, disable_resource)
        self.click_save_button_edit_resource()
        return self

    def handle_ip_verification_edit_resource(self, resource_name, disable=False, enable=False, ips: list = False):
        if disable:
            if self.db.verify_resource_ip_verification_by_resource_name(resource_name):
                self.tick_ip_verification_checkbox()
            else:
                log.info("IP verification of the resource is already disabled")
        if enable and ips:
            if self.db.verify_resource_ip_verification_by_resource_name(resource_name):
                log.info("IP verification of the resource is already enabled")
                for ip in ips:
                    (self.fill_in_ip_field(ip).click_add_ip_button())
            else:
                self.tick_ip_verification_checkbox()
                for ip in ips:
                    (self.fill_in_ip_field(ip).click_add_ip_button())
        return self

    def handle_resource_state_edit_resource(self, resource_name, enable=False, disable=False):
        if enable:
            if self.db.verify_resource_enabled_by_resource_name(resource_name):
                log.info("Resource is already enabled")
            else:
                self.click_enabled_switch()
        if disable:
            if self.db.verify_resource_enabled_by_resource_name(resource_name):
                self.click_enabled_switch()
            else:
                log.info("Resource is already disabled")
        return self

    def verify_resource_edit(self, resource_name):
        toast_text = f"Resource '{resource_name}' was successfully updated."
        self.glob.verify_toast_text(toast_text)
        return self

    @allure.step("Verify a name of the first resource in the table")
    def verify_first_resource_name(self, expected_name):
        self.driver.ui_element(self.NAME_FIRST_RESOURCE).should(self.be.visible).should(self.have.text(expected_name))
        return self

    @allure.step("Verify an ID of the first resource in the table")
    def verify_first_resource_id(self, expected_id):
        self.driver.ui_element(self.ID_LINK_FIRST_RESOURCE).should(self.be.visible).should(self.have.text(expected_id))
        return self

    @allure.step('Click the "Three dots" button of the first resource')
    def click_three_dots_button_first_resource(self):
        self.driver.ui_element(self.THREE_DOTS_FIRST_RESOURCE).should(self.be.visible).click()
        return self

    @allure.step('Click the "Edit" button in the dropdown')
    def click_edit_button_first_resource(self):
        self.driver.ui_element(self.EDIT_BTN_DROPDOWN).should(self.be.visible).click()
        return self

    @allure.step('Click the "Delete" button in the dropdown')
    def click_delete_button_first_resource(self):
        self.driver.ui_element(self.DELETE_BTN_DROPDOWN).should(self.be.visible).click()
        return self

    @allure.step("Verify an IPs of the first resource in the table")
    def verify_ips_first_resource(self, ips: list):
        self.click_three_dots_button_first_resource().click_edit_button_first_resource()
        for row, ip in zip(range(1, len(ips) + 1), ips):
            (
                self.driver.ui_element(self.any_resource_ip(row, edit_resource=True))
                .should(self.be.visible)
                .should(self.have.text(ip))
            )
        return self

    @allure.step("Deleting a resource")  # Maybe don't need this step name
    def delete_first_resource(self, resource_name=None):
        if resource_name:
            delete_dialog_text = f"Do you really want to delete resource '{resource_name}'?"
        else:
            first_resource_name = self.db.get_first_resource_name()
            delete_dialog_text = f"Do you really want to delete resource '{first_resource_name}'?"
        self.click_three_dots_button_first_resource()
        self.click_delete_button_first_resource()
        self.glob.verify_delete_dialog_text(delete_dialog_text)
        self.glob.click_yes_button_delete_dialog()
        return self

    def verify_resource_deletion(self, resource_name):
        toast_text = f"Resource '{resource_name}' was deleted successfully."
        self.glob.verify_toast_text(toast_text)
        return self

    @allure.step('Fill in the "Name" field in the filters')
    def fill_in_resource_name_filter(self, resource_name):
        self.driver.ui_element(self.NAME_FLD_FILTER).should(self.be.visible).set_value(resource_name)
        return self

    @allure.step('Fill in the "Resource ID" field in the filters')
    def fill_in_resource_id_filter(self, resource_id):
        self.driver.ui_element(self.ID_FLD_FILTER).should(self.be.visible).set_value(resource_id)
        return self

    def filter_resources(self, resource_name=False, resource_id=False):
        self.glob.open_filters()
        if resource_name:
            self.fill_in_resource_name_filter(resource_name)
        if resource_id:
            self.fill_in_resource_id_filter(resource_id)
        if not any([resource_name, resource_id]):
            log.info("No filters selected")
            raise ValueError("Select at least one filter")
        self.glob.apply_filters()
        return self
