from pages.basePage import BasePage
from playwright.sync_api import expect
import allure
from config.settings import Settings


class ProductPage(BasePage):
    def __init__(self, page, product_id: str | None = None):
        super().__init__(page)
        self.product_id = product_id
        self._created_cart_ids: list[str] = []
        self._created_favorite_ids: list[str] = []
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

        data = {}
        try:
            data = response.json()
        except Exception:
            pass
        cart_id = data.get("id") or response.url.rstrip("/").split("/")[-1]
        self._created_cart_ids.append(cart_id)

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

    # def cleanup(self) -> None:
    #     """Best-effort teardown -- deletes any cart/favorite resources this
    #     instance created. Failures are logged, not raised, so a cleanup
    #     issue never masks or fails the actual test result."""
    #     headers = self.get_auth_header()
    #     self.page.pause()
    #     for cart_id in self._created_cart_ids:
    #         try:
    #             self.page.request.delete(
    #                 f"{Settings.API_BASE_URL}/carts/{cart_id}", headers=headers
    #             )
    #         except Exception as e:
    #             print(f"[cleanup] Failed to delete cart {cart_id}: {e}")

    #     for fav_id in self._created_favorite_ids:
    #         try:
    #             self.page.request.delete(
    #                 f"{Settings.API_BASE_URL}/favorites/{fav_id}", headers=headers
    #             )
    #         except Exception as e:
    #             print(f"[cleanup] Failed to delete favorite {fav_id}: {e}")

    #     self._created_cart_ids.clear()
    #     self._created_favorite_ids.clear()
    def cleanup(self) -> None:
        print("[cleanup] started")
        print("[cleanup] page closed:", self.page.is_closed())
        print("[cleanup] created carts:", self._created_cart_ids)
        print("[cleanup] created favorites:", self._created_favorite_ids)

        if not self._created_cart_ids and not self._created_favorite_ids:
            print("[cleanup] nothing to delete")
            return

        headers = self.get_auth_header()

        for cart_id in self._created_cart_ids:
            print(f"[cleanup] deleting cart {cart_id}")
            try:
                resp = self.page.request.delete(
                    f"{Settings.API_BASE_URL}/carts/{cart_id}",
                    headers=headers,
                )
                print(f"[cleanup] cart delete status: {resp.status}")
            except Exception as e:
                print(f"[cleanup] cart delete failed: {e}")

        for fav_id in self._created_favorite_ids:
            print(f"[cleanup] deleting favorite {fav_id}")
            try:
                resp = self.page.request.delete(
                    f"{Settings.API_BASE_URL}/favorites/{fav_id}",
                    headers=headers,
                )
                print(f"[cleanup] favorite delete status: {resp.status}")
            except Exception as e:
                print(f"[cleanup] favorite delete failed: {e}")

        print("[cleanup] finished")
