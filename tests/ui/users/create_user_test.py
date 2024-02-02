import allure
import pytest

from src.common import string_utils as s


@allure.suite("User creating tests")
class TestCreateUser:
    @pytest.mark.regress
    def test_create_user(self, users_page, db, user_login=("user_" + s.random_name())):
        """
        Steps:
            1. Go to the "Users" page
            2. Click on the "Add" button
            3. Fill in the "Login" field  in the "Add User" dialog
            4. Fill in the "First Name" field
            5. Fill in the "Last Name" field
            6. Click on the "Create" button
            7. Verify that the user was created

        Expected result:
            1. "Add User" dialog closes, appears a toast about successful creation
               and user appears in the list
        """
        (
            users_page
            .create_valid_user(user_login)
            .verify_user_creating(user_login)
            .verify_first_user_login(user_login)
        )
        assert db.get_all_user_info_by_login(user_login), f"User '{user_login}' wasn't created"
