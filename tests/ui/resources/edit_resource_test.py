import allure
import pytest


@allure.suite("Edit resource tests")
class TestEditResource:
    @pytest.mark.regress
    def test_edit_first_resource(self, resources_page, global_):
        resource_name = "new_resource"
        attempts = 5
        ips = ["5.5.5.5", "9.9.9.9", "7.7.7.7"]

        (
            resources_page.edit_first_resource(
                name=resource_name, attempts=attempts, ip_verif_enable=True, ips=ips, disable_resource=True
            )
        )
