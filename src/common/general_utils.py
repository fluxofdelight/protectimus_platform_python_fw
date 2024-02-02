import allure

from src.ui.pages.base_page import BasePage


class GeneralUtils(BasePage):
    @allure.step("Verify the CSS property of the element")
    def verify_css_property(self, locator, css_value, css_property=None):
        css_property = css_property if css_property else "background-color"
        self.driver.ui_element(locator).with_(timeout=0.5).should(self.have.css_property(css_property, css_value))
        return self
