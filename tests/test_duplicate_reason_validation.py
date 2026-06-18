import os
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.configurations_page import ConfigurationsPage


def test_duplicate_reason_validation(page: Page):
    """
    Test Case: Duplicate Equipment Action Reason Validation

    Business Intent: Verify that the system prevents duplicate reason text entries
                     in the Equipment Action Reason Configuration section.

    Preconditions: Valid credentials must be available via environment variables
                   DSP_USERNAME and DSP_PASSWORD

    Test Steps:
        1. Navigate to the application login page
        2. Click 'Login with Despachoprevio' button
        3. Enter username and click Next
        4. Enter password and click Sign In
        5. Accept cookies popup if displayed
        6. Navigate to Configurations page
        7. Verify Equipment Action Reason Configuration section is displayed
        8. Locate the 'Notify Broker' action row
        9. Clear existing reason text
        10. Enter duplicate reason text 'Due to CPKC system limitation'
        11. Click Save configurations button
        12. Verify that an error message is displayed (duplicate not allowed)

    Expected Result: System should display an error indicating duplicate reason is not allowed
    """

    base_url = os.getenv("DSP_BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")
    username = os.getenv("DSP_USERNAME", "SivaRajesh.Gottumukkala@cpkcr.com")
    password = os.getenv("DSP_PASSWORD", "Kasiviswanatha9949874966")
    duplicate_reason = "Due to CPKC system limitation"

    login_page = LoginPage(page)
    config_page = ConfigurationsPage(page)

    login_page.navigate(base_url)

    login_page.click_login_with_despachoprevio()

    login_page.enter_username(username)
    login_page.click_next()

    login_page.enter_password(password)
    login_page.click_sign_in()

    login_page.accept_cookies()

    config_page.navigate_to_configurations()

    assert config_page.verify_equipment_action_reason_section_visible(), \
        "Equipment Action Reason Configuration section is not visible"

    input_field, original_value = config_page.find_action_reason_row("Notify Broker")
    assert input_field is not None, "Notify Broker action row not found"

    config_page.clear_reason_for_action("Notify Broker")

    config_page.enter_reason_for_action("Notify Broker", duplicate_reason)

    config_page.click_save_configurations()

    assert config_page.is_error_displayed(), \
        f"Expected error message for duplicate reason, but got: {config_page.get_alert_message()}"
