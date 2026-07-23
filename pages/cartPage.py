import re
from pages.basePage import BasePage
from playwright.sync_api import expect
import allure


class CartPage(BasePage):
    """
    Cart page (/checkout, step 1).

    IMPORTANT -- unlike HomePage/ProductPage, this page does NOT fetch on
    load. Cart state is already held client-side (Angular store) from
    earlier add-to-cart calls, so there's no network response to sync
    against on navigation. Sync on DOM presence instead. Mutation actions
    (update qty, remove) DO fire real API calls and are synced on those.
    """

    def __init__(self, page):
        super().__init__(page)
        self.rows = self.page.locator("tbody tr")
        self.cart_total = self.page.get_by_test_id("cart-total")
        self.continue_shopping_btn = self.page.get_by_test_id("continue-shopping")
        self.proceed_checkout_btn = self.page.get_by_test_id("proceed-1")
        self.empty_cart_message = self.page.get_by_text("The cart is empty. Nothing to display.")

    def _line_item(self, product_name: str):
        """Row scoped to an EXACT product name match. Playwright's
        has_text does substring matching, so a plain string would let
        'Pliers' match 'Combination Pliers' -- anchor with regex."""
        title = self.page.get_by_test_id("product-title").filter(
            has_text=re.compile(rf"^{re.escape(product_name)}\s*$")
        )
        return self.rows.filter(has=title)

    def get_line_item_count(self) -> int:
        print(self.rows.count())
        return self.rows.count()

    def get_quantity(self, product_name: str) -> int:
        qty_input = self._line_item(product_name).get_by_test_id("product-quantity")
        return int(qty_input.input_value())

    def get_line_price(self, product_name: str) -> str:
        return self._line_item(product_name).get_by_test_id("line-price").text_content()

    def get_cart_total(self) -> str:
        return self.cart_total.text_content()

    def is_empty(self) -> bool:
        return self.get_line_item_count() == 0

    @allure.step("Update cart item quantity")
    def update_quantity(self, product_name: str, quantity: int) -> dict:
        """
        Fills quantity and blurs (Tab) -- confirmed the PUT only fires on
        blur/Enter, not per keystroke. Waits on the PUT for the status
        code, then waits for the rendered total to change as the settle
        signal (the app's internal GET /carts/{id} refetch isn't reliably
        interceptable as a second expect_response without a race).
        """
        previous_total = self.cart_total.text_content()
        qty_input = self._line_item(product_name).get_by_test_id("product-quantity")

        with self.page.expect_response(
            lambda r: "/product/quantity" in r.url and r.request.method == "PUT"
        ) as put_info:
            qty_input.fill(str(quantity))
            qty_input.press("Tab")

        expect(self.cart_total).not_to_have_text(previous_total)
        return {"status": put_info.value.status}

    @allure.step("Remove item from cart")
    def remove_item(self, product_name: str) -> dict:
        """
        Remove button is an icon-only <a class="btn btn-danger"> with no
        data-test attribute and no accessible name -- the one locator in
        the framework that falls back to a CSS class, scoped within the
        row, since the app gives us no better hook here.
        """
        row = self._line_item(product_name)
        with self.page.expect_response(
            lambda r: "/carts/" in r.url and r.request.method == "DELETE"
        ) as del_info:
            row.locator("a.btn.btn-danger").click()

        expect(row).to_have_count(0)
        return {"status": del_info.value.status}

    def get_subtotal(self) -> str | None:
        """Only rendered when a discount applies -- absent, not hidden,
        otherwise (matches cart-icon / empty-message pattern elsewhere)."""
        subtotal = self.page.get_by_test_id("cart-subtotal")
        return subtotal.text_content() if subtotal.count() > 0 else None

    def has_eco_discount(self) -> bool:
        return self.page.get_by_test_id("cart-eco-discount").count() > 0

    def get_eco_discount_amount(self) -> str | None:
        discount = self.page.get_by_test_id("cart-eco-discount")
        return discount.text_content() if discount.count() > 0 else None

    def get_eco_discount_percentage(self) -> float | None:
        """Percentage isn't in its own data-test cell -- it's embedded in
        the row label text ('Eco-Friendly Discount (5%)'), so parse it
        out via regex rather than adding a second locator strategy."""
        label = self.page.get_by_text(re.compile(r"Eco-Friendly Discount \(\d+%\)"))
        if label.count() == 0:
            return None
        match = re.search(r"\((\d+)%\)", label.text_content())
        return float(match.group(1)) if match else None

    @staticmethod
    def _parse_money(text: str) -> float:
        """Strips currency symbol, thousands separators, and the
        discount row's leading minus sign; returns absolute float."""
        cleaned = text.replace("$", "").replace(",", "").replace("-", "").strip()
        return float(cleaned)
