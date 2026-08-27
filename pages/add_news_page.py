from playwright.sync_api import expect
from pages.base_page import BasePage

class AddNewsPage(BasePage):

    def open(self):
        self.navigate("/news/create")
        return self

    def create_new(self, title: str, subtitle: str, text: str, tags: str):
        self.page.locator("input[name=\"title\"]").fill(title)
        self.page.locator("input[name=\"subtitle\"]").fill(subtitle)
        self.page.locator("textarea[name=\"text\"]").fill(text)
        self.page.get_by_role("textbox", name="технологии, наука, спорт").fill(tags)
        self.page.get_by_role("button", name="Создать").click()
        return self

    def get_news_card(self, title):
        return self.page.locator(".card").filter(has_text=title)

    def get_create_button(self):
        return self.page.get_by_role("button", name="Создать")

    def check_redirect(self):
        self.page.wait_for_url("**/", timeout=20000)
        self.page.reload()
        assert f"{self.base_url}/" == self.page.url

    def check_new(self, new_data, new_user):
        card = self.get_news_card(new_data["title"])
        expect(card).to_be_visible()
        expect(card).to_contain_text(new_data["subtitle"][:10])
        expect(card).to_contain_text(new_data["text"][:10])
        expect(card).to_contain_text(new_user.first_name)
        expect(card).to_contain_text(new_user.last_name)

    def check_not_redirect(self):
        expect(self.get_create_button()).to_be_visible(timeout=10000)
        expect(self.page).to_have_url(f"{self.base_url}/news/create", timeout=20000)