from playwright.sync_api import expect, Locator
import allure
from pages.base_page import BasePage

class NewsListPage(BasePage):
    def open(self):
        self.navigate()
        self.page.wait_for_selector(".card", timeout=10000)
        return self

    def search(self, query: str):
        search_input = self.page.get_by_placeholder("Поиск...")
        search_input.fill(query)
        search_input.press("Enter")
        self.page.wait_for_timeout(5000)
        return self

    def click_news(self, title: str):
        self.page.get_by_text(title, exact=False).first.click()
        return self

    def should_have_news(self):
        expect(self.page.locator(".card").first).to_be_visible()
        return self

    def click_page(self, page_number: int):
        self.page.get_by_role("button", name=str(page_number), exact=True).click()
        expect(self.page.locator("button.join-item.btn.btn-primary")).to_have_text(str(page_number))
        return self

    def click_next(self):
        current_page = self.get_current_page()
        old_titles = self.get_card_titles()

        button = self.page.get_by_role("button", name="»")
        expect(button).to_be_enabled()
        button.click()

        expect(self.page.locator("button.join-item.btn.btn-primary")).not_to_have_text(str(current_page))
        expect(self.page.locator(".card h2 a")).not_to_have_text(old_titles)
        return self

    def click_previous(self):
        current_page = self.get_current_page()
        old_titles = self.get_card_titles()

        button = self.page.get_by_role("button", name="«")
        expect(button).to_be_enabled()
        button.click()

        expect(self.page.locator("button.join-item.btn.btn-primary")).not_to_have_text(str(current_page))
        expect(self.page.locator(".card h2 a")).not_to_have_text(old_titles)
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

    def check_word_in_card(self, cards, word):
        expect(cards.first).to_be_visible()
        count = cards.count()
        with allure.step("Проверка наличия слова в статье"):
            for i in range(count):
                card = cards.nth(i)

                title = self.get_card_title(card)
                subtitle = self.get_card_subtitle(card)
                text = self.get_card_text(card)
                tags = self.get_card_tags(card)

                card_content = " ".join([title, subtitle, text, *tags]).lower()
                assert word.lower() in card_content

    def check_buttons_on_start(self):
        expect(self.page.get_by_role("button", name="«")).to_be_disabled()
        expect(self.page.get_by_role("button", name="»")).to_be_enabled()