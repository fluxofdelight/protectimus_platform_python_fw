import allure
import pytest

from src.common import string_utils as s


@allure.suite("Resource creating tests")
class TestCreateResource:
    @pytest.mark.regress
    def test_create_resource(self, resources_page, db, resource_name=("resource_" + s.random_name())):
        """
        Steps:
            1. Go to the "Resources" page
            2. Click on the "Add" button
            3. Fill in the "Resource Name" field  in the "Add resource" dialog
            4. Click on the "Create" button
            5. Verify that the resource was created

        Expected result:
            1. "Add Resource" dialog closes, appears a toast about successful creation
               and resource appears in the list
        """
        (
            resources_page.create_valid_resource(resource_name)
            .verify_resource_creating(resource_name)
            .verify_first_resource_name(resource_name)
        )
        assert db.get_all_resource_info_by_resource_name(resource_name), f"Resource '{resource_name}' wasn't created"

    def test_create_resource_with_ip_verification(
        self, resources_page, db, resource_name=("resource_" + s.random_name())
    ):
        """
        Steps:
            1. Go to the "Resources" page
            2. Click on the "Add" button
            3. Fill in the "Resource Name" field  in the "Add resource" dialog
            4. Click on the "Create" button
            5. Verify that the resource was created

        Expected result:
            1. "Add Resource" dialog closes, appears a toast about successful creation
               and resource appears in the list
        """
        ips = ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
        (
            resources_page.create_valid_resource(resource_name, ip_enabled=True, ips=ips)
            .verify_resource_creating(resource_name)
            .verify_first_resource_name(resource_name)
            .verify_ips_first_resource(ips)
        )
        assert db.get_all_resource_info_by_resource_name(resource_name), f"Resource '{resource_name}' wasn't created"
        ips_db = db.get_resource_ips_by_resource_name(resource_name)
        assert ips_db == ",".join(ips), f"Resource IPs ({ips_db}) don't match with expected IPs ({ips})"
