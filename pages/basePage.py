from playwright.sync_api import Page, expect, Locator


class BasePage:
    """Base page class that provides common methods for all pages."""
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def to_be_visible(self, locator, **kwargs):
        expect(locator).to_be_visible(**kwargs)

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

    def _wait_for_response(self, action, endpoint, method):
        """
        Playwright's auto-waiting covers element actionability, not async
        data fetches. This app re-fetches the product list from the API
        on every search/sort/filter/paginate action — we must wait for
        that specific network response before reading the DOM, or we
        read stale/empty state. Avoids blind sleeps; only waits as long
        as the actual request takes.
        """
        with self.page.expect_response(lambda r: endpoint in r.url and r.request.method == method and r.ok):
            action()

    def wait_for_products_response(self, action):
        self._wait_for_response(action, "/products", "QUERY")
