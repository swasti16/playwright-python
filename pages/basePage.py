from playwright.sync_api import Page, expect, Locator


class BasePage:
    """Base page class that provides common methods for all pages."""
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def to_be_visible(self, locator):
        expect(locator).to_be_visible()

    def click(self, locator: Locator):
        self.to_be_visible(locator)
        locator.click()

    def fill(self, locator: Locator, text: str):
        self.to_be_visible(locator)
        locator.fill(text)

    def get_by_role(self, role: str, name: str = None, **kwargs):
        return self.page.get_by_role(role, name=name, **kwargs)

    def get_by_text(self, text: str = None, **kwargs):
        return self.page.get_by_text(text=text, **kwargs)
