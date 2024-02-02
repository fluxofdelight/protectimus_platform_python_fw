from selenium.webdriver.common.by import By

from src.ui.locators.locators_provider import LocatorsProvider


class ResourcesLocators:
    ADD_RESOURCE_BUTTON = LocatorsProvider(web=(By.CSS_SELECTOR, "button.btn-sm"))

    """Filter"""
    NAME_FLD_FILTER = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.p-3 > div:nth-child(1) div.mb-3 > input.form-control")
    )
    ID_FLD_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.mb-3 > input[type="number"]'))

    # First resource in the table
    AVATAR_LINK_FIRST_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "div.media-aside > div.text-center"))
    ID_LINK_FIRST_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "div.media-body > div.justify-content-between a"))
    NAME_FIRST_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "div.media-body > div.justify-content-between span"))
    GEO_FILTER_FIRST_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "td.ps-4:nth-child(2) i.fa-globe + a"))
    TIME_FILTER_FIRST_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "td.ps-4:nth-child(2) i.fa-clock + a"))
    CREATOR_LINK_FIRST_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "td:nth-child(3) > a"))
    ENABLED_FIRST_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, 'td input[role="switch"]'))
    THREE_DOTS_FIRST_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "i.fa-ellipsis-v"))

    # Resource's dropdown
    EDIT_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(1)"))
    ASSIGN_USER_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(4)"))
    ASSIGN_TOKEN_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(5)"))
    ASSIGN_TOKEN_WITH_USER_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(6)"))
    DELETE_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(15)"))  # Will be 8 soon

    """"'Add Resource' dialog"""
    NAME_FLD_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid > div > div.modal input[name="resourceNameInput"]')
    )
    ATTEMPTS_FLD_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid > div > div.modal input[name="loginAttemptsBeforeLockInput"]')
    )
    IP_CHECKBOX_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal div.mb-3 > div.form-check")
    )
    IP_FLD_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal div.mt-2 input")
    )
    IP_BTN_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal div.mt-2 button")
    )
    FIRST_IP_ADD_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal div.px-3 a"))
    FIRST_IP_DELETE_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal div.px-3 i")
    )
    ENABLED_SWITCH_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal div.d-flex > div.form-check")
    )
    X_BTN_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal button.btn-close")
    )
    CANCEL_BTN_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal button.btn:nth-child(1)")
    )
    CREATE_BTN_ADD_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.modal div.modal-footer > button.btn:nth-child(2)")
    )

    """ 'Edit Resource' dialog"""
    NAME_FLD_EDIT_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid > div > div.row:nth-child(3) input[name="resourceNameInput"]')
    )
    ATTEMPTS_FLD_EDIT_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid > div > div.row input[name="loginAttemptsBeforeLockInput"]')
    )
    IP_CHECKBOX_EDIT_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.row div.mb-3 > div.form-check")
    )
    IP_FLD_EDIT_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "div.container-fluid > div > div.row div.mt-2 input"))
    IP_BTN_EDIT_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.row div.mt-2 button")
    )
    FIRST_IP_EDIT_RESOURCE = LocatorsProvider(web=(By.CSS_SELECTOR, "div.container-fluid > div > div.row div.px-3 a"))
    FIRST_IP_DELETE_EDIT_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.container-fluid > div > div.row div.px-3 i")
    )
    ENABLED_SWITCH_EDIT_RESOURCE = LocatorsProvider(
        web=(
            By.CSS_SELECTOR,
            'div.container-fluid > div > div.row div[id^="resource-modal"] div.d-flex > div.form-check',
        )
    )
    X_BTN_EDIT_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid > div > div.row div[id^="resource-modal"] button.btn-close')
    )
    CANCEL_BTN_EDIT_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid > div > div.row div[id^="resource-modal"] button.btn:nth-child(1)')
    )
    SAVE_BTN_EDIT_RESOURCE = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid > div > div.row div[id^="resource-modal"] button.btn:nth-child(2)')
    )

    @staticmethod
    def any_resource_id_link(row_number):
        any_resource_id_link = LocatorsProvider(
            web=(By.CSS_SELECTOR, f"tr:nth-child({str(row_number)}) div.media-body > div.justify-content-between a")
        )
        return any_resource_id_link

    @staticmethod
    def any_resource_ip(row_number, edit_resource=False):
        locator = f"div.container-fluid > div > div.row div.px-3 div.ip-address:nth-child({str(row_number)}) a" \
            if edit_resource else \
            f"div.container-fluid > div > div.modal div.px-3 div.ip-address:nth-child({str(row_number)}) a"
        any_resource_ip = LocatorsProvider(web=(By.CSS_SELECTOR, locator))
        return any_resource_ip
