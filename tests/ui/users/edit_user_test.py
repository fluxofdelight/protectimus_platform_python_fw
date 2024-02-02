import allure
import pytest


@allure.suite("Edit user tests")
class TestEditUser:
    @pytest.mark.regress
    def test_edit_first_user(self, users_page, global_):
        """
        Steps:
            1. Go to the "Users" page
            2. Click the "Three dots" button of the first user
            3. Click the "Edit" button in the drop-down
            4. Fill in all fields in the "Edit User" dialog with another values
            5. Click on the "Save" button
            6. Verify the text in the toast
            7. Verify updated data of the user on the "Users" page
            8. Open the "Edit User" dialog again
            9. Verify an alias and that user has a password

        Expected result:
            1. User info has been updated
        """
        login = "two"
        alias = "test"
        password = "12345678"
        first_name = "Bill"
        last_name = "Lib"
        email = "test@test.co"
        phone = "1234567890"
        first_user_login = users_page.get_first_user_login()
        (
            users_page.verify_first_user_login(first_user_login).edit_first_user(
                login=login,
                alias=alias,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )
        )
        # Add check via DB instead
        (
            users_page.verify_user_edit(login)
            .verify_first_user_login(login)
            .verify_first_user_full_name(first_name, last_name)
            .verify_first_user_email(email)
            .verify_first_user_phone(phone)
            .click_three_dots_button_first_user()
            .click_edit_button_first_user()
            .verify_first_user_alias(alias)
            .verify_first_user_has_password()
        )
