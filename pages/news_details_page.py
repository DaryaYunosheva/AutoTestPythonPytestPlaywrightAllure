from pages.base_page import BasePage
from playwright.sync_api import expect

class NewsDetailPage(BasePage):

    def add_comment(self, comment: str):
        self.page.get_by_role("textbox", name="Оставьте комментарий").fill(comment)
        self.page.get_by_role("button", name="Отправить").click()

    def get_comment(self, comment: str):
        return self.page.get_by_text(comment, exact=True)

    def get_comment_card(self, comment: str):
        return self.page.locator( ".card-body", has_text=comment)

    def get_comment_author(self, comment: str):
        comment_card = self.get_comment_card(comment)
        return comment_card.locator("span.font-semibold")

    def get_button(self):
        return self.page.get_by_role("button", name="Отправить")

    def check_comment(self, comment, new_user):
        expect(self.get_comment(comment)).to_be_visible()
        expect(self.get_comment_card(comment)).to_be_visible()
        expect(self.get_comment_author(comment)).to_have_text(f"{new_user.first_name} {new_user.last_name}")