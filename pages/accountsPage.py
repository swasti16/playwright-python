from pages.basePage import BasePage
from components.navBar import NavBar


class AccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.navbar = NavBar(page)  # composed, not inherited
        self.favorites_button = self.get_by_role("button", name="Favorites")
        self.profile_button = self.get_by_role("button", name="Profile")
        self.invoices_button = self.get_by_role("button", name="Invoices")
        self.messages_button = self.get_by_role("button", name="Messages")
