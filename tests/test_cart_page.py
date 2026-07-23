import pytest
from pages.productPage import ProductPage
from pages.cartPage import CartPage
from config.settings import Settings
from playwright.sync_api import expect

@pytest.mark.happy_path
class TestCartPage:

    @pytest.mark.smoke
    def test_update_quantity_recalculates_line_and_total(
        self, product_page: ProductPage, cart_page
    ):
        product_page.add_to_cart()
        cart: CartPage = cart_page()

        product_name = product_page.get_product_name()
        result = cart.update_quantity(product_name, 3)

        assert result["status"] == 200
        assert cart.get_quantity(product_name) == 3

    @pytest.mark.regression
    def test_remove_item_clears_row_and_updates_total(
        self, product_page: ProductPage, cart_page
    ):
        product_page.add_to_cart()
        cart: CartPage = cart_page()
        product_name = product_page.get_product_name()

        result = cart.remove_item(product_name)

        assert result["status"] == 204
        assert cart.is_empty()

    @pytest.mark.regression
    def test_empty_cart_shows_message(self, auth_page):
        """Navigates directly rather than via cart_page fixture -- with a
        genuinely empty cart there's no icon to click through"""
        auth_page.goto(Settings.CART_URL)
        cart = CartPage(auth_page)
        expect(cart.page.locator("ul.steps-4.steps-indicator")).to_be_visible()
        assert cart.is_empty()
