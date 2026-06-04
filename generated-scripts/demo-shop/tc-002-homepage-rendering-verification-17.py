import pytest
from playwright.sync_api import Page, expect


def test_tc_002_homepage_rendering_verification(page: Page):
    """
    Title: TC-002 Homepage Rendering Verification
    Business Intent: Verify the homepage of sauce-demo.myshopify.com loads with HTTP 200 status,
                     key UI sections (hero, navigation bar, product tiles) are present and visible,
                     and no JavaScript console errors are blocking the experience.
    Preconditions: None
    """
    # --- Arrange ---
    base_url = "https://sauce-demo.myshopify.com/"
    console_errors = []

    def handle_console_error(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    # Register console error listener before navigation (Step 9)
    page.on("console", handle_console_error)

    # --- Act ---
    # Step 1-3: Navigate to the application URL and wait for full page load
    response = page.goto(base_url, wait_until="load")

    # Step 3: Wait for network idle to ensure all resources have loaded
    page.wait_for_load_state("networkidle")

    # --- Assert ---
    # Step 4-5: Verify the main document HTTP response status code is 200 OK
    assert response is not None, "No HTTP response received from the server"
    assert response.status == 200, f"Expected HTTP 200 OK but received {response.status}"

    # Step 6: Verify hero section (banner/promotional image area) is present and visible
    hero_locator = page.locator(
        "header, [role='banner'], .hero, .banner, [class*='hero'], [class*='slideshow'], "
        ".index-section--image, .shopify-section .hero__image"
    ).first
    expect(hero_locator).to_be_visible(timeout=10000)

    # Step 7: Verify navigation bar (top menu with links) is present and visible
    nav_locator = page.locator(
        "header, nav, .site-nav, .header__inline-menu, "
        "[class*='header'], [role='navigation']"
    ).first
    expect(nav_locator).to_be_visible(timeout=10000)

    # Step 8: Verify product tiles (listing cards with images, names, and prices) are present and visible
    product_locator = page.locator(
        "a[href*='/products/'], .product-card, .grid__item, .product-item, "
        "[class*='product-card'], .products .product, .product-grid li"
    ).first
    expect(product_locator).to_be_visible(timeout=10000)

    # Step 9: Verify no blocking JavaScript console errors are present
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
    assert len(blocking_console_errors) == 0, (
        f"Blocking JavaScript console errors found ({len(blocking_console_errors)}): "
        + "; ".join(blocking_console_errors[:5])
    )

    # Step 10: Verify all main sections are fully visible and rendered without broken layout
    expect(page.locator("body")).to_be_visible()
    expect(page.get_by_role("banner")).to_be_visible(timeout=10000)
    expect(page.get_by_role("contentinfo")).to_be_visible(timeout=10000)
