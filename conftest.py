import re

import pytest
import logging
import allure
from playwright.sync_api import Browser, BrowserContext, Page, expect
from pathlib import Path
from helpers.data_for_tests import user2, User
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from helpers.data_generator import generate_user
from pages.register_page import RegisterPage

BASE_URL = ''
ARTIFACTS_DIR = Path("artifacts")
TRACES_DIR = ARTIFACTS_DIR / "traces"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"

logger = logging.getLogger(__name__)

for directory in [ARTIFACTS_DIR, TRACES_DIR, SCREENSHOTS_DIR, VIDEOS_DIR]:
    directory.mkdir(parents = True, exist_ok = True)

@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser, request):
    test_name = request.node.name
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru_RU",
        record_video_dir =  str(VIDEOS_DIR)
    )

    context.tracing.start(screenshots=True, snapshots=True, sources= True)
    context._test_name = test_name
    context._test_failed = False
    yield context

    if context._test_failed:
        trace_path = TRACES_DIR / f"{test_name}.zip"
        context.tracing.stop(path=str(trace_path))
        allure.attach.file(str(trace_path), "Playwright trace", attachment_type=allure.attachment_type.ZIP)
        logger.info(f"Результат теста {test_name} сохранен")
    else:
        context.tracing.stop()

    video_path = VIDEOS_DIR / f"{test_name}.webm"
    if context._test_failed and video_path.exists():
        allure.attach.file(str(video_path), "Video", attachment_type=allure.attachment_type.WEBM)
    elif video_path.exists():
        video_path.unlink()

    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    page = context.new_page()
    page.set_default_timeout(15000)

    yield page

    rep_call = getattr(request.node, "rep_call", None)

    if rep_call and rep_call.failed:
        context._test_failed = True
        screenshot_path = SCREENSHOTS_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        allure.attach.file(str(screenshot_path), "Screenshot", attachment_type=allure.attachment_type.PNG)
        logger.info(f"Скриншот сохранен: {screenshot_path}")
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="function", autouse=True)
def allure_setup(request):
    test_name = request.node.name.replace("test_", "").replace("_", " ").title()
    allure.dynamic.title(test_name)
    #if request.node.docstring:
      #  allure.dynamic.description(request.node.docstring)
    docstring = request.function.__doc__
    if docstring:
        allure.dynamic.description(docstring.strip())


@pytest.fixture(scope="function")
def new_user(page: Page):
    user = User(**generate_user())
    RegisterPage(page).open().register( user.first_name, user.last_name, user.email, user.phone, user.password)
    expect(page, "Неудачная попытка регистрации пользователя").to_have_url(re.compile(".*/login"))

    logger.info(f"Зарегистрирован пользователь {user.email}")
    return user

@pytest.fixture(scope="function")
def auth_page(page: Page, new_user: User):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(new_user.email, new_user.password)
    expect(page.get_by_role("link", name="Добавить новость")).to_be_visible()
    return page

@pytest.fixture
def profile_page(auth_page):
    return(ProfilePage(auth_page).open())