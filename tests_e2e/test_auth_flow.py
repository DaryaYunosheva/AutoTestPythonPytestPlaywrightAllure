import pytest
import logging
import allure
from playwright.sync_api import Page, expect
from helpers.data_generator import generate_user
from pages.register_page import RegisterPage
from pages.login_page import LoginPage

logger = logging.getLogger("TestAuthFlow")

@allure.epic("Аутентификация")
@allure.feature("Регистрация/Вход")
class TestAuthFlow:

    @allure.story("Полный цикл регистрации и авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка полного цикла: регистрации нового пользователя, редирект на страницу входа и успешная авторизация")
    @pytest.mark.positive
    def test_full_cycle_auth(self, page: Page):
        logger.info("Начало теста: Полный цикл авторизации")

        user_data = generate_user()
        logging.debug(f"Сгенерирован новый пользователь: {user_data['email']}")

        register_page = RegisterPage(page)
        login_page = LoginPage(page)

        with allure.step("Открыть страницу регистрации"):
            register_page.navigate("/register")
        with allure.step("Зарегистрировать нового пользователя"):
            register_page.register(
                user_data['first_name'], user_data['last_name'], user_data['email'], user_data['phone'],
                user_data['password']
            )
        with allure.step("Проверка редиректа /login"):
            page.wait_for_url("**/login", timeout=10000)
            assert "/login" in page.url

        with allure.step("Выполнить вход зарегистрированного пользователя"):
            login_page.open()
            login_page.login(user_data['email'], user_data['password'])

        with allure.step("Проверка успешной авторизации"):
            add_news_button = page.get_by_role("link", name="Добавить новость")
            expect(add_news_button).to_be_visible(timeout=10000)
        register_page.take_screenshot("full_cycle_auth_success.png")
        logger.info("Тест завершен успешно")