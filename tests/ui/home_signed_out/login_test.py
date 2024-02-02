import allure
import pytest

from src.common import string_utils as s


@allure.suite("Home page login tests")
class TestLogin:
    @pytest.mark.regress
    def test_default_login(self, home_signed_out_page, home_signed_in_page, project_config):
        """
        Steps:
            1. Open the Home page with a signed-out user
            2. Enter an existing email
            3. Enter a valid password
            4. Click on the login button
            5. Verify that login was successful

        Expected result:
            1. Opens the Home page with a signed-in user and login has been successful
        """
        email = project_config.web.email
        password = project_config.web.password
        home_signed_out_page.login(email, password)
        home_signed_in_page.verify_client_email(email)

    @pytest.mark.negative
    def test_login_with_invalid_password(self, home_signed_out_page, project_config):
        """
        Steps:
            1. Open the Home page with a signed-out user
            2. Enter an existing email
            3. Enter an invalid password
            4. Click on the login button
            5. Verify the error message

        Expected result:
            1. Appears the error message and login has been successful
        """
        email = project_config.web.email
        password = s.random_password()
        (
            home_signed_out_page.fill_in_login_email(email)
            .fill_in_password(password)
            .click_login_button()
            .verify_error_message()
        )
