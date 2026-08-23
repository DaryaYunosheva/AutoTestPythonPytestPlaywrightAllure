from pages.base_page import BasePage

class RegisterPage(BasePage):
    def open(self):
        self.navigate("/register")
        return self

    def register(self, firstname:str, lastname:str, email:str, phone:str, password:str):
        self.page.locator("input[name=\"first_name\"]").fill(firstname)
        self.page.locator("input[name=\"last_name\"]").fill(lastname)
        self.page.locator("input[name=\"email\"]").fill(email)
        self.page.locator("input[name=\"phone\"]").fill(phone)
        self.page.locator("input[name=\"password\"]").fill(password)
        self.page.get_by_role("button", name="Зарегистрироваться").click(timeout=10000)
        return self