import allure
import pytest
import logging
from playwright.sync_api import expect

from helpers.data_generator import generate_email

logger = logging.getLogger("TestProfile")

@allure.epic("Профиль")
@allure.feature("Проверка/Изменение данных профиля")
class TestProfile:

    @allure.story("Проверка данных")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка данных")
    @pytest.mark.positive
    def test_profile_data(self, profile_page, new_user):
        logger.info("Начало теста: Проверка данных")
        profile_page.should_have_profile(new_user)
        logger.info("Тест завершен успешно")

    @allure.story("Изменение имени")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Изменение имени на валидное значение")
    @pytest.mark.positive
    def test_change_first_name(self, profile_page):
        logger.info("Начало теста: Изменение имени")
        new = "NewName"
        profile_page.update_profile(firstname=new)
        profile_page.page.reload()

        expect(profile_page.get_input("first_name")).to_have_value(new)
        logger.info("Тест завершен успешно")

    @allure.story("Изменение имени")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Изменение имени на невалидное значение")
    @pytest.mark.negative
    def test_change_first_empty_name(self, profile_page, new_user):
        logger.info("Начало теста: Изменение имени")
        first_name = new_user.first_name
        new = ""
        profile_page.update_profile(firstname=new)
        profile_page.page.reload()

        expect(profile_page.get_input("first_name")).to_have_value(first_name)
        logger.info("Тест завершен успешно")

    @allure.story("Изменение фамилии")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Изменение фамилии на валидное значение")
    @pytest.mark.positive
    def test_change_last_name(self, profile_page):
        logger.info("Начало теста: Изменение фамилии")
        new = "NewLastName"
        profile_page.update_profile(lastname=new)
        profile_page.page.reload()

        expect(profile_page.get_input("last_name")).to_have_value(new)
        logger.info("Тест завершен успешно")

    @allure.story("Изменение фамилии")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Изменение фамилии на невалидное значение")
    @pytest.mark.negative
    def test_change_last_empty_name(self, profile_page, new_user):
        logger.info("Начало теста: Изменение фамилии")
        last_name = new_user.last_name
        new = ""
        profile_page.update_profile(lastname=new)
        profile_page.page.reload()

        expect(profile_page.get_input("last_name")).to_have_value(last_name)
        logger.info("Тест завершен успешно")

    @allure.story("Изменение почты")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Изменение почты на валидное значение")
    @pytest.mark.positive
    def test_change_email(self, profile_page):
        logger.info("Начало теста: Изменение почты")
        new = generate_email()
        profile_page.update_profile(email=new)
        profile_page.page.reload()

        expect(profile_page.get_input("email")).to_have_value(new)
        logger.info("Тест завершен успешно")

    @allure.story("Изменение почты")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Изменение почты на невалидное значение")
    @pytest.mark.negative
    def test_change_email_empty(self, profile_page, new_user):
        logger.info("Начало теста: Изменение почты")
        email = new_user.email
        new = ""
        profile_page.update_profile(email=new)
        profile_page.page.reload()

        expect(profile_page.get_input("email")).to_have_value(email)
        logger.info("Тест завершен успешно")

    @allure.story("Изменение номера телефона")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Изменение номера телефона на валидное значение")
    @pytest.mark.positive
    def test_change_phone(self, profile_page):
        logger.info("Начало теста: Изменение номера телефона")
        new = "89993334422"
        profile_page.update_profile(phone=new)
        profile_page.page.reload()

        expect(profile_page.get_input("phone")).to_have_value(new)
        logger.info("Тест завершен успешно")

    @allure.story("Изменение номера телефона")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Изменение номера телефона на невалидное значение")
    @pytest.mark.negative
    def test_change_phone_empty(self, profile_page, new_user):
        logger.info("Начало теста: Изменение номера телефона")
        phone = new_user.phone
        new = ""
        profile_page.update_profile(phone=new)
        profile_page.page.reload()

        expect(profile_page.get_input("phone")).to_have_value(phone)
        logger.info("Тест завершен успешно")