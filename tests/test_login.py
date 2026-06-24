from pages.loginPage import LoginPage


class TestLogin:
    def test_page_locators(self, login_page: LoginPage):
        login_page.to_be_visible(login_page.get_by_role("link", "Contact"))
        login_page.to_be_visible(login_page.get_by_role("button", "Categories"))
        login_page.to_be_visible(login_page.get_by_role("button", "Select language"))
        login_page.to_be_visible(login_page.get_by_role("button", "Sign in with Google"))

    def test_valid_login(self, login_page: LoginPage):
        login_page.login("customer@practicesoftwaretesting.com", "welcome01")
        login_page.to_be_visible(login_page.get_by_role("button", name="Jane Doe"))

    def test_invalid_login(self, login_page: LoginPage):
        login_page.login("wrong@email.com", "wrongpass")
        login_page.to_be_visible(login_page.get_by_text("Invalid email or password"))

    def test_invalid_email_format(self, login_page: LoginPage):
        login_page.login("wrong", "wrongpass")
        login_page.to_be_visible(login_page.get_by_text("Email format is invalid"))
