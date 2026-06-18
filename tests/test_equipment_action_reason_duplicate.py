"""
Test Case: Equipment Action Reason Configuration - Duplicate Validation
Business Intent: Verify that the system prevents duplicate Equipment Action Reason
                 entries (case-insensitive) and displays appropriate validation message
Preconditions: Valid DSP user credentials must be available via environment variables
"""
import os
import pytest
from playwright.sync_api import Page, expect


def test_equipment_action_reason_duplicate_validation(page: Page):
    """
    Test duplicate Equipment Action Reason validation with case-insensitive check

    Steps:
    1. Clear browser cookies and cache
    2. Navigate to Pega login page
    3. Login via Microsoft SSO (Despachoprevio)
    4. Navigate to Configuration section
    5. Add new Equipment Action Reason: Action='Cancelled', Reason='duplicate waybill'
    6. Verify duplicate validation (case-insensitive)
    """
    # --- Arrange ---
    base_url = os.environ.get(
        "DSP_BASE_URL",
        "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth"
    )
    username = os.environ.get("DSP_USERNAME", "")
    password = os.environ.get("DSP_PASSWORD", "")

    if not username or not password:
        pytest.skip("DSP_USERNAME and DSP_PASSWORD environment variables required")

    # Import page objects
    from pages.microsoft_login_page import MicrosoftLoginPage
    from pages.pega_configuration_page import PegaConfigurationPage

    # --- Act & Assert ---

    # Step 1 & 2: Navigate to base URL (browser context is fresh per test)
    page.goto(base_url, wait_until="networkidle")
    expect(page).to_have_title("Login Page", timeout=10000)

    # Step 3: Click on 'Login with Despachoprevio' button
    login_despachoprevio_button = page.get_by_role(
        "button",
        name="Login with despachoprevio"
    )
    expect(login_despachoprevio_button).to_be_visible(timeout=10000)
    login_despachoprevio_button.click()

    # Wait for Microsoft SSO page to load
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("**/login.microsoftonline.com/**", timeout=15000)

    # Step 4-7: Complete Microsoft SSO login
    ms_login = MicrosoftLoginPage(page)
    ms_login.complete_login(username, password, stay_signed_in=False)

    # Wait for successful authentication and redirect back to Pega
    page.wait_for_load_state("networkidle", timeout=30000)
    page.wait_for_url("**/pegacloud.net/**", timeout=30000)

    # Step 8: Handle cookie consent if it appears
    pega_config = PegaConfigurationPage(page)
    pega_config.accept_cookies_if_present()

    # Step 9: Click on Configuration icon from the left menu
    pega_config.click_configuration_menu()

    # Step 10: Verify Equipment Action Reason Configuration section is displayed
    pega_config.verify_equipment_action_reason_section_visible()

    # Step 11: Click on Add button at the left bottom corner
    pega_config.click_add_button()

    # Step 12: Select 'Cancelled' Action from the Action dropdown
    pega_config.select_action_dropdown("Cancelled")

    # Step 13: Enter duplicate Reason 'duplicate waybill' (case-insensitive test)
    # Note: This assumes 'duplicate waybill' already exists in the system
    # The test verifies case-insensitive duplicate detection
    pega_config.enter_reason_text("duplicate waybill")

    # Step 14: Click on Save Configuration button
    pega_config.click_save_configuration()

    # Verify duplicate validation message appears
    validation_message = pega_config.verify_duplicate_validation_message()
    assert validation_message is not None, "No validation message displayed"
    assert len(validation_message) > 0, "Validation message is empty"

    # Verify the message indicates duplication
    validation_lower = validation_message.lower()
    assert any(
        keyword in validation_lower
        for keyword in ["duplicate", "already exists", "existing", "unique"]
    ), f"Validation message does not indicate duplication: {validation_message}"

    print(f"✓ Duplicate validation test passed. Message: {validation_message}")
