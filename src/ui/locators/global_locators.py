from selenium.webdriver.common.by import By

from src.ui.locators.locators_provider import LocatorsProvider


class GlobalLocators:

    """Top navbar"""
    CLIENT_EMAIL = LocatorsProvider(web=(By.CSS_SELECTOR, "a.header-dropdown-toggle"))

    """Sidebar"""
    USERS_BUTTON = LocatorsProvider(web=(By.CSS_SELECTOR, "div.side-bar-wrapper > ul > li:nth-child(1)"))
    TOKENS_BUTTON = LocatorsProvider(web=(By.CSS_SELECTOR, "div.side-bar-wrapper > ul > li:nth-child(2)"))
    RESOURCES_BUTTON = LocatorsProvider(web=(By.CSS_SELECTOR, "div.side-bar-wrapper > ul > li:nth-child(3)"))
    ADMINS_BUTTON = LocatorsProvider(web=(By.CSS_SELECTOR, "div.side-bar-wrapper > ul > li:nth-child(4)"))

    """Header"""
    NUM_OF_OBJECTS = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.quota-card-body > div:nth-child(2) > div:nth-child(2)")
    )  # div.sparkline-box-content
    # Top pagination
    LEFT_DOUBLE_ARROW_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, "div.my-2 li.page-item:nth-child(1)"))
    LEFT_ARROW_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, "div.my-2 li.page-item:nth-last-child(2)"))
    RIGHT_ARROW_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, "div.my-2 li.page-item:nth-last-child(3)"))
    RIGHT_DOUBLE_ARROW_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, "div.my-2 li.page-item:nth-last-child(2)"))
    # Bottom pagination
    LEFT_DOUBLE_ARROW_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, "div.mb-2 li.page-item:nth-child(1)"))
    LEFT_ARROW_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, "div.mb-2 li.page-item:nth-last-child(2)"))
    RIGHT_ARROW_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, "div.mb-2 li.page-item:nth-last-child(3)"))
    RIGHT_DOUBLE_ARROW_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, "div.mb-2 li.page-item:nth-last-child(2)"))
    # Top dropdown to set up a number of objects displayed in the table
    ELEMENTS_NUM_TOP_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "div.my-2 select.form-select"))
    OPTION_5_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.my-2 select.form-select > option[value="5"]'))
    OPTION_10_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.my-2 select.form-select > option[value="10"]'))
    OPTION_15_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.my-2 select.form-select > option[value="15"]'))
    OPTION_20_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.my-2 select.form-select > option[value="20"]'))
    OPTION_25_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.my-2 select.form-select > option[value="25"]'))
    OPTION_50_TOP = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.my-2 select.form-select > option[value="50"]'))
    # Bottom dropdown
    ELEMENTS_NUM_BTM_DROPDOWN = LocatorsProvider(web=(By.CSS_SELECTOR, "div.mb-2 select.form-select"))
    OPTION_5_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.mb-2 select.form-select > option[value="5"]'))
    OPTION_10_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.mb-2 select.form-select > option[value="10"]'))
    OPTION_15_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.mb-2 select.form-select > option[value="15"]'))
    OPTION_20_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.mb-2 select.form-select > option[value="20"]'))
    OPTION_25_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.mb-2 select.form-select > option[value="25"]'))
    OPTION_50_BTM = LocatorsProvider(web=(By.CSS_SELECTOR, 'div.mb-2 select.form-select > option[value="50"]'))
    # Filter
    SEARCH_FIELD = LocatorsProvider(web=(By.CSS_SELECTOR, 'input[type="search"]'))
    FILTERS_ACCORDION = LocatorsProvider(web=(By.CSS_SELECTOR, "span.pointer"))
    APPLY_BTN_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, "button.me-2"))
    CLEAR_BTN_FILTER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.col-md-12 > button.btn-sm:not(button.me-2)"))

    """Modals"""
    TOAST_CONTAINER = LocatorsProvider(web=(By.CSS_SELECTOR, "div.toast-container"))
    # Delete dialog
    CENTER_DIALOG = LocatorsProvider(web=(By.CSS_SELECTOR, "div.modal-dialog-centered > div.modal-content"))
    DELETE_DIALOG_NO_BTN = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.modal-dialog-centered > div.modal-content div.col-md-6:nth-child(1)")
    )
    DELETE_DIALOG_YES_BTN = LocatorsProvider(
        web=(By.CSS_SELECTOR, "div.modal-dialog-centered > div.modal-content div.col-md-6:nth-child(2)")
    )
