from pages.base_page import BasePage

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