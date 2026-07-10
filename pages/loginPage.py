from playwright.sync_api import Page
from pages.basePage import BasePage


class LoginPage(BasePage):
    """Login page class that provides methods specific to the login page."""
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = self.get_by_role("textbox", "Email address")
        self.password_input = self.get_by_role("textbox", "Password")
        self.login_button = self.get_by_role("button", "Login")

    def user_button(self, username: str):
        return self.get_by_role("button", name=username)

    def login_and_wait_for_profile(self, email: str, password: str):
        """Performs login and waits for the /users/me fetch that only
        fires on successful auth. Use for valid-credential login flows."""
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.wait_for_response(lambda: self.click(self.login_button), "/users/me")

    def login(self, email: str, password: str):
        """Performs the login action."""
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.login_button)
