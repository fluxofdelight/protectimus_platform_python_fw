import pytest

from src.common.entry_data import EntryData
from src.db.pages.resources.resources_page import ResourcesPageDB
from src.ui.pages.resources.resources_page import ResourcesPage


@pytest.fixture(scope="class", autouse=True)
def resources_page(driver):
    yield ResourcesPage(driver)


@pytest.fixture(scope="class", autouse=True)
def db():
    yield ResourcesPageDB()


@pytest.fixture(scope="class", autouse=True)
def entry_data():
    yield EntryData()


@pytest.fixture(scope="class", autouse=True)
def open_resources_page(global_):
    yield global_.open_resources_page()
