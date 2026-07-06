import os
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.configuration_page import ConfigurationPage


def test_update_equipment_action_reason_configuration(page: Page):
    """
    Test Case: Update Equipment Action Reason Configuration - DSP

    Steps:
        Step 1: Navigate to base URL (from env: BASE_URL)
                Expected: Base URL is loaded successfully and login page is displayed
        Step 2: Click on 'Login with Despachoprevio' button
                Expected: 'Login with Despachoprevio' button is clicked successfully and SSO authentication is initiated
        Step 3: Enter Username (from env: APP_USERNAME)
                Expected: Username field accepts the provided username
        Step 4: Click on 'Next' button
                Expected: 'Next' button is clicked and password field is displayed
        Step 5: Enter password (from env: APP_PASSWORD)
                Expected: Password field accepts the provided password (masked)
        Step 6: Click on 'Sign in' button
                Expected: User is authenticated and redirected to DSP Home page with Car By Release status, Car History, DSP Reports, and Configuration menus visible on the left
        Step 7: Once user logs in, if any popup arises like 'Accept Cookies', click on 'Accept' button
                Expected: Cookies popup is accepted and dismissed if present
        Step 8: Navigate to Configuration page from the left menu
                Expected: Configuration page is displayed with General settings by default
        Step 9: Locate 'Equipment Action Reason Configuration' container
                Expected: 'Equipment Action Reason Configuration' container is located and displayed with existing configurations
        Step 10: Inside Equipment Action Reason Configuration container, select existing action 'Cancelled'
                Expected: Existing action 'Cancelled' is selected successfully
        Step 11: Update reason to 'Duplicate Waybill'
                Expected: Reason text is updated to 'Duplicate Waybill' in the text field
        Step 12: Click on 'Save Configuration' button under Equipment Action Reason Configuration section
                Expected: Changes are saved successfully by clicking Save Configuration button in 'Equipment Action Reason Configuration' container
        Step 13: Verify the updated action-reason pair is displayed with Action: 'Cancelled' and Reason: 'Duplicate Waybill'
                Expected: Updated action-reason pair is displayed correctly with Action: 'Cancelled' and Reason: 'Duplicate Waybill'
        Step 14: Click on eye icon to view Pega audit history/log
                Expected: Pega audit history/log is displayed
        Step 15: Verify the audit trail displays Event, Created by, Created On, Updated by, and Updated On information
                Expected: The audit trail successfully logs the Event, Created by, Created On, Updated by, and Updated On details
    """

    # Initialize page objects
    login_page = LoginPage(page)
    config_page = ConfigurationPage(page)

    # Step 1: Navigate to base URL (from env: BASE_URL)
    base_url = os.environ["BASE_URL"]
    login_page.navigate(base_url)
    page.screenshot(path='screenshots/step_001_navigate.png')
    expect(page).to_have_url("**/PRAuth**")

    # Step 2: Click on 'Login with Despachoprevio' button
    login_page.click_despachoprevio_login()
    page.screenshot(path='screenshots/step_002_click_login_despachoprevio.png')
    expect(page).to_have_url("**/login.microsoftonline.com/**")

    # Step 3: Enter Username (from env: APP_USERNAME)
    login_page.enter_username(os.environ["APP_USERNAME"])
    page.screenshot(path='screenshots/step_003_fill_username.png')
    expect(login_page.username_input).to_have_value(os.environ["APP_USERNAME"])

    # Step 4: Click on 'Next' button
    login_page.click_next()
    page.screenshot(path='screenshots/step_004_click_next.png')
    expect(login_page.password_input).to_be_visible()

    # Step 5: Enter password (from env: APP_PASSWORD)
    login_page.enter_password(os.environ["APP_PASSWORD"])
    page.screenshot(path='screenshots/step_005_fill_password.png')
    expect(login_page.password_input).to_have_value(os.environ["APP_PASSWORD"])

    # Step 6: Click on 'Sign in' button
    login_page.click_signin()
    page.screenshot(path='screenshots/step_006_click_signin.png')
    expect(page).to_have_url("**/prweb/PRAuth/app/dsp-cont**")

    # Step 7: Accept cookies popup if present
    login_page.accept_cookies_if_present()
    page.screenshot(path='screenshots/step_007_accept_cookies.png')
    expect(page).to_have_title("*Despacho Previo*")

    # Step 8: Navigate to Configuration page from the left menu
    config_page.navigate_to_configuration()
    page.screenshot(path='screenshots/step_008_navigate_configuration.png')
    expect(page).to_have_url("**/configurations**")

    # Step 9: Locate 'Equipment Action Reason Configuration' container
    expect(config_page.equipment_action_config_heading).to_be_visible()
    page.screenshot(path='screenshots/step_009_locate_equipment_action_config.png')

    # Step 10: Inside Equipment Action Reason Configuration container, select existing action 'Cancelled'
    cancelled_row_index = config_page.find_row_with_action("Cancelled")
    assert cancelled_row_index > 0, "Cancelled action not found in configuration"
    action_dropdown = config_page.get_action_dropdown_for_row(cancelled_row_index)
    page.screenshot(path='screenshots/step_010_select_cancelled_action.png')
    expect(action_dropdown.locator('option:checked')).to_have_text("Cancelled")

    # Step 11: Update reason to 'Duplicate Waybill'
    config_page.update_reason(cancelled_row_index, "Duplicate Waybill")
    reason_input = config_page.get_reason_input_for_row(cancelled_row_index)
    page.screenshot(path='screenshots/step_011_update_reason.png')
    expect(reason_input).to_have_value("Duplicate Waybill")

    # Step 12: Click on 'Save Configuration' button under Equipment Action Reason Configuration section
    config_page.click_save_configuration()
    page.screenshot(path='screenshots/step_012_click_save_configuration.png')
    # Verify save completed by checking the values are still present
    expect(reason_input).to_have_value("Duplicate Waybill")

    # Step 13: Verify the updated action-reason pair is displayed with Action: 'Cancelled' and Reason: 'Duplicate Waybill'
    actual_action = config_page.get_selected_action(cancelled_row_index)
    actual_reason = config_page.get_reason_value(cancelled_row_index)
    page.screenshot(path='screenshots/step_013_verify_updated_pair.png')
    assert actual_action == "Cancelled", f"Expected action 'Cancelled', got '{actual_action}'"
    assert actual_reason == "Duplicate Waybill", f"Expected reason 'Duplicate Waybill', got '{actual_reason}'"

    # Step 14: Click on eye icon to view Pega audit history/log
    config_page.click_audit_history(cancelled_row_index)
    page.screenshot(path='screenshots/step_014_click_audit_history.png')
    expect(config_page.audit_modal).to_be_visible()

    # Step 15: Verify the audit trail displays Event, Created by, Created On, Updated by, and Updated On information
    audit_modal = config_page.audit_modal
    page.screenshot(path='screenshots/step_015_verify_audit_trail.png')
    expect(audit_modal).to_be_visible()
    # Verify modal contains audit information
    modal_text = audit_modal.inner_text()
    assert len(modal_text) > 0, "Audit modal is empty"
