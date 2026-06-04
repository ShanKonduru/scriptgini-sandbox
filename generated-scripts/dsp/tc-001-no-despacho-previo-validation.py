import pytest
from playwright.sync_api import Page, expect


def test_tc_001_no_despacho_previo_validation(page: Page):
    """
    Title: TC-001 No Despacho Previo Validation
    Business Intent: Verify that a DSP user can navigate to the car by release page,
                     filter equipment by status and waybill date, select equipment,
                     and validate the "No Despacho previo" option displays the correct
                     reason in the popup.
    Preconditions: Valid DSP user credentials must be available via environment variables
                   DSP_USERNAME and DSP_PASSWORD
    """
    # --- Arrange ---
    import os

    dsp_username = os.getenv("DSP_USERNAME", "dsp_test_user")
    dsp_password = os.getenv("DSP_PASSWORD", "test_password")
    base_url = os.getenv("DSP_BASE_URL", "https://dsp-app-url.com")

    # --- Act & Assert ---

    # Step 1: Login as DSP user
    page.goto(f"{base_url}/login", wait_until="networkidle")

    # Locate and fill login form
    username_input = page.get_by_role("textbox", name="username").or_(
        page.locator("input[name='username'], input[id='username'], input[type='text'][placeholder*='user' i]")
    ).first
    expect(username_input).to_be_visible(timeout=10000)
    username_input.fill(dsp_username)

    password_input = page.get_by_role("textbox", name="password").or_(
        page.locator("input[name='password'], input[id='password'], input[type='password']")
    ).first
    expect(password_input).to_be_visible(timeout=10000)
    password_input.fill(dsp_password)

    # Click login button
    login_button = page.get_by_role("button", name="login").or_(
        page.get_by_role("button", name="sign in")
    ).or_(
        page.locator("button[type='submit'], input[type='submit'], button:has-text('Login')")
    ).first
    expect(login_button).to_be_visible(timeout=5000)
    login_button.click()

    # Wait for successful login - expect dashboard or main page
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(lambda url: "login" not in url.lower(), timeout=15000)

    # Step 2: Navigate to car by release page
    # Look for navigation menu item or link
    car_by_release_link = page.get_by_role("link", name="car by release").or_(
        page.get_by_role("link", name="release")
    ).or_(
        page.locator("a[href*='release'], a[href*='car'], nav a:has-text('Car by Release')")
    ).first
    expect(car_by_release_link).to_be_visible(timeout=10000)
    car_by_release_link.click()

    # Wait for car by release page to load
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)  # Allow page to stabilize

    # Step 3: Select "to be released" status and select June 6th 2025 in waybill date from field
    # Locate status dropdown/filter
    status_filter = page.get_by_role("combobox", name="status").or_(
        page.locator("select[name*='status' i], select[id*='status' i], [data-testid*='status']")
    ).first
    expect(status_filter).to_be_visible(timeout=10000)
    status_filter.select_option(label="to be released")

    # Locate waybill date from field
    waybill_date_input = page.get_by_role("textbox", name="waybill date").or_(
        page.locator("input[name*='waybill' i], input[id*='waybill' i], input[type='date']")
    ).first
    expect(waybill_date_input).to_be_visible(timeout=10000)
    waybill_date_input.fill("2025-06-06")

    # Trigger filter/search if there's a search/filter button
    filter_button = page.get_by_role("button", name="filter").or_(
        page.get_by_role("button", name="search")
    ).or_(
        page.locator("button:has-text('Filter'), button:has-text('Search'), button[type='submit']")
    )
    if filter_button.count() > 0:
        filter_button.first.click()
        page.wait_for_load_state("networkidle")

    # Step 4: Select equipment with checkbox
    # Locate equipment list/table and select first available equipment
    equipment_checkbox = page.get_by_role("checkbox").first.or_(
        page.locator("input[type='checkbox']:not([disabled])")
    ).first
    expect(equipment_checkbox).to_be_visible(timeout=10000)
    equipment_checkbox.check()

    # Verify checkbox is checked
    expect(equipment_checkbox).to_be_checked()

    # Step 5: Click on actions button
    actions_button = page.get_by_role("button", name="actions").or_(
        page.locator("button:has-text('Actions'), button[id*='action' i], button[class*='action' i]")
    ).first
    expect(actions_button).to_be_visible(timeout=10000)
    actions_button.click()

    # Wait for actions menu to appear
    page.wait_for_timeout(500)

    # Step 6: Select No Despacho previo option
    no_despacho_option = page.get_by_role("menuitem", name="No Despacho previo").or_(
        page.get_by_role("button", name="No Despacho previo")
    ).or_(
        page.locator("li:has-text('No Despacho previo'), a:has-text('No Despacho previo'), button:has-text('No Despacho previo')")
    ).first
    expect(no_despacho_option).to_be_visible(timeout=10000)
    no_despacho_option.click()

    # Step 7: Check popup is containing reason for No Despacho previo option
    # Wait for popup/modal to appear
    popup_modal = page.locator(
        "[role='dialog'], .modal, [class*='popup'], [class*='modal'], [class*='dialog']"
    ).first
    expect(popup_modal).to_be_visible(timeout=10000)

    # Verify popup contains reason text or explanation
    reason_text = popup_modal.locator(
        "text=/reason/i, text=/motivo/i, text=/explicación/i, [class*='reason'], [id*='reason']"
    ).first
    expect(reason_text).to_be_visible(timeout=5000)

    # Verify popup has meaningful content about "No Despacho previo"
    popup_content = popup_modal.inner_text()
    assert len(popup_content.strip()) > 0, "Popup content is empty"
    assert any(
        keyword in popup_content.lower()
        for keyword in ["despacho", "previo", "reason", "motivo", "no dispatch"]
    ), f"Popup does not contain expected reason information. Content: {popup_content[:200]}"

    # Additional validation: Check for confirmation or close button in popup
    popup_button = popup_modal.get_by_role("button").first.or_(
        popup_modal.locator("button")
    ).first
    expect(popup_button).to_be_visible(timeout=5000)
