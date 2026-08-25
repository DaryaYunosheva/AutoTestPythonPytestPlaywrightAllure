import allure
import logging
import pytest
from pages.add_news_page import AddNewsPage
from pages.news_details_page import NewsDetailPage
from helpers.data_generator import generate_comment, generate_news
from playwright.sync_api import expect, Page

from pages.news_list_page import NewsListPage

logger = logging.getLogger("Comments")
@allure.epic("Комментарии")
@allure.feature("Комментарии")
class TestDetailsNews:

    @allure.story("Создание комментария")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка добавления комментария к новости")
    @pytest.mark.positive
    def test_add_comment(self, auth_page, new_user):
        logger.info("Начало теста: Создание комментария")
        news_page = NewsListPage(auth_page)
        add_news_page = AddNewsPage(auth_page)
        news_detail_page = NewsDetailPage(auth_page)
        comment = generate_comment()
        news = generate_news()

        with allure.step("Генерация и открытие новости"):
            add_news_page.open().create_new(**news)
            news_page.open().click_news(news["title"])

        with allure.step("Добавление комментария"):
            news_detail_page.add_comment(comment)

        with allure.step("Перезагрузка страницы"):
            news_detail_page.page.reload()

        with allure.step("Проверка комментария"):
            expect(news_detail_page.get_comment(comment)).to_be_visible()
            expect(news_detail_page.get_comment_card(comment)).to_be_visible()
            expect(news_detail_page.get_comment_author(comment)).to_have_text(f"{new_user.first_name} {new_user.last_name}")

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
            expect(news_detail_page.get_button()).not_to_be_visible()
        logger.info("Тест завершен успешно")

