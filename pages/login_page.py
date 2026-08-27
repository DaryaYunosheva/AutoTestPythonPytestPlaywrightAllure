from pages.base_page import BasePage
from playwright.sync_api import expect

class LoginPage(BasePage):
    def open(self):
        self.navigate("/login")
        self.page.wait_for_url("**/login", timeout=10000)
        return self

    def login(self, email:str, password:str):
        self.page.get_by_role("textbox", name="user@example.com").fill(f"{email}")
        self.page.get_by_role("textbox", name="••••••").fill(f"{password}")
        self.page.get_by_role("button", name="Войти").click()
        return self

    def check_button(self):
        add_news_button = self.page.get_by_role("link", name="Добавить новость")
        expect(add_news_button).to_be_visible(timeout=15000)