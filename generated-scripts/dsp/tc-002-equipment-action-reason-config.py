import os
import pytest
from playwright.sync_api import Page, expect
from pages.dsp_login_page import DSPLoginPage
from pages.dsp_configuration_page import DSPConfigurationPage


def test_tc_002_equipment_action_reason_configuration(page: Page):
    """
    Title: TC-002 Equipment Action Reason Configuration
    Business Intent: Verify that a DSP user can navigate to the Equipment Action Reason
                     Configuration section, add a new action-reason entry (Cancelled - Duplicate Waybill),
                     switch tabs without saving, and verify the unsaved entry persists when returning
                     to the Active tab.
    Preconditions: Valid DSP user credentials must be available via environment variables
                   DSP_USERNAME and DSP_PASSWORD
    Test Steps:
        1. Navigate to base URL
        2. Click on Login with Despachoprevio button
        3. Enter Username: SivaRajesh.Gottumukkala@cpkcr.com
        4. Click on Next button
        5. Enter Password
        6. Click on Sign in button
        7. If any popup appears (like accept cookies), click on Accept button
        8. Navigate to Configuration icon and click on it
        9. Verify Equipment Action Reason Configuration section is displayed at the bottom
        10. Click on Add button in Equipment Action Reason Configuration section
        11. Select Cancelled from Action column dropdown
        12. Enter Reason as 'Duplicate Waybill' in the Reason column
        13. Click on Inactive tab without clicking Save button
        14. Navigate back to Active tab
        15. Verify the newly added action-reason entry
    """
    # --- Arrange ---
    base_url = os.getenv("DSP_BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")
    dsp_username = os.getenv("DSP_USERNAME", "SivaRajesh.Gottumukkala@cpkcr.com")
    dsp_password = os.getenv("DSP_PASSWORD")

    if not dsp_password:
        pytest.skip("DSP_PASSWORD environment variable not set")

    login_page = DSPLoginPage(page)
    config_page = DSPConfigurationPage(page)

    # --- Act & Assert ---

    # Step 1: Navigate to base URL
    login_page.navigate(base_url)
    expect(page).to_have_url(base_url, timeout=10000)

    # Step 2: Click on Login with Despachoprevio button
    login_page.click_login_with_despachoprevio()
    # Should redirect to Microsoft SSO login page
    expect(page).to_have_url(lambda url: "login.microsoftonline.com" in url, timeout=10000)

    # Step 3: Enter Username
    expect(login_page.username_input).to_be_visible(timeout=10000)
    login_page.enter_username(dsp_username)

    # Step 4: Click on Next button
    login_page.click_next()

    # Step 5: Enter Password
    expect(login_page.password_input).to_be_visible(timeout=10000)
    login_page.enter_password(dsp_password)

    # Step 6: Click on Sign in button
    login_page.click_sign_in()

    # Wait for redirect back to Pega application
    expect(page).to_have_url(lambda url: "pegacloud.net" in url, timeout=30000)

    # Step 7: Handle any popup that appears (Stay signed in?, Accept cookies, etc.)
    login_page.handle_stay_signed_in_popup(stay_signed_in=True)

    # Additional wait for Pega application to fully load
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Step 8: Navigate to Configuration icon and click on it
    config_page.click_configuration_icon()

    # Step 9: Verify Equipment Action Reason Configuration section is displayed at the bottom
    assert config_page.is_equipment_action_reason_section_visible(), \
        "Equipment Action Reason Configuration section is not visible"

    # Step 10: Click on Add button in Equipment Action Reason Configuration section
    config_page.click_add_button_in_equipment_section()

    # Step 11: Select Cancelled from Action column dropdown
    config_page.select_action_dropdown("Cancelled")

    # Step 12: Enter Reason as 'Duplicate Waybill' in the Reason column
    config_page.enter_reason_text("Duplicate Waybill")

    # Step 13: Click on Inactive tab without clicking Save button
    config_page.click_inactive_tab()

    # Step 14: Navigate back to Active tab
    config_page.click_active_tab()

    # Step 15: Verify the newly added action-reason entry
    assert config_page.verify_action_reason_entry_exists("Cancelled", "Duplicate Waybill"), \
        "The newly added action-reason entry (Cancelled - Duplicate Waybill) is not visible in the Active tab"

    # Additional verification: Get the reason text for the Cancelled action
    reason_text = config_page.get_action_reason_entry_text("Cancelled")
    assert "Duplicate Waybill" in reason_text, \
        f"Expected reason 'Duplicate Waybill' but got '{reason_text}'"
