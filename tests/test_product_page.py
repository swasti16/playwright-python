import pytest
from pages.productPage import ProductPage
import allure


BUG_PRODUCTS = {
    "favorites_401": "01KX6C47BJBEXATVBP58NMCVA8",
    "cart_422_id_mismatch": "01KX7ZM9TCJXEJSEK5KH7ZE67R",
}


@pytest.mark.happy_path
class TestProductPageHappyPath:
    """Standard flow -- product_page auto-parametrized by pytest_generate_tests
    hook in conftest.py, sourced live from get_happy_path_product_ids()."""

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_to_cart_success(self, product_page: ProductPage):
        result = product_page.add_to_cart()
        assert result["status"] == 201
        assert "added" in result["toast_text"].lower()

    @pytest.mark.smoke
    def test_add_new_product_to_favorites(self, product_page: ProductPage):
        result = product_page.add_to_favorites()
        assert result["status"] == 201
        assert "added" in result["toast_text"].lower()

    @pytest.mark.regression
    def test_add_duplicate_product_to_favorites(self, product_page: ProductPage):
        product_page.add_to_favorites()
        result = product_page.add_to_favorites()
        assert result["status"] == 409


@pytest.mark.boundary
class TestProductPageBoundary:
    """Structurally different products -- edge attributes, not just 'another item'.
    product_page auto-parametrized from get_boundary_product_ids()."""

    @pytest.mark.regression
    def test_boundary_product_add_to_cart(self, product_page: ProductPage):
        result = product_page.add_to_cart()
        assert result["status"] == 201


class TestProductPageKnownBugs:
    """
    Pinned regression tests for confirmed application defects, found via
    exploratory testing. These assert CURRENT (broken) behavior so any
    change -- fix or regression -- is caught, not to endorse the bug.
    Intentionally hardcoded IDs -- pinning specific known defects, not
    sampling the catalog.
    """

    @pytest.mark.regression
    @pytest.mark.knownbugs
    @pytest.mark.parametrize(
        "product_page", [BUG_PRODUCTS["favorites_401"]], indirect=True
    )
    def test_favorites_unauthorized_on_specific_product(self, product_page: ProductPage):
        """Bug: valid session, /carts succeeds, /favorites returns 401
        on this specific product ID."""
        result = product_page.add_to_favorites()
        assert result["status"] == 401

    @pytest.mark.regression
    @pytest.mark.knownbugs
    @pytest.mark.parametrize(
        "product_page", [BUG_PRODUCTS["cart_422_id_mismatch"]], indirect=True
    )
    def test_add_to_cart_invalid_product_id_bug(self, product_page: ProductPage):
        """Bug: POST goes to /carts/{id} with a different, lowercase ID
        than the product's own uppercase ID -- suggests client-side ID
        resolution bug (cache/case mismatch)."""
        result = product_page.add_to_cart()
        assert result["status"] == 422
