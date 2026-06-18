import os
from datetime import datetime
import pytest
from playwright.sync_api import Page, expect

from pages.dsp_login_page import DSPLoginPage
from pages.dsp_configurations_page import DSPConfigurationsPage


def test_tc_002_equipment_action_reason_configuration(page: Page):
    """
    Title: TC-002 Equipment Action Reason Configuration
    Business Intent: Verify that a DSP admin user can navigate to the Equipment Action
                     Reason Configuration section, add a new action reason with description,
                     save the configuration, and validate that the entry persists after
                     page refresh.
    Preconditions: Valid DSP admin credentials must be available via environment variables
                   DSP_USERNAME and DSP_PASSWORD
    """
    # --- Arrange ---
    dsp_username = os.getenv('DSP_USERNAME', 'SivaRajesh.Gottumukkala@cpkcr.com')
    dsp_password = os.getenv('DSP_PASSWORD', 'Kasiviswanatha9949874966')
    base_url = os.getenv('DSP_BASE_URL', 'https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth')

    # Generate unique action reason value using timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    action_reason = f'AutoTest_Reason_{timestamp}'
    description = f'Automated test description created on {timestamp}'

    # Initialize page objects
    login_page = DSPLoginPage(page)
    config_page = DSPConfigurationsPage(page)

    # --- Act & Assert ---

    # Step 1-5: Login via Microsoft SSO
    login_page.login(base_url, dsp_username, dsp_password)

    # Step 6-7: Verify DSP Home page is displayed
    expect(page).to_have_title(lambda title: 'Despacho Previo' in title, timeout=10000)
    expect(page).to_have_url(lambda url: 'dsp-cont' in url, timeout=10000)

    # Step 8: Navigate to Configurations
    config_page.navigate_to_configurations()
    expect(page).to_have_title(lambda title: 'Configurations' in title, timeout=10000)

    # Step 9-10: Navigate to Equipment Action Reason Configuration section
    config_page.open_equipment_action_reason_config()
    page.wait_for_timeout(1000)

    # Verify Equipment Action Reason Configuration section is displayed
    equipment_heading = config_page.main_frame.get_by_text(
        'Equipment Action Reason Configuration', exact=True
    )
    expect(equipment_heading).to_be_visible(timeout=5000)

    # Step 11: Click Add button to create new action reason
    config_page.click_add_action_reason()

    # Step 12-13: Populate Action and Description fields
    config_page.fill_action_reason(action_reason, description)

    # Step 14: Click Save button
    config_page.save_configuration()

    # Step 15: Verify success or handle validation errors
    # Note: If validation errors occur, the test will fail appropriately
    # In production, you may need to handle specific Pega validation dialogs
    page.wait_for_timeout(2000)

    # Check if save was successful by looking for the new entry
    # (Pega may reload the section after save)
    page.wait_for_timeout(1000)

    # Step 16-17: Refresh page and navigate back to Equipment Action Reason Configuration
    config_page.refresh_and_reopen_section()

    # Step 18: Validate that the newly added reason is persisted
    is_persisted = config_page.verify_action_reason_exists(action_reason)

    assert is_persisted, (
        f'Action reason "{action_reason}" was not found after page refresh. '
        f'The configuration may not have been saved successfully.'
    )

    # Additional verification: Check that the entry is visible in the table
    action_element = config_page.main_frame.get_by_text(action_reason, exact=True)
    expect(action_element).to_be_visible(
        timeout=5000,
        message=f'Expected action reason "{action_reason}" to be visible in the configuration table'
    )
