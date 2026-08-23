import logging
import allure
import pytest
from playwright.sync_api import Page, expect
from helpers.data_for_tests import user1
from helpers.data_generator import generate_news
from pages.add_news_page import AddNewsPage

logger = logging.getLogger("News")

@allure.epic("Новости")
@allure.feature("Создание новости")
class TestAddNews:

    @allure.story("Создание новости с корректными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что пользователь может создать новость, заполнив все поля")
    @pytest.mark.positive
    def test_add_news_success(self, auth_page):
        logger.info("Начало теста: Создание новости")
        add_new_page = AddNewsPage(auth_page)
        add_new_page.open()
        new_data = generate_news()
        logging.debug(f"Сгенерирована новая статья")
        with allure.step("Создание статьи"):
            add_new_page.create_new(new_data["title"], new_data["subtitle"], new_data["text"], new_data["tags"])

        with allure.step("Проверка редиректа"):
            auth_page.wait_for_url("**/", timeout=20000)
            auth_page.reload()
            assert f"{add_new_page.base_url}/"==auth_page.url

        with allure.step("Проверка наличия новости"):
            card = add_new_page.get_news_card(new_data["title"])
            expect(card).to_be_visible()
            expect(card).to_contain_text(new_data["subtitle"][:10])
            expect(card).to_contain_text(new_data["text"][:10])
            expect(card).to_contain_text(user1.first_name)
            expect(card).to_contain_text(user1.last_name)
        logger.info("Тест завершен успешно")


    @allure.story("Создание новости с пустым заголовком")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что новость не создастся с пустым заголовком")
    @pytest.mark.negative
    def test_add_news_wrong_title(self, auth_page):
        logger.info("Начало теста: Создание новости с пустым заголовком")
        add_new_page = AddNewsPage(auth_page)
        add_new_page.open()
        new_data = generate_news()
        logging.debug(f"Сгенерирована новая статья")
        with allure.step("Создание статьи"):
            add_new_page.create_new("", new_data["subtitle"], new_data["text"], new_data["tags"])
        with allure.step("Проверка, что пользователь остался на странице создания"):
            expect(auth_page).to_have_url(f"{add_new_page.base_url}/news/create")
        logger.info("Тест завершен успешно")


    @allure.story("Создание новости с заголовком состоящим только из пробелов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что новость не создастся с заголовком из пробелов")
    @pytest.mark.xfail
    @pytest.mark.negative
    def test_add_news_probel_title(self, auth_page):
        logger.info("Начало теста: Создание новости с заголовком из пробелов")
        add_new_page = AddNewsPage(auth_page)
        add_new_page.open()
        new_data = generate_news()
        logging.debug(f"Сгенерирована новая статья")
        with allure.step("Создание статьи"):
            add_new_page.create_new("       ", new_data["subtitle"], new_data["text"], new_data["tags"])
        with allure.step("Проверка, что пользователь остался на странице создания"):
            button = add_new_page.page.get_by_role("button", name="Создать")
            expect(button).to_be_visible(timeout=10000)
            expect(add_new_page.page).to_have_url(f"{add_new_page.base_url}/news/create", timeout=30000)
        logger.info("Тест завершен успешно")


    @allure.story("Создание новости с пустым текстом")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("")
    @pytest.mark.negative
    def test_add_news_wrong_text(self, auth_page):
        logger.info("Начало теста: Создание новости с пустым текстом")
        add_new_page = AddNewsPage(auth_page)
        add_new_page.open()
        new_data = generate_news()
        logging.debug(f"Сгенерирована новая статья")
        with allure.step("Создание статьи"):
            add_new_page.create_new(new_data["title"], new_data["subtitle"], "", new_data["tags"])
        with allure.step("Проверка, что пользователь остался на странице создания"):
            expect(auth_page).to_have_url(f"{add_new_page.base_url}/news/create")
        logger.info("Тест завершен успешно")


    @allure.story("Создание новости с текстом состоящим только из пробелов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что новость не создастся с текстом из пробелов")
    @pytest.mark.xfail
    @pytest.mark.negative
    def test_add_news_probel_text(self, auth_page):
        logger.info("Начало теста: Создание новости с текстом из пробелов")
        add_new_page = AddNewsPage(auth_page)
        add_new_page.open()
        new_data = generate_news()
        logging.debug(f"Сгенерирована новая статья")
        with allure.step("Создание статьи"):
            add_new_page.create_new(new_data["title"], new_data["subtitle"], "      ", new_data["tags"])
        with allure.step("Проверка, что пользователь остался на странице создания"):
            button = add_new_page.page.get_by_role("button", name="Создать")
            expect(button).to_be_visible(timeout=10000)
            expect(add_new_page.page).to_have_url(f"{add_new_page.base_url}/news/create", timeout=30000)
        logger.info("Тест завершен успешно")