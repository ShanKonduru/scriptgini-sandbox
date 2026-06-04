import re

import pytest
from playwright.sync_api import Page, expect


def _extract_cart_count(page: Page) -> int:
    """Read cart badge count from common Shopify cart badge selectors."""
    count_locators = [
        page.locator("#cart-icon-bubble .cart-count-bubble span"),
        page.locator("a[href*='/cart'] .cart-count-bubble span"),
        page.locator("a[href*='/cart'] .count"),
        page.locator("[id*='cart'] .cart-count-bubble"),
    ]

    for locator in count_locators:
        try:
            if locator.count() > 0 and locator.first.is_visible(timeout=3000):
                raw_text = locator.first.inner_text(timeout=3000).strip()
                match = re.search(r"\d+", raw_text)
                if match:
                    return int(match.group(0))
        except Exception:
            continue

    return 0


def _open_search_results(page: Page, base_url: str, query: str) -> None:
    page.goto(base_url, wait_until="load")
    page.wait_for_load_state("networkidle")

    search_input = page.locator(
        "input[name='q'][type='search'], input[type='search'], form[action*='/search'] input[name='q']"
    ).first
    expect(search_input).to_be_visible(timeout=10000)
    search_input.fill(query)
    expect(search_input).to_have_value(query)
    search_input.press("Enter")

    page.wait_for_load_state("networkidle")
    assert "search" in page.url or "q=" in page.url, "Search results URL was not loaded"


def _select_first_product_and_add(page: Page, expected_cart_count: int) -> str:
    product_link = page.locator("a[href*='/products/']").first
    expect(product_link).to_be_visible(timeout=10000)
    product_link.click()

    product_title_locator = page.locator("h1, .product__title, [data-product-title]").first
    expect(product_title_locator).to_be_visible(timeout=10000)
    product_title = product_title_locator.inner_text(timeout=5000).strip()
    assert product_title, "Product title is empty"

    add_to_cart_button = page.locator(
        "button[name='add'], button[type='submit']:has-text('Add to cart'), button:has-text('Add to cart')"
    ).first
    expect(add_to_cart_button).to_be_visible(timeout=10000)
    add_to_cart_button.click()

    # Validate cart count update after each add action.
    expect.poll(lambda: _extract_cart_count(page), timeout=15000).to_be(expected_cart_count)

    page.goto("https://sauce-demo.myshopify.com/cart", wait_until="load")
    page.wait_for_load_state("networkidle")
    expect(page.locator("body")).to_be_visible()

    expect(page.get_by_text(product_title, exact=False).first).to_be_visible(timeout=10000)

    cart_rows = page.locator(".cart-item, .cart__item, tr.cart-item, form[action*='/cart'] [name='updates[]']")
    expect(cart_rows.first).to_be_visible(timeout=10000)
    assert cart_rows.count() >= expected_cart_count, (
        f"Expected at least {expected_cart_count} cart line(s), got {cart_rows.count()}"
    )

    return product_title


def test_tc_003_shopify_login_search_add_to_cart(page: Page):
    """
    Title: TC-003 Shopify login, search products, add to cart with step validations
    Business Intent: Validate login flow, product search, cart add behavior, and per-action assertions.
    Preconditions: Site is reachable and test account is active.
    """
    base_url = "https://sauce-demo.myshopify.com/"
    login_url = "https://sauce-demo.myshopify.com/account/login"
    user_email = "cpkcshankonduru@gmail.com"
    user_password = "Cpkc$h@nK0nduru123"
    product_queries = ["shirt", "hoodie", "cap"]

    console_errors = []

    def handle_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    page.on("console", handle_console)

    # Step 1-3: Launch and navigate to homepage.
    response = page.goto(base_url, wait_until="load")
    page.wait_for_load_state("networkidle")
    assert response is not None, "No response received for homepage"
    assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    expect(page.locator("header, [role='banner']").first).to_be_visible(timeout=10000)
    expect(page.locator("nav, [role='navigation']").first).to_be_visible(timeout=10000)

    # Step 4-8: Open login page and validate successful sign-in.
    page.goto(login_url, wait_until="load")
    page.wait_for_load_state("networkidle")

    email_input = page.locator("input[name='customer[email]'], input[type='email']").first
    password_input = page.locator("input[name='customer[password]'], input[type='password']").first
    sign_in_button = page.locator("button[type='submit'], input[type='submit'], button:has-text('Sign in')").first

    expect(email_input).to_be_visible(timeout=10000)
    expect(password_input).to_be_visible(timeout=10000)
    expect(sign_in_button).to_be_visible(timeout=10000)

    email_input.fill(user_email)
    expect(email_input).to_have_value(user_email)

    password_input.fill(user_password)
    assert password_input.input_value() != "", "Password field is empty after fill"

    sign_in_button.click()
    page.wait_for_load_state("networkidle")

    assert "/account/login" not in page.url, "Login did not complete successfully"
    login_error = page.locator(
        ".errors, [role='alert'], .form__message, .customer .errors"
    ).first
    if login_error.count() > 0:
        assert not login_error.is_visible(), "Login error banner is visible"

    # Step 9-19: Search and add products with per-add validations.
    added_products = []
    for index, query in enumerate(product_queries, start=1):
        _open_search_results(page, base_url, query)
        added_title = _select_first_product_and_add(page, expected_cart_count=index)
        added_products.append(added_title)

    # Final cart verification.
    page.goto("https://sauce-demo.myshopify.com/cart", wait_until="load")
    page.wait_for_load_state("networkidle")
    expect.poll(lambda: _extract_cart_count(page), timeout=15000).to_be(len(product_queries))

    for product_name in added_products:
        expect(page.get_by_text(product_name, exact=False).first).to_be_visible(timeout=10000)

    ignored_console_error_fragments = [
        "tag.marinsm.com",
        "s.adroll.com",
        "Failed to load resource",
        "MIME type ('image/gif') is not executable",
        "favicon",
    ]
    blocking_console_errors = [
        err
        for err in console_errors
        if not any(fragment in err for fragment in ignored_console_error_fragments)
    ]
    assert not blocking_console_errors, (
        f"Blocking JavaScript console errors found ({len(blocking_console_errors)}): "
        + "; ".join(blocking_console_errors[:5])
    )
