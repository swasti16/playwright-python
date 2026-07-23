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

    def is_cart_icon_present(self) -> bool:
        """Confirmed via recon: cart icon doesn't render at all when the
        cart is empty (not just hidden) -- no element, no API call."""
        return self.cart_link.count() > 0
