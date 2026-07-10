import pytest
from pages.homePage import HomePage


class TestHomePageSearch:
    @pytest.mark.smoke
    def test_search_returns_relevant_products(self, home_page: HomePage):
        home_page.search_for_item("Pliers")
        names = home_page.get_product_names()
        assert len(names) > 0, "Search returned no results for a known product"
        assert all("pliers" in n.lower() for n in names), f"Irrelevant results: {names}"

    @pytest.mark.regression
    def test_search_no_results_for_nonsense_query(self, home_page: HomePage):
        home_page.search_for_item("zzzznonexistentproductzzzz")
        assert home_page.product_cards.count() == 0


class TestHomePageSort:
    @pytest.mark.regression
    @pytest.mark.parametrize("label,reverse", [
        ("Name (A - Z)", False),
        ("Name (Z - A)", True),
    ])
    def test_sort_by_name(self, home_page: HomePage, label, reverse):
        home_page.select_sort_option(label)
        names = home_page.get_product_names()
        assert names == sorted(names, key=str.lower, reverse=reverse)

    @pytest.mark.regression
    @pytest.mark.parametrize("label,reverse", [
        ("Price (Low - High)", False),
        ("Price (High - Low)", True),
    ])
    def test_sort_by_price(self, home_page, label, reverse):
        home_page.select_sort_option(label)
        prices = home_page.get_product_prices()
        assert prices == sorted(prices, reverse=reverse)


class TestHomePageFilters:
    @pytest.mark.regression
    def test_filter_by_category_reduces_results(self, home_page: HomePage):
        baseline_count = home_page.product_cards.count()
        home_page.filter_by_category("Hammer")
        filtered_names = home_page.get_product_names()
        assert home_page.product_cards.count() <= baseline_count
        assert len(filtered_names) > 0

    @pytest.mark.regression
    def test_price_range_filter_excludes_higher_priced_products(self, home_page: HomePage):
        home_page.adjust_max_price_handle(arrow_presses=20, direction="left")
        max_allowed = home_page.get_current_max_price_value()
        prices = home_page.get_product_prices()
        assert all(p <= max_allowed for p in prices), (
            f"Found price(s) above slider max {max_allowed}: {prices}"
        )

    @pytest.mark.regression
    def test_combined_category_and_price_filter(self, home_page: HomePage):
        home_page.filter_by_category("Hammer")
        count_after_category = home_page.product_cards.count()
        home_page.adjust_max_price_handle(arrow_presses=20, direction="left")
        count_after_both = home_page.product_cards.count()
        assert count_after_both <= count_after_category


class TestHomePagePagination:
    @pytest.mark.smoke
    def test_next_page_loads_different_products(self, home_page):
        page1_names = home_page.get_product_names()
        home_page.click_next_page()   # was: home_page.next_page_button.click()
        assert home_page.is_page_active(2)
        page2_names = home_page.get_product_names()
        assert page1_names != page2_names

    @pytest.mark.regression
    def test_prev_button_disabled_on_first_page(self, home_page: HomePage):
        assert home_page.prev_page_button.is_disabled() or \
            "disabled" in home_page.page.locator("li.page-item", has=home_page.prev_page_button).get_attribute("class")

    @pytest.mark.regression
    def test_direct_page_navigation(self, home_page: HomePage):
        home_page.go_to_page(3)
        assert home_page.is_page_active(3)

    def test_capture_requests_during_search(self, home_page: HomePage):
        seen = []
        home_page.page.on("request", lambda req: seen.append(f"{req.method} {req.url}"))

        home_page.search_input.fill("Pliers")
        home_page.search_button.click()
        home_page.page.wait_for_timeout(2500)  # debug-only, not for real tests

        print("\n--- Requests fired during search ---")
        for r in seen:
            print(r)

    def test_capture_requests(self, home_page):
        def log(response):
            print(
                response.request.method,
                response.status,
                response.url,
            )

        home_page.page.on("response", log)

        home_page.search_input.fill("Pliers")
        home_page.search_button.click()

        home_page.page.wait_for_timeout(3000)
