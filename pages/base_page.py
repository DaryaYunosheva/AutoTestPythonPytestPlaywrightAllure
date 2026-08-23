from pathlib import Path

import allure
import logging
from playwright.sync_api import Page, expect

logger = logging.getLogger("BasePage")

class BasePage:
    def __init__(self, page: Page, base_url:str = "https://archiscope.ru"):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = "/"):
        url = self.base_url + path
        logger.info(f"Переход на страницу {url}")

        with allure.step(f"Переход на страницу: {url}"):
            self.page.goto(f"{url}", timeout=30000)
            self.page.wait_for_load_state("networkidle")
        logger.info(f"Страница загружена: {url}")
        return self

    def get_title(self) -> str:
        return self.page.title()

    def take_screenshot(self, name:str):
        screenshot_path = f"artifacts/screenshots/{name}.png"
        Path("artifacts/screenshot").mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"Сделан скриншот: {screenshot_path}")
        allure.attach.file(str(screenshot_path), name=name, attachment_type="image/png")


    def should_see_text(self, text:str):
        expect(self.page.get_by_text(text)).to_be_visible(timeout=10000)
        return self

    def should_see_button(self, name:str):
        expect(self.page.get_by_role("button", name = name)).to_be_visible()
        return self

    def should_see_error(self):
        expect(self.page.locator(".alert-error")).to_be_visible(timeout=10000)
        return self
