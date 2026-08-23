import allure
import logging
import pytest
from helpers.data_for_tests import user2
from pages import news_details_page
from pages.news_details_page import NewsDetailPage
from helpers.data_generator import generate_comment
from playwright.sync_api import expect, Page

logger = logging.getLogger("Comments")
@allure.epic("Комментарии")
@allure.feature("Комментарии")
class TestDetailsNews:
    @allure.story("Создание комментария")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка добавления комментария к новости")
    @pytest.mark.positive
    def test_add_comment(self, auth_page):
        logger.info("Начало теста: Создание комментария")
        news_detail_page = NewsDetailPage(auth_page)
        comment = generate_comment()

        with allure.step("Открытие новости"):
            news_detail_page.navigate("/news/240")

        with allure.step("Добавление комментария"):
            news_detail_page.add_comment(comment)
        with allure.step("Перезагрузка страницы"):
            news_detail_page.page.reload()

        with allure.step("Проверка комментария"):
            comment_text = news_detail_page.page.get_by_text(comment, exact=True)
            expect(comment_text).to_be_visible()
            comment_card = auth_page.locator(".card-body",has_text=comment)
            expect(comment_card).to_be_visible()
            expect(comment_card.locator("span.font-semibold")).to_have_text(f"{user2.first_name} {user2.last_name}")
        logger.info("Тест завершен успешно")


    @allure.story("Комментарии у неавторизованных пользователей")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка комментирования у неавторизованного пользователя")
    @pytest.mark.negative
    def test_comment_no_login(self, page: Page):
        logger.info("Начало теста: Проверка комментирования у неавторизованного пользователя")
        news_detail_page = NewsDetailPage(page)
        with allure.step("Открытие новости"):
            news_detail_page.navigate("/news/240")
        with allure.step("Проверка отсутствия кнопки для отправки комментария"):
            expect(news_detail_page.page.get_by_role("button", name="Отправить")).not_to_be_visible()
        logger.info("Тест завершен успешно")

