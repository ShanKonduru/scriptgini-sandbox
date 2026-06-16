import os
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.cars_by_release_page import CarsByReleasePage


def test_no_despacho_previo_dropdown_options(page: Page):
    """
    Test Case: Verify No Despacho Previo Action Reason Dropdown Options

    Business Intent:
        Verify that a DSP user can navigate to the Cars By Release page, filter equipment
        by status and waybill date, select equipment, access the "No Despacho previo" action,
        and validate that the action reason dropdown contains the expected options:
        - Duplicate waybill
        - Released on other waybill
        - Cancelled waybill

    Preconditions:
        - Valid DSP user credentials must be available via environment variables:
          DSP_USERNAME, DSP_PASSWORD, DSP_BASE_URL

    Test Steps:
        1. Navigate to base URL and complete SSO login
        2. Accept cookies popup
        3. Navigate to Cars By Release page (default landing page after login)
        4. Select 'To be released' status filter
        5. Select June 6th 2025 in waybill date from field
        6. Click filter/search button if present
        7. Select first equipment with checkbox
        8. Click Actions button
        9. Select 'No Despacho previo' option
        10. Click on action reason dropdown
        11. Verify dropdown contains: Duplicate waybill, Released on other waybill, Cancelled waybill
    """

    # --- Arrange: Get credentials from environment ---
    base_url = os.getenv("DSP_BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")
    username = os.getenv("DSP_USERNAME")
    password = os.getenv("DSP_PASSWORD")

    assert username, "DSP_USERNAME environment variable is required"
    assert password, "DSP_PASSWORD environment variable is required"

    # Initialize page objects
    login_page = LoginPage(page)
    cars_page = CarsByReleasePage(page)

    # --- Act: Step 1-3 - Complete login flow ---
    login_page.login(base_url, username, password)

    # Verify we're on the Cars By Release Status page
    expect(page).to_have_title("Cars By Release Status - Despacho Previo", timeout=15000)

    # Wait for page to fully load
    cars_page.wait_for_page_load()

    # --- Act: Step 4-6 - Apply filters ---
    cars_page.select_status("To be released")
    cars_page.enter_waybill_date_from("2025-06-06")
    cars_page.click_filter_button()

    # --- Act: Step 7 - Select equipment ---
    cars_page.select_first_equipment()

    # --- Act: Step 8 - Click Actions button ---
    cars_page.click_actions_button()

    # --- Act: Step 9 - Select No Despacho previo option ---
    cars_page.select_no_despacho_previo()

    # --- Act: Step 10 - Click action reason dropdown ---
    cars_page.click_action_reason_dropdown()

    # --- Assert: Step 11 - Verify dropdown options ---
    expected_options = [
        "Duplicate waybill",
        "Released on other waybill",
        "Cancelled waybill"
    ]

    # Verify each expected option is present
    for option in expected_options:
        assert cars_page.is_option_present(option), \
            f"Expected option '{option}' not found in action reason dropdown"

    # Alternative verification: Get all found options and verify count
    found_options = cars_page.verify_dropdown_options(expected_options)
    assert len(found_options) == len(expected_options), \
        f"Expected {len(expected_options)} options, but found {len(found_options)}: {found_options}"

    print(f"✓ All expected options verified: {expected_options}")
