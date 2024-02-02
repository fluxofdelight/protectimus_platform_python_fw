import allure
import pytest


@allure.suite("Resource deleting tests")
class TestDeleteResource:
    @pytest.mark.regress
    def test_delete_first_resource(self, resources_page, db):
        """
        Steps:
            1. Go to the "Resources" page
            2. Get first resource name from DB
            3. Click the "Three dots" button of the first resource
            4. Click the "Delete" button in the dropdown
            5. Verify the text in the deletion dialog
            6. Click the "Yes" button in the dialog for deletion
            7. Verify the deletion toast
            8. Verify the deletion of resource in the DB
            9. Verify that another resource name doesn't match with deleted one, or if there are
                no resource created

        Expected result:
            1. Deletion dialog closes, appears a toast about successful deletion
               and resource disappears from the list
        """
        first_resource_name = db.get_first_resource_name()
        (resources_page.delete_first_resource().verify_resource_deletion(first_resource_name))
        assert not db.get_all_resource_info_by_resource_name(
            first_resource_name
        ), f"Resource '{first_resource_name}' wasn't deleted"

        another_resource_name = db.get_first_resource_name()
        if another_resource_name:
            assert another_resource_name != first_resource_name, "Resource wasn't deleted"
        else:
            print("No resources created\nPASSED")
