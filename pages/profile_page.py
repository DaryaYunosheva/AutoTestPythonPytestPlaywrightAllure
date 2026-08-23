from pages.base_page import BasePage

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


