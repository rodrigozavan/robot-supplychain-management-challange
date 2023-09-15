from locators.AgentTerritoryLocators import AgentTerritoryLocators
from playwright.sync_api import Page
from settings import DOCS_DIR
from os import path


class AgentTerritoryPage(Page):
    def __init__(self, page: Page, url="https://developer.automationanywhere.com/challenges/automationanywherelabs-supplychainmanagement.html"):
        self._locators = AgentTerritoryLocators()
        self.page = page
        self._url = url
    
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def open(self) -> None:
        """
        Open the page based on the current url

        Args:

        Returns:
            None
        """
        self.page.goto(self.url)

    def download_workbook(self) -> str:
        """
        Download workbook with data from agent territory

        Args:

        Returns:
            str containing the full path to the workbook
        """
        with self.page.expect_download() as download_info:
            self.page.locator(self._locators.button_download).click()
        
        download = download_info.value
        full_path = path.join(DOCS_DIR, download.suggested_filename)
        download.save_as(full_path)

        return full_path

        