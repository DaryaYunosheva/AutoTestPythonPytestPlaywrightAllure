from playwright.sync_api import Page, expect
from pages.news_list_page import NewsListPage
import allure
import logging
import pytest

logger = logging.getLogger("TestNewsList")

@allure.epic("Новости")
@allure.feature("Список новостей")
class TestNewsList:
    @allure.story("Отображение списка")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка загрузки списка новостей")
    @pytest.mark.positive
    def test_news_list_load(self, page: Page):
        logger.info("Начало теста: Отображение списка")
        news_list = NewsListPage(page)
        news_list.open()
        news_list.should_have_news()
        logger.info("Тест завершен успешно")

    @allure.story("Поиск")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка поиска новостей по ключевому слову")
    @pytest.mark.positive
    def test_news_search(self, page: Page):
        logger.info("Начало теста: Поиск новостей по ключевому слову")
        news_list = NewsListPage(page)
        news_list.open()
        word = "Банк"
        with allure.step("Поиск новостей по заданному слову"):
            news_list.search(word)
            cards = news_list.get_cards()
        news_list.check_word_in_card(cards, word)

        logger.info("Тест завершен успешно")

    @allure.story("Пагинация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка перехода вперед и назад между страницами")
    @pytest.mark.positive
    def test_pagination_next_previous(self, page: Page):
        logger.info("Начало теста: Переход вперед и назад между страницами")
        news_page = NewsListPage(page)
        news_page.open()

        with allure.step("Проверка корректного отображения кнопок на начальной странице"):
            news_page.check_buttons_on_start()

        with allure.step("Сохранение данных начальной страницы"):
            start_page = news_page.get_current_page()
            first_list = news_page.get_card_titles()

        with allure.step("Переход на следующую страницу"):
            news_page.click_next()


        with allure.step("Сохранение данных новой страницы"):
            second_list = news_page.get_card_titles()
            end_page = news_page.get_current_page()

        with allure.step("Проверка, что переход был совершен"):
            assert start_page!=end_page
            assert first_list!=second_list

        with allure.step("Переход на предыдущую страницу"):
            news_page.click_previous()

        with allure.step("Сохранение данных новой страницы"):
            last_list = news_page.get_card_titles()
            last_page = news_page.get_current_page()

        with allure.step("Проверка, что был переход на начальную страницу"):
            assert first_list == last_list
            assert last_page == start_page

        logger.info("Тест завершен успешно")


    @allure.story("Пагинация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка перехода на страницу по номеру")
    @pytest.mark.positive
    def test_pagination_number(self, page: Page):
        logger.info("Начало теста: Переход на страницу по номеру")
        news_page = NewsListPage(page)
        news_page.open()

        with allure.step("Сохранение данных начальной страницы"):
            start_page = news_page.get_current_page()
            first_list = news_page.get_card_titles()

        with allure.step("Переход на страницу с номером 2"):
            news_page.click_page(2)

        with allure.step("Сохранение данных новой страницы"):
            second_list = news_page.get_card_titles()
            end_page = news_page.get_current_page()

        with allure.step("Проверка, что переход был совершен"):
            assert start_page != end_page
            assert first_list != second_list

        with allure.step("Переход на страницу 1"):
            news_page.click_page(1)

        with allure.step("Сохранение данных новой страницы"):
            last_list = news_page.get_card_titles()
            last_page = news_page.get_current_page()

        with allure.step("Проверка, что был переход на начальную страницу"):
            assert first_list == last_list
            assert last_page == start_page

        logger.info("Тест завершен успешно")


