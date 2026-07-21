from pages.basePage import BasePage
from playwright.sync_api import expect
import allure


class ProductPage(BasePage):
    def __init__(self, page, product_id: str | None = None):
        super().__init__(page)
        self.product_id = product_id
        self.product_name = self.page.get_by_test_id("product-name")
        self.unit_price = self.page.get_by_test_id("unit-price")
        self.description = self.page.get_by_test_id("product-description")
        self.quantity_input = page.get_by_role("spinbutton", name="Quantity")
        self.decrease_qty_btn = self.page.get_by_role("button", name="Decrease quantity")
        self.increase_qty_btn = self.page.get_by_role("button", name="Increase quantity")
        self.add_to_cart_btn = self.page.get_by_role("button", name="Add to cart ")
        self.add_to_favorites_btn = self.page.get_by_role("button", name=" Add to favourites ")
        self.add_to_compare_btn = self.page.get_by_role("button", name=" Compare ")
        self.alert_toast = self.page.get_by_role("alert")

    def _wait_for_clean_toast_state(self, timeout: int = 6000) -> None:
        """Waits for any lingering toast to fully detach before the next
        action. Prevents strict-mode violations when the previous toast's
        fade-out animation overlaps with a new toast appearing (e.g. two
        rapid favorites clicks -- 201 then 409)."""
        expect(self.alert_toast).to_have_count(0, timeout=timeout)

    @allure.step("Add product to cart")
    def add_to_cart(self) -> dict:
        self._wait_for_clean_toast_state()
        with self.page.expect_response(
            lambda r: "/carts" in r.url and r.request.method == "POST"
        ) as response_info:
            self.add_to_cart_btn.click()

        response = response_info.value
        expect(self.alert_toast).to_be_visible()
        toast_text = self.alert_toast.text_content()

        return {"status": response.status, "toast_text": toast_text}

    @allure.step("Add product to favorites")
    def add_to_favorites(self) -> dict:
        self._wait_for_clean_toast_state()
        with self.page.expect_response(
            lambda r: "/favorites" in r.url and r.request.method == "POST"
        ) as response_info:
            self.add_to_favorites_btn.click()

        response = response_info.value
        expect(self.alert_toast).to_be_visible()
        toast_text = self.alert_toast.text_content()

        return {"status": response.status, "toast_text": toast_text}
