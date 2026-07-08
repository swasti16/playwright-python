from playwright.sync_api import Page
from pages.basePage import BasePage
from components.navBar import NavBar


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.navbar = NavBar(page)
        # 1. Search & Sort
        self.search_input = page.get_by_role("textbox", name="Search")
        self.search_button = page.get_by_role("button", name="Search")
        self.sort_dropdown = page.get_by_role("combobox", name="Sort")

        # 2. Filters
        self.price_slider_min = page.get_by_role("slider", name="ngx-slider")
        self.price_slider_max = page.get_by_role("slider", name="ngx-slider-max")

        # 3. Product Grid
        self.product_cards = page.locator(".card")

        # 4. Pagination
        self.next_page_button = page.get_by_role("button", name="next")

    def search_for_item(self, item_name: str):
        self.search_input.fill(item_name)
        self.search_button.click()

    def filter_by_category(self, category_name: str):
        self.page.get_by_label(category_name).check()
