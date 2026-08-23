from playwright.sync_api import expect, Locator

from pages.base_page import BasePage

class NewsListPage(BasePage):
    def open(self):
        self.navigate()
        return self

    def search(self, query: str):
        search_input = self.page.get_by_placeholder("Поиск...")
        search_input.fill(query)
        search_input.press("Enter")
        return self

    def click_news(self, title: str):
        self.page.get_by_text(title, exact=False).first.click()
        return self

    def should_have_news(self):
        expect(self.page.locator(".card").first).to_be_visible()
        return self

    def click_page(self, page_number: int):
        self.page.get_by_role("button", name=str(page_number), exact=True).click()
        return self

    def click_next(self):
        self.page.get_by_role("button", name="»").click()
        return self

    def click_previous(self):
        self.page.get_by_role("button", name="«").click()
        return self

    def get_card_titles(self):
        return self.page.locator(".card h2 a").all_inner_texts()

    def get_current_page(self):
        return int(self.page.locator("button.join-item.btn.btn-primary").inner_text())

    def get_cards(self):
        return self.page.locator(".card")

    def get_card_title(self, card: Locator):
        return card.locator("h2.card-title a").inner_text()

    def get_card_subtitle(self, card: Locator):
        return card.locator("h2.card-title + p").inner_text()

    def get_card_text(self, card: Locator):
        return card.locator("h2.card-title + p + p").inner_text()

    def get_card_tags(self, card: Locator):
        return card.locator(".badge").all_inner_texts()
