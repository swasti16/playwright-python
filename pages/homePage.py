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
        self.prev_page_button = page.get_by_role("button", name="previous")

    def search_for_item(self, item_name: str):
        self.search_input.fill(item_name)
        self.wait_for_products_response(self.search_button.click)

    def filter_by_category(self, category_name: str):
        self.wait_for_products_response(
            lambda: self.page.get_by_label(category_name).check()
        )

    def select_sort_option(self, label: str):
        self.wait_for_products_response(
            lambda: self.sort_dropdown.select_option(label=label)
        )

    def go_to_page(self, page_number: int):
        self.wait_for_products_response(
            lambda: self.page.get_by_role("button", name=f"Page-{page_number}").click()
        )

    def click_next_page(self):
        self.wait_for_products_response(self.next_page_button.click)

    def adjust_max_price_handle(self, arrow_presses: int, direction: str = "left"):
        self.price_slider_max.focus()
        key = "ArrowLeft" if direction == "left" else "ArrowRight"

        def press_all():
            for _ in range(arrow_presses):
                self.price_slider_max.press(key)

        self.wait_for_products_response(press_all)

    def get_product_names(self) -> list[str]:
        names = self.product_cards.get_by_test_id("product-name").all_inner_texts()
        return [n.strip() for n in names]

    def get_product_prices(self) -> list[float]:
        prices = self.product_cards.get_by_test_id("product-price").all_inner_texts()
        return [float(p.replace("$", "").strip()) for p in prices]

    def get_co2_rating_badge(self) -> list[float]:
        return self.product_cards.locator(".co2-letter.active").text_content()

    def is_page_active(self, page_number: int) -> bool:
        active_item = self.page.locator(".page-item.active")
        return active_item.inner_text().strip() == str(page_number)

    def get_current_max_price_value(self) -> float:
        bubble = self.page.locator(".ngx-slider-model-high")
        return float(bubble.inner_text().strip())
