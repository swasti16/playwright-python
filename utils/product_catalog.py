"""
Fetches live product catalog data via direct API call (not through Playwright
browser context -- this runs at test collection time, before any fixture
exists). Used to seed pytest_generate_tests with real, current product IDs
instead of hardcoded values that break when seed data changes.
"""
import requests
from config.settings import Settings

_API_BASE = "https://api.practicesoftwaretesting.com"
_cache: list[dict] | None = None


def _fetch_all_products() -> list[dict]:
    """Fetches every page of /products and returns the flattened list.
    Cached at module level -- collection runs this once per pytest session,
    not once per test."""
    global _cache
    if _cache is not None:
        return _cache

    products = []
    page = 1
    while True:
        resp = requests.get(f"{_API_BASE}/products", params={"page": page})
        resp.raise_for_status()
        body = resp.json()
        products.extend(body["data"])
        if page >= body["last_page"]:
            break
        page += 1

    _cache = products
    return products


def get_happy_path_product_ids(count_per_category: int = 1) -> list[str]:
    """One in-stock product per distinct category -- standard flow coverage."""
    products = _fetch_all_products()
    seen_categories = set()
    ids = []
    for p in products:
        cat = p["category"]["name"]
        if cat not in seen_categories and p["in_stock"]:
            ids.append(p["id"])
            seen_categories.add(cat)
    return ids[:count_per_category] if count_per_category else ids


def get_boundary_product_ids() -> dict[str, str]:
    """
    Structurally distinct products worth explicit edge-case coverage.
    Returns a dict so tests can reference by meaning, not position.
    """
    products = _fetch_all_products()

    # out_of_stock = next((p["id"] for p in products if not p["in_stock"]), None)
    location_offer = next((p["id"] for p in products if p["is_location_offer"]), None)
    highest_price = max(products, key=lambda p: p["price"])["id"]
    lowest_price = min(products, key=lambda p: p["price"])["id"]

    return {
        # "out_of_stock": out_of_stock,
        "location_offer": location_offer,
        "highest_price": highest_price,
        "lowest_price": lowest_price,
    }#