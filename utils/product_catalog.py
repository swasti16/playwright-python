"""
Fetches live product catalog data via direct API call (not through Playwright
browser context -- this runs at test collection time, before any fixture
exists). Used to seed pytest_generate_tests with real, current product IDs
instead of hardcoded values that break when seed data changes.
"""
import requests
import random
from datetime import date

from config.settings import Settings

_cache: list[dict] | None = None


def _product_exists(product_id: str) -> bool:
    """Validates a product ID still resolves via the detail endpoint.
    The /products list endpoint appears to lag behind the detail
    endpoint on this shared practice site -- list and detail may be
    served from different data sources. Filtering once at collection
    time is far cheaper than discovering staleness mid test run."""
    resp = requests.get(f"{Settings.API_BASE_URL}/products/{product_id}")
    return resp.status_code == 200


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
        resp = requests.get(f"{Settings.API_BASE_URL}/products", params={"page": page})
        resp.raise_for_status()
        body = resp.json()
        products.extend(body["data"])
        if page >= body["last_page"]:
            break
        page += 1

    _cache = products
    return products


def get_happy_path_product_ids(count_per_category: int = 1) -> list[str]:
    """Random in-stock, currently-resolvable product(s) per distinct
    category. Seeded by today's date for xdist-safe identical collection
    across worker processes, while rotating day-to-day for coverage.

    Validates each sampled ID against the detail endpoint and draws
    replacements from the same category's remaining pool if a candidate
    is stale -- guarantees count_per_category valid IDs per category
    where the category has enough live stock, rather than silently
    returning fewer."""
    products = _fetch_all_products()
    rng = random.Random(date.today().isoformat())

    by_category: dict[str, list[str]] = {}
    for p in products:
        if p["in_stock"]:
            by_category.setdefault(p["category"]["name"], []).append(p["id"])

    ids = []
    for category_name, cat_ids in by_category.items():
        rng.shuffle(cat_ids)
        valid_for_category = []
        for candidate in cat_ids:
            if len(valid_for_category) >= count_per_category:
                break
            if _product_exists(candidate):
                valid_for_category.append(candidate)
        if len(valid_for_category) < count_per_category:
            print(f"[product_catalog] '{category_name}': only "
                  f"{len(valid_for_category)}/{count_per_category} live products found")
        ids.extend(valid_for_category)

    return ids


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

    result = {
        "location_offer": location_offer,
        "highest_price": highest_price,
        "lowest_price": lowest_price,
    }
    return {k: v for k, v in result.items() if v and _product_exists(v)}


# TEMP DEBUG — add at the bottom of the file, run directly: python utils/product_catalog.py
if __name__ == "__main__":
    products = _fetch_all_products()
    print(f"Total products fetched: {len(products)}")
    print(f"Categories found: {sorted(set(p['category']['name'] for p in products))}")