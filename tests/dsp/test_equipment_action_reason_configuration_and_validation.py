"""
DSP Equipment Action Reason Configuration and Validation Test
Test Case: Update Equipment Action Reason Configuration and validate in Cars By Release workflow
"""
import os
import pytest
from playwright.sync_api import Page, expect

from pages.dsp.login_page import LoginPage
from pages.dsp.home_page import HomePage
from pages.dsp.configuration_page import ConfigurationPage
from pages.dsp.cars_by_release_page import CarsByReleasePage


def test_equipment_action_reason_configuration_and_validation(page: Page):
    """
    Test: Equipment Action Reason Configuration and Validation

    Business Intent:
    Verify that a DSP user can update the Equipment Action Reason Configuration
    for 'No Despacho Previo' action, save the changes, and then validate that
    the updated reason appears in the Cars By Release workflow when performing
    the 'No Despacho Previo' action on selected equipment.

    Preconditions:
    - Valid DSP user credentials must be available via environment variables
      DSP_USERNAME and DSP_PASSWORD
    - Base URL must be provided via DSP_BASE_URL environment variable
    """

    # --- Arrange ---
    base_url = os.environ.get(
        "DSP_BASE_URL",
        "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth"
    )
    dsp_username = os.environ.get("DSP_USERNAME", "SivaRajesh.Gottumukkala@cpkcr.com")
    dsp_password = os.environ.get("DSP_PASSWORD", "Kasiviswanatha9949874966")

    # Initialize page objects
    login_page = LoginPage(page)
    home_page = HomePage(page)
    config_page = ConfigurationPage(page)
    cars_page = CarsByReleasePage(page)

    # --- Act & Assert ---

    # Step 1: Navigate to base URL
    login_page.navigate(base_url)
    expect(page).to_have_url(base_url, timeout=10000)

    # Step 2: Click on 'Login with Despachoprevio' button
    login_page.click_login_with_despachoprevio()

    # Step 3: Enter email address in the username field
    login_page.enter_username(dsp_username)

    # Step 4: Click on 'Next' button
    login_page.click_next()

    # Step 5: Enter password in the password field
    login_page.enter_password(dsp_password)

    # Step 6: Click on 'Sign in' button
    login_page.click_sign_in()

    # Step 7: Handle 'Accept Cookies' popup if it appears
    login_page.handle_accept_cookies_if_present()

    # Verify DSP Home page is displayed
    home_page.verify_home_page_loaded()

    # Step 8: Navigate to Configuration page from the left navigation menu
    home_page.navigate_to_configuration()

    # Verify Configuration page is displayed
    config_page.verify_configuration_page_loaded()

    # Step 9: Locate 'Equipment Action Reason Configuration' container
    # (verified in verify_configuration_page_loaded)

    # Step 10: Inside Equipment Action Reason Configuration container,
    # select existing action 'No Despacho Previo'
    config_page.select_action_no_despacho_previo()

    # Step 11: Update the reason text to 'Cancelled waybill'
    config_page.update_reason_text("Cancelled waybill")

    # Step 12: Click on 'Save Configuration' button
    config_page.click_save_configuration()

    # Step 13: Verify changes are saved successfully and updated reason
    # 'Cancelled waybill' is present in the configuration
    config_page.verify_reason_saved("Cancelled waybill")

    # Step 14: Navigate to Cars By Release page from the left navigation menu
    home_page.navigate_to_cars_by_release()

    # Verify Cars By Release page is displayed
    cars_page.verify_cars_by_release_page_loaded()

    # Step 15: Select 'to be released' status from the status filter options
    cars_page.select_status_to_be_released()

    # Step 16: Select an equipment by clicking the checkbox next to it
    cars_page.select_equipment_by_checkbox()

    # Step 17: Click on 'Actions' button
    cars_page.click_actions_button()

    # Step 18: Select 'No Despacho Previo' option from the actions dropdown
    cars_page.select_no_despacho_previo_action()

    # Step 19: Click on 'Select No Despacho Previo Action Reason' dropdown
    cars_page.click_action_reason_dropdown()

    # Step 20: Select 'Cancelled waybill' from the reason dropdown options
    cars_page.select_reason_cancelled_waybill()

    # Step 21: Click on 'Submit' button to complete the action
    cars_page.click_submit_button()

    # Verify action is completed successfully and popup closes
    cars_page.verify_action_completed()
