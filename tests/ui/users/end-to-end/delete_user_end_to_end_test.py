import allure
import pytest


@allure.suite("User deleting end-to-end tests")
class TestDeleteUserEndToEnd:
    @pytest.mark.smoke
    def test_delete_user_by_login_using_search(self, users_page, global_, entry_data, db):
        """
        Steps:
            1. Go to the "Users" page
            2. Enter the login of user in the "Search" field
            3. Press the "Enter" key
            4. Verify the founded user
            5. Click the "Three dots" button of the first user
            6. Click the "Delete" button in the dropdown
            7. Verify the text in the deletion dialog
            8. Click the "Yes" button in the dialog for deletion
            9. Verify the deletion toast
            10. Verify the deletion of user in the DB

        Expected result:
            1. Deletion dialog closes, appears a toast about successful deletion
               and user disappears from the list
        """
        global_.search_objects(entry_data.user_login_to_delete)
        (
            users_page.verify_first_user_login(entry_data.user_login_to_delete)
            .delete_first_user(entry_data.user_login_to_delete)
            .verify_user_deletion(entry_data.user_login_to_delete)
        )
        assert not db.get_all_user_info_by_login(
            entry_data.user_login_to_delete
        ), f"User '{entry_data.user_login_to_delete}' wasn't deleted"
