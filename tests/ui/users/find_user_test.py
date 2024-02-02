import allure
import pytest


@allure.suite("User searching tests")
class TestFilterUser:
    @pytest.mark.regress
    def test_search_user_by_login(self, users_page, global_, entry_data):
        """
        Steps:
            1. Go to the "Users" page
            2. Enter the login of user in the "Search" field
            3. Press the "Enter" key
            4. Verify that expected login displays on the "Users" page

        Expected result:
            1. Search of user by login via the "Search" field was successful
        """
        global_.search_objects(entry_data.user_login_to_search)
        users_page.verify_first_user_login(entry_data.user_login_to_search)

    @pytest.mark.regress
    def test_filter_user_by_all_filters(self, users_page, users_page_locators, global_, entry_data):
        """
        Steps:
            1. Go to the "Users" page
            2. Enter the login of user in the "Search" field
            3. Press the "Enter" key
            4. Clear the "Search" field
            5. Disable the "API support" of the founded user
            6. Open filters
            7, Fill in "Login", "Email", "ID", "First Name", "Second Name" fields
            8. Select the "Blocked by Administrator" option in the "Block" dropdown
            9. Click on the "Apply" button
            10. Verify filtered user credentials

        Expected result:
            1. User was successfully filtered with all filters (except "Resource")
        """
        (
            global_
            .search_objects(entry_data.user_login_filter)
            .clear_search_field()
        )
        (
            users_page
            .verify_first_user_login(entry_data.user_login_filter)
            .block_first_user()
        )
        users_page.filter_users(
            entry_data.user_login_filter,
            entry_data.user_email_filter,
            entry_data.user_id_filter,
            entry_data.user_fname_filter,
            entry_data.user_lname_filter,
            True,
            users_page_locators.OPTION_BLOCKED_BY_ADMIN_DROP,
        )
        (
            users_page.verify_first_user_login(entry_data.user_login_filter)
            .verify_first_user_full_name(entry_data.user_fname_filter, entry_data.user_lname_filter)
            .verify_first_user_email(entry_data.user_email_filter)
            .verify_first_user_id_via_full_url(entry_data.user_id_filter)
            .verify_first_user_blocked()
        )
