import allure
import pytest


@allure.suite("User deleting tests")
class TestDeleteUser:
    @pytest.mark.regress
    def test_delete_first_user(self, users_page, db):
        """
        Steps:
            1. Go to the "Users" page
            2. Get first user in the list or create, if there are no users
            3. Verify that user exists in the DB
            4. Click the "Three dots" button of the first user
            5. Click the "Delete" button in the dropdown
            6. Verify the text in the deletion dialog
            7. Click the "Yes" button in the dialog for deletion
            8. Verify the deletion toast
            9. Verify the deletion of user in the DB
            10. Verify that another user login doesn't match with deleted one, or if there are
                no users created

        Expected result:
            1. Deletion dialog closes, appears a toast about successful deletion
               and user disappears from the list
        """
        first_user_login = users_page.get_first_user_and_create_if_not_exist()

        assert db.get_all_user_info_by_login(first_user_login), f"User '{first_user_login}' wasn't created"
        (
            users_page
            .delete_first_user()
            .verify_user_deletion(first_user_login)
        )
        assert not db.get_all_user_info_by_login(first_user_login), f"User '{first_user_login}' wasn't deleted"

        another_user_login = users_page.get_first_user_login()
        if another_user_login:
            assert another_user_login != first_user_login, "User wasn't deleted"
        else:
            print("No users created\nPASSED")
