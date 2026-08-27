from pages.base_page import BasePage
import allure
from playwright.sync_api import expect
class ProfilePage(BasePage):

    def open(self):
        self.navigate("/profile")
        return self

    def update_profile(self, firstname=None, lastname=None, email=None, phone=None,  password=None):
        if firstname is not None:
            self.page.locator("input[name=\"first_name\"]").fill(firstname)

        if lastname is not None:
            self.page.locator("input[name=\"last_name\"]").fill(lastname)

        if email is not None:
            self.page.locator("input[name=\"email\"]").fill(email)

        if phone is not None:
            self.page.locator("input[name=\"phone\"]").fill(phone)

        if password is not None:
            self.page.locator("input[name=\"password\"]").fill(password)

        self.page.get_by_role("button", name="Сохранить").click()
        return self

    def should_have_profile(self,new_user):
        with allure.step("Проверка имени"):
            self.check_one("first_name", new_user.first_name)
        with allure.step("Проверка фамилии"):
            self.check_one("last_name", new_user.last_name)
        with allure.step("Проверка почты"):
            self.check_one("email", new_user.email)
        with allure.step("Проверка телефона"):
            self.check_one("phone", new_user.phone)


    def check_one(self, typ: str, word):
        element = self.page.locator(f"input[name=\"{typ}\"]")
        expect(element).to_have_value(word)
