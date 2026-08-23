import pytest
import logging
import allure
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from helpers.data_for_tests import user1

logger = logging.getLogger("TestLogin")

@allure.epic("Аутентификация")
@allure.feature("Вход")
class TestLogin:

    @allure.story("Вход с существующим пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Проверка, что пользователь может войти с корректными данными")
    @pytest.mark.positive
    def test_logging_success(self, page: Page):
        logger.info("Начало теста: Авторизация с корректными данными")
        login_page = LoginPage(page)
        login_page.open()
        with allure.step("Авторизация пользователя"):
            login_page.login(user1.email, user1.password)
        with allure.step("Проверка редиректа"):
            add_news_button = page.get_by_role("link", name="Добавить новость")
            expect(add_news_button).to_be_visible(timeout=15000)
        logger.info("Тест завершен успешно")

    @allure.story("Вход с некорректным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что пользователь не войдет с неверным паролем")
    @pytest.mark.negative
    def test_login_password_wrong(self, page: Page):
        logger.info("Начало теста: Авторизация с неверным паролем")
        login_page = LoginPage(page)
        login_page.open()
        with allure.step("Авторизация пользователя"):
            login_page.login("test@example.com", "wrong_password")
        with allure.step("Проверка отображения ошибки"):
            login_page.should_see_error()
        logger.info("Тест завершен успешно")

    @allure.story("Вход с некорректной почтой")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что система не даст войти пользователю с некорректной почтой")
    @pytest.mark.negative
    def test_login_email_wrong(self, page: Page):
        logger.info("Начало теста: Авторизация с невалидной почтой")
        login_page = LoginPage(page)
        login_page.open()
        with allure.step("Авторизация пользователя"):
            login_page.login("wrong@w", "password123")
        with allure.step("Проверка отображения ошибки"):
            login_page.should_see_error()
        logger.info("Тест завершен успешно")

    @allure.story("Вход с незарегистрированным пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что пользователь не может зайти без регистрации")
    @pytest.mark.negative
    def test_login_not_user(self, page: Page):
        logger.info("Начало теста: Авторизация незарегистрированного пользователя")
        login_page = LoginPage(page)
        login_page.open()
        with allure.step("Авторизация пользователя"):
            login_page.login("wrong@wrong.com", "password123")
        with allure.step("Проверка отображения ошибки"):
            login_page.should_see_error()
        logger.info("Тест завершен успешно")