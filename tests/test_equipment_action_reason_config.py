"""
Test Case: Equipment Action Reason Configuration Verification
Verifies presence of Add button, Delete icons, and Save Configuration button
in the Equipment Action Reason Configuration section.
"""
import os
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.configuration_page import ConfigurationPage


def test_equipment_action_reason_configuration_ui_elements(page: Page):
    """
    Test Case: Equipment Action Reason Configuration - UI Elements Verification

    Steps:
    1. Clear all browser cookies and cache
    2. Navigate to base URL: https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth
    3. Click on 'Login with Despachoprevio' button to authenticate as Super Admin User
    4. Click on Configuration icon from the left menu
    5. Navigate to Equipment Action Reason Configuration section
    6. Verify Presence of Add Button in Equipment Action Reason Configuration section
    7. Verify Presence of Delete icon next to each reason in the configuration table
    8. Verify Presence of Save Configuration Button

    Preconditions:
    - Super Admin user credentials must be set in environment variables:
      ADMIN_EMAIL and ADMIN_PASSWORD
    """
    # Step 1: Clear all browser cookies and cache
    page.context.clear_cookies()

    # Get credentials from environment
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    base_url = os.environ.get("BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")

    if not admin_email or not admin_password:
        pytest.skip("ADMIN_EMAIL and ADMIN_PASSWORD environment variables must be set")

    # Step 2: Navigate to base URL
    login_page = LoginPage(page)
    login_page.navigate(base_url)

    # Verify login page loaded
    expect(page).to_have_title("Login Page", timeout=15000)

    # Step 3: Click on 'Login with Despachoprevio' button to authenticate as Super Admin User
    login_page.click_despachoprevio_login()

    # Wait for Microsoft SSO redirect
    expect(page).to_have_url("**/login.microsoftonline.com/**", timeout=15000)

    # Enter email
    login_page.enter_email(admin_email)
    login_page.click_next()

    # Enter password
    login_page.enter_password(admin_password)
    login_page.click_signin()

    # Handle "Stay signed in?" prompt if it appears
    login_page.handle_stay_signed_in()

    # Wait for successful login and redirect back to Pega application
    expect(page).to_have_url("**/prweb/**", timeout=30000)
    page.wait_for_load_state("networkidle")

    # Allow Pega application to fully load (it's a complex SPA)
    page.wait_for_timeout(3000)

    # Step 4: Click on Configuration icon from the left menu
    config_page = ConfigurationPage(page)
    config_page.click_configuration_icon()

    # Step 5: Navigate to Equipment Action Reason Configuration section
    config_page.navigate_to_equipment_action_reason_config()

    # Step 6: Verify Presence of Add Button in Equipment Action Reason Configuration section
    add_button = config_page.get_add_button()
    expect(add_button).to_be_visible(timeout=10000)
    assert config_page.verify_add_button_present(), "Add button is not present in Equipment Action Reason Configuration section"

    # Step 7: Verify Presence of Delete icon next to each reason in the configuration table
    delete_icons = config_page.get_delete_icons()
    expect(delete_icons.first).to_be_visible(timeout=10000)
    assert config_page.verify_delete_icons_present(), "Delete icons are not present next to configuration items"

    # Verify multiple delete icons exist (one per configuration row)
    delete_count = delete_icons.count()
    assert delete_count > 0, f"Expected at least 1 delete icon, found {delete_count}"

    # Step 8: Verify Presence of Save Configuration Button
    save_button = config_page.get_save_configuration_button()
    expect(save_button).to_be_visible(timeout=10000)
    assert config_page.verify_save_configuration_button_present(), "Save Configuration button is not present"

    # Take a final screenshot for verification
    page.screenshot(path="test-results/equipment-action-reason-config-verified.png", full_page=True)
