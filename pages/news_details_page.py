from pages.base_page import BasePage


class NewsDetailPage(BasePage):

    def add_comment(self, comment: str):
        self.page.get_by_role("textbox", name="Оставьте комментарий").fill(comment)
        self.page.get_by_role("button", name="Отправить").click()