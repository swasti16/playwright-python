import pytest
from playwright.sync_api import sync_playwright, expect
from pages.loginPage import LoginPage

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch()
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    yield page


@pytest.fixture
def login_page(page):
    login_page = LoginPage(page)
    login_page.navigate('https://practicesoftwaretesting.com/')
    expect(login_page.get_by_role("link", name="Practice Software Testing - Toolshop")).to_be_visible()
    sign_in_link = login_page.get_by_role("link", name="Sign in")
    expect(sign_in_link).to_be_visible()
    sign_in_link.click()
    yield login_page
