from selenium.webdriver.common.by import By

from src.ui.locators.locators_provider import LocatorsProvider


class UsersPageLocators:

    ADD_USER_BUTTON = LocatorsProvider(web=(By.CSS_SELECTOR, "a.btn"))

    """Filter"""
    # Fields
    LOGIN_FLD_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.p-3 > div:nth-child(1) input.form-control"))
    EMAIL_FLD_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.p-3 > div:nth-child(2) input.form-control"))
    ID_FLD_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, 'input[type="number"]'))
    FIRST_NAME_FLD_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.p-3 > div:nth-child(4) input.form-control"))
    LAST_NAME_FLD_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.p-3 > div:nth-child(5) input.form-control"))
    RESOURCE_FLD_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.p-3 > div:nth-child(7) input.form-control"))
    BLOCK_DROPDOWN_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.p-3 select.form-select"))
    # Block dropdown options
    OPTION_EMPTY_DROP = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.p-3 select.form-select > option:nth-child(1)")
    )
    OPTION_NOT_BLOCKED_DROP = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.p-3 select.form-select > option:nth-child(2)")
    )
    OPTION_BLOCKED_BY_ADMIN_DROP = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.p-3 select.form-select > option:nth-child(3)")
    )
    OPTION_INVALID_LOGIN_DROP = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.p-3 select.form-select > option:nth-child(4)")
    )
    OPTION_INVALID_OTP_DROP = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.p-3 select.form-select > option:nth-child(5)")
    )
    OPTION_INVALID_EMAIL_DROP = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.p-3 select.form-select > option:nth-child(6)")
    )
    OPTION_INVALID_PIN_DROP = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.p-3 select.form-select > option:nth-child(7)")
    )

    # First user in the table
    AVATAR_LINK_FIRST_USER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.media-aside img.avatar"))
    LOGIN_LINK_FIRST_USER = LocatorsProvider(web=(By.CSS_SELECTOR, "span.text-muted > a"))
    NAME_FIRST_USER = LocatorsProvider(web=(By.CSS_SELECTOR, "span.float-start"))
    EMAIL_FIRST_USER = LocatorsProvider(web=(By.CSS_SELECTOR, "td.ps-4 > span:nth-child(1)"))
    PHONE_FIRST_USER = LocatorsProvider(web=(By.CSS_SELECTOR, "td.ps-4 > span:nth-child(3)"))
    CREATOR_LINK_FIRST_USER = LocatorsProvider(web=(By.CSS_SELECTOR, "td:nth-child(3) > a"))
    API_FIRST_USER = LocatorsProvider(web=(By.CSS_SELECTOR, 'input[role="switch"]'))
    THREE_DOTS_FIRST_USER = LocatorsProvider(web=(By.CSS_SELECTOR, "i.fa-ellipsis-v"))

    # User's dropdown
    EDIT_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(1)"))
    ASSIGN_NEW_TOKEN_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(3)"))
    ASSIGN_EXIST_TOKEN_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(4)"))
    DELETE_BTN_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "ul.show > li:nth-child(6)"))

    """"Add User dialog"""
    # Fields
    LOGIN_FLD_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(4) input[name="login"]')
    )
    ALIAS_FLD_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(4) input[name="alias"]')
    )
    PASS_FLD_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(4) input[name="password"]')
    )
    PASS_CONF_FLD_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(4) input[name="passwordConfirmation"]')
    )
    FIRST_NAME_FLD_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(4) input[name="firstName"]')
    )
    LAST_NAME_FLD_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(4) input[name="lastName"]')
    )
    EMAIL_FLD_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(4) input[name="email"]')
    )
    PHONE_FLD_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(4) input[name="phoneNumber"]')
    )
    # Buttons
    X_BTN_ADD_USER = LocatorsProvider(
        web=(
            By.CSS_SELECTOR,
            'div.container-fluid div[id^="userModal"]:nth-child(4) div.modal-header > button.btn-close',
        )
    )
    CANCEL_BTN_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div[id^="userModal"]:nth-child(4) button.btn:nth-child(1)')
    )
    CREATE_BTN_ADD_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div[id^="userModal"]:nth-child(4) button.btn:nth-child(2)')
    )

    """ 'Edit User' dialog"""
    # Fields
    LOGIN_FLD_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(3) input[name="login"]')
    )
    ALIAS_FLD_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(3) input[name="alias"]')
    )
    PASS_FLD_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(3) input[name="password"]')
    )
    PASS_CONF_FLD_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(3) input[name="passwordConfirmation"]')
    )
    FIRST_NAME_FLD_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(3) input[name="firstName"]')
    )
    LAST_NAME_FLD_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(3) input[name="lastName"]')
    )
    EMAIL_FLD_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(3) input[name="email"]')
    )
    PHONE_FLD_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div:nth-child(3) input[name="phoneNumber"]')
    )
    # Buttons
    X_BTN_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div[id^="userModal"]:nth-child(2) button.btn-close')
    )
    CANCEL_BTN_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div[id^="userModal"]:nth-child(2) button.btn:nth-child(1)')
    )
    SAVE_BTN_EDIT_USER = LocatorsProvider(
        web=(By.CSS_SELECTOR, 'div.container-fluid div[id^="userModal"]:nth-child(2) button.btn:nth-child(2)')
    )

    @staticmethod
    def any_user_login_link(row_number):
        any_user_login_link = LocatorsProvider(
            web=(By.CSS_SELECTOR, f"tr:nth-child({str(row_number)}) span.text-muted > a")
        )
        return any_user_login_link
