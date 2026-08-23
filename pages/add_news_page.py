
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

