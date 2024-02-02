import allure
import pytest


@allure.suite("Resource searching tests")
class TestFilterResource:
    @pytest.mark.regress
    def test_search_resource_by_name(self, resources_page, global_, entry_data):
        """
        Steps:
            1. Go to the "Resources" page
            2. Enter the name of resource in the "Search" field
            3. Press the "Enter" key
            4. Verify that expected login displays on the "Resources" page

        Expected result:
            1. Search of resource by name via the "Search" field was successful
        """
        global_.search_objects(entry_data.resource_name_to_search)
        resources_page.verify_first_resource_name(entry_data.resource_name_to_search)

    @pytest.mark.regress
    def test_filter_user_by_all_filters(self, resources_page, global_, entry_data):
        """
        Steps:
            1. Go to the "Resources" page
            2. Enter the name of resource in the "Search" field
            3. Press the "Enter" key
            4. Clear the "Search" field
            5. Open filters
            6. Fill in "Name" field
            7. Fill in "ID" field
            8. Click on the "Apply" button
            9. Verify filtered resource name and ID

        Expected result:
            1. Resource was successfully filtered with all filters
        """
        global_.search_objects(entry_data.resource_name_filter).clear_search_field()
        (
            resources_page.verify_first_resource_name(entry_data.resource_name_filter)
            .filter_resources(entry_data.resource_name_to_search, entry_data.resource_id_filter)
            .verify_first_resource_name(entry_data.resource_name_filter)
            .verify_first_resource_id(entry_data.resource_id_filter)
        )
