from playwright.sync_api import Playwright, sync_playwright
from pages.AgentTerritoryPage import AgentTerritoryPage
from utils.workbook_headler import workbook_data_to_dict
import json


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    agent_territory = AgentTerritoryPage(page)
    agent_territory.open()

    full_path_workbook = agent_territory.download_workbook()

    data_workbook = workbook_data_to_dict(full_path_workbook)

    with open("data_workbook.json", mode="w", encoding="utf-8") as file:
        file.write(json.dumps(data_workbook, ensure_ascii=False))

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
