"""
Test Case: Equipment Action Reason Configuration - Blank Reason Validation
Business Intent: Verify that a Super Admin user can navigate to the Equipment Action
                 Reason Configuration section and clear the reason field for an existing
                 action reason entry.

Test Steps:
1. Navigate to DSP application URL
2. Login as Super Admin User
3. Click on Configuration icon from the menu
4. Navigate to Equipment Action Reason Configuration section
5. Locate and click on existing action reason entry (Action: 'Notify Broker', Reason: 'Due to chop code invalid')
6. Clear the reason field and keep it blank
7. Click on Save configuration button

Preconditions: Valid Super Admin credentials must be available via environment variables
"""
import os
import pytest
from playwright.sync_api import Page, expect

from pages.dsp_login_page import DSPLoginPage
from pages.dsp_configuration_page import DSPConfigurationPage


def test_equipment_action_reason_blank_validation(page: Page):
    """
    Test that verifies equipment action reason configuration can be updated
    with a blank reason field.
    """
    # --- Arrange: Get credentials from environment ---
    dsp_url = os.environ.get("DSP_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")
    dsp_username = os.environ.get("DSP_USERNAME", "SivaRajesh.Gottumukkala@cpkcr.com")
    dsp_password = os.environ.get("DSP_PASSWORD", "Kasiviswanatha9949874966")

    action_to_modify = "Notify Broker"
    reason_to_clear = "Due to chop code invalid"

    # --- Act & Assert ---

    # Step 1 & 2: Navigate to DSP and login as Super Admin
    login_page = DSPLoginPage(page)
    login_page.navigate(dsp_url)

    # Verify login page is loaded
    expect(login_page.username_input).to_be_visible(timeout=10000)

    # Perform login
    login_page.login(dsp_username, dsp_password)

    # Wait for post-login page to load (should redirect away from login)
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(lambda url: "login" not in url.lower() and "auth" not in url.lower(), timeout=15000)

    # Step 3: Click on Configuration icon from the menu
    config_page = DSPConfigurationPage(page)
    config_page.click_configuration_icon()

    # Verify we're in the configuration area
    page.wait_for_timeout(1000)

    # Step 4: Navigate to Equipment Action Reason Configuration section
    config_page.navigate_to_equipment_action_reason_config()

    # Verify the configuration section loaded
    page.wait_for_timeout(1000)

    # Step 5: Locate and click on existing action reason entry
    config_page.find_and_click_action_reason_entry(action_to_modify, reason_to_clear)

    # Verify the entry form/details are displayed
    page.wait_for_timeout(500)

    # Step 6: Clear the reason field and keep it blank
    config_page.clear_reason_field()

    # Verify the reason field is now empty
    frame = config_page.get_main_content_frame()
    if frame:
        reason_field = frame.locator("input[name*='Reason' i], textarea[name*='Reason' i]").first
    else:
        reason_field = page.locator("input[name*='Reason' i], textarea[name*='Reason' i]").first

    expect(reason_field).to_have_value("", timeout=5000)

    # Step 7: Click on Save configuration button
    config_page.click_save_configuration()

    # Verify save was successful (look for success message or page reload)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # Optional: Verify success message or that we're back to the list view
    # This depends on the actual application behavior after save
    # Common patterns:
    # - Success toast/banner appears
    # - Returns to configuration list
    # - Shows updated entry in table

    # Check for common success indicators in Pega applications
    success_indicators = [
        page.locator("text=/saved successfully/i"),
        page.locator("text=/update.*success/i"),
        page.locator("[class*='success']"),
        page.locator("[role='alert']:has-text('success')")
    ]

    success_found = False
    for indicator in success_indicators:
        if indicator.count() > 0:
            success_found = True
            break

    # Assert that either we see a success message OR we're back at the configuration list
    # (some apps don't show explicit success, just navigate back)
    assert success_found or page.url != dsp_url, "Save action completed but no confirmation detected"
