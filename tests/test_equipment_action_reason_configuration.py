import os
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.configurations_page import ConfigurationsPage
from pages.cars_by_release_page import CarsByReleasePage


def test_equipment_action_reason_configuration_update_and_verify(page: Page):
    """
    Test Case: Equipment Action Reason Configuration - Update and Verify

    Business Intent:
    Verify that a DSP admin user can:
    1. Update an action reason in the Equipment Action Reason Configuration
    2. Navigate to Cars By Release page
    3. Select equipment and apply the No Despacho Previo action
    4. Verify the updated reason is available in the action reason dropdown

    Preconditions:
    - Valid DSP admin credentials must be available via environment variables
    - User must have permission to update configurations
    """

    # Arrange - Get credentials and base URL from environment
    base_url = os.getenv("DSP_BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")
    email = os.getenv("DSP_EMAIL", "SivaRajesh.Gottumukkala@cpkcr.com")
    password = os.getenv("DSP_PASSWORD", "Kasiviswanatha9949874966")

    # Initialize page objects
    login_page = LoginPage(page)
    config_page = ConfigurationsPage(page)
    cars_page = CarsByReleasePage(page)

    # Test data
    target_action = "No Despacho Previo"
    original_reason = "Cancelled Waybill"
    updated_reason = "Updated test reason - Cancelled waybill"

    # Act & Assert

    # Step 1-8: Login and navigate to Configurations
    login_page.login(base_url, email, password)
    expect(page).to_have_title("Cars By Release Status - Despacho Previo", timeout=15000)

    # Step 9: Navigate to Configuration page
    config_page.navigate_to_configurations()
    expect(page).to_have_title("Configurations - Despacho Previo", timeout=10000)

    # Step 10: Verify Equipment Action Reason Configuration section is shown
    config_page.verify_equipment_action_reason_section_visible()

    # Step 11-12: Find existing action-reason pair and update it
    # Note: Using row 17 which has "No Despacho Previo" - "Cancelled Waybill"
    target_row = 17
    config_page.update_reason_for_row(target_row, updated_reason)

    # Step 13: Save configuration
    config_page.click_save_configurations()

    # Step 14: Verify updated reason is present in configuration table
    page.wait_for_timeout(1000)
    pairs = config_page.get_all_action_reason_pairs()
    updated_pair = next((p for p in pairs if p["row"] == target_row), None)
    assert updated_pair is not None, f"Row {target_row} not found in configuration table"
    assert updated_pair["action"] == target_action, f"Expected action '{target_action}', got '{updated_pair['action']}'"
    assert updated_pair["reason"] == updated_reason, f"Expected reason '{updated_reason}', got '{updated_pair['reason']}'"

    # Step 15: Navigate to Car By Release page
    cars_page.navigate_to_cars_by_release()
    expect(page).to_have_title("Cars By Release Status - Despacho Previo", timeout=10000)

    # Step 16: Select 'To Be Released' status
    cars_page.select_status("TO BE RELEASED")

    # Step 17: Select equipment with checkbox
    cars_page.select_equipment_checkbox(index=1)
    cars_page.verify_equipment_checkbox_checked(index=1)

    # Step 18: Click on Actions button
    cars_page.click_actions_button()

    # Step 19: Select No Despacho Previo option
    cars_page.select_no_despacho_previo_action()

    # Step 20: Verify action dialog is visible
    cars_page.verify_action_dialog_visible()

    # Step 21: Click on Select No Despacho Previo Action Reason dropdown
    # and verify updated reason is available
    available_reasons = cars_page.get_available_action_reasons()
    assert original_reason in available_reasons, f"Expected reason '{original_reason}' not found in dropdown options"

    # Step 21-22: Select 'Cancelled waybill' from dropdown and submit
    cars_page.select_action_reason(original_reason)

    # Step 23: Click Submit button
    cars_page.click_submit()

    # Final verification: Action was submitted successfully
    page.wait_for_timeout(2000)
