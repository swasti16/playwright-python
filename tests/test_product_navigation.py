from pages.homePage import HomePage
from pages.productPage import ProductPage
from playwright.sync_api import expect


class TestProductNavigation:
    def test_clicking_product_card_opens_correct_product(self, home_page: HomePage):
        """
        Integration test: verifies the home page grid links route to a
        valid product page. Separate from ProductPage functional tests --
        this ONLY tests navigation/routing, not product page behavior.
        """
        first_card_name = home_page.get_product_names()[0]
        home_page.product_cards.first.click()

        product_page = ProductPage(home_page.page)
        expect(product_page.product_name).to_have_text(first_card_name)