from pages.basePage import BasePage


class NavBar(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.toolshop_heading = self.get_by_role("link", name="Practice Software Testing - Toolshop")
        self.home_link = self.get_by_role("link", name="Home")
        self.categories_btn = self.get_by_role("button", name="Categories")
        self.language_btn = self.get_by_role("button", name="Select language")
        self.cart_link = self.get_by_role("link", name="cart")
        self.contact_link = self.get_by_role("link", name="Contact")
