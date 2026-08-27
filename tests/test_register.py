import logging
import allure
import pytest
from playwright.sync_api import Page, expect
from helpers.data_generator import generate_user
from pages.register_page import RegisterPage

logger = logging.getLogger("TestRegister")

@allure.epic("Аутентификация")
@allure.feature("Регистрация")
class TestRegister:

    @allure.story("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Проверка, что пользователь может успешно зарегистрироваться на платформе")
    @pytest.mark.positive
    def test_register_new_user_success(self, page: Page):
        logger.info("Начало теста: Регистрация нового пользователя")
        register_page = RegisterPage(page)
        register_page.open()

        user_data = generate_user()
        logging.debug(f"Сгенерирован новый пользователь: {user_data['email']}")
        register_page.register(
            user_data['first_name'], user_data['last_name'], user_data['email'], user_data['phone'],
            user_data['password']
        )
        with allure.step("Проверка редиректа /login"):
            register_page.check_redirect()
        logger.info("Тест завершен успешно")

    @allure.story("Регистрация зарегистрированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что пользователь не сможет повторно зарегистрироваться на платформе")
    @pytest.mark.negative
    def test_reregister_user(self, page: Page):
        logger.info("Начало теста: Регистрация зарегистрированного пользователя")
        register_page = RegisterPage(page)
        register_page.open()

        user_data = generate_user()
        register_page.register(
            user_data['first_name'], user_data['last_name'], "test@example.com", user_data['phone'],
            "password123"
        )
        with allure.step("Проверка ошибки"):
            register_page.should_see_text("Email already registered")
        logger.info("Тест завершен успешно")

    @allure.story("Регистрация с невалидной почтой")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что пользователь не сможет зарегистрироваться с некорректной почтой")
    @pytest.mark.negative
    @pytest.mark.xfail
    def test_register_wrong_email(self, page: Page):
        logger.info("Начало теста: Регистрация нового пользователя с невалидной почтой")
        register_page = RegisterPage(page)
        register_page.open()

        user_data = generate_user()
        register_page.register(
            user_data['first_name'], user_data['last_name'], "test@e", user_data['phone'],
            "password123"
        )
        with allure.step("Проверка ошибки"):
            register_page.should_see_error()
        logger.info("Тест завершен успешно")