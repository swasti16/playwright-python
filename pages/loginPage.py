from playwright.sync_api import Page
from pages.basePage import BasePage


class LoginPage(BasePage):
    """Login page class that provides methods specific to the login page."""
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = self.get_by_role("textbox", "Email address")
        self.password_input = self.get_by_role("textbox", "Password")
        self.login_button = self.get_by_role("button", "Login")

    def login(self, username: str, password: str):
        """Performs the login action."""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
