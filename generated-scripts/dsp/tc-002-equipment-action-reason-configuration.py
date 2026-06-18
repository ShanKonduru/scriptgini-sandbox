import os
import pytest
from playwright.sync_api import Page, expect, FrameLocator


def test_tc_002_equipment_action_reason_configuration(page: Page):
    """
    Title: TC-002 Equipment Action Reason Configuration - Add Reason with Spaces
    Business Intent: Verify that a user can navigate to the Configurations page,
                     access the Equipment Action Reason Configuration section,
                     add a new action reason with leading/trailing spaces, and
                     verify the reason is saved correctly in the configuration table.
    Preconditions: Valid DSP user credentials must be available via environment variables
                   DSP_USERNAME and DSP_PASSWORD
    """
    # --- Arrange ---
    dsp_username = os.getenv("DSP_USERNAME", "SivaRajesh.Gottumukkala@cpkcr.com")
    dsp_password = os.getenv("DSP_PASSWORD", "Kasiviswanatha9949874966")
    base_url = os.getenv("DSP_BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")

    # --- Act & Assert ---

    # Step 1: Navigate to base URL
    page.goto(base_url, wait_until="networkidle")
    expect(page).to_have_title("Login Page")

    # Step 2: Click on 'Login with Despachoprevio' button
    login_despachoprevio_button = page.get_by_role("link", name="Login with despachoprevio")
    expect(login_despachoprevio_button).to_be_visible(timeout=10000)
    login_despachoprevio_button.click()

    # Wait for Microsoft login page
    page.wait_for_load_state("networkidle")
    expect(page).to_have_title("Sign in to your account")

    # Step 3: Enter email in the email field
    email_input = page.get_by_role("textbox", name="Enter your email, phone, or")
    expect(email_input).to_be_visible(timeout=10000)
    email_input.fill(dsp_username)

    # Step 4: Click on Next button
    next_button = page.get_by_role("button", name="Next")
    expect(next_button).to_be_visible(timeout=5000)
    next_button.click()

    # Wait for password page
    page.wait_for_timeout(1000)

    # Step 5: Enter password in the password field
    password_input = page.get_by_role("textbox", name="Enter the password for")
    expect(password_input).to_be_visible(timeout=10000)
    password_input.fill(dsp_password)

    # Step 6: Click on Sign in button
    signin_button = page.get_by_role("button", name="Sign in")
    expect(signin_button).to_be_visible(timeout=5000)
    signin_button.click()

    # Wait for application to load
    page.wait_for_load_state("networkidle")

    # Step 7: Handle cookies acceptance popup if it appears
    try:
        accept_button = page.get_by_test_id(":privacy-dialog:accept")
        if accept_button.is_visible(timeout=5000):
            accept_button.click()
            page.wait_for_timeout(1000)
    except Exception:
        # Popup may not appear, continue
        pass

    # Wait for main application page to load
    page.wait_for_load_state("networkidle")
    expect(page).to_have_title("Cars By Release Status - Despacho Previo", timeout=15000)

    # Step 8: Expand navigation menu
    expand_nav_button = page.get_by_role("button", name="Expand navigation")
    if expand_nav_button.is_visible(timeout=5000):
        expand_nav_button.click()
        page.wait_for_timeout(500)

    # Step 9: User selects Configuration icon from the left menu
    configurations_link = page.get_by_text("Configurations", exact=True)
    expect(configurations_link).to_be_visible(timeout=10000)
    configurations_link.click()

    # Wait for configurations page to load
    page.wait_for_load_state("networkidle")
    expect(page).to_have_title("Configurations - Despacho Previo", timeout=10000)

    # Wait for iframe to load
    page.wait_for_timeout(2000)

    # Get iframe locator - Pega applications use iframes extensively
    iframe: FrameLocator = page.frame_locator("iframe").first

    # Wait for loading to complete
    try:
        loading_indicator = page.get_by_text("Loading content...")
        if loading_indicator.is_visible(timeout=2000):
            loading_indicator.wait_for(state="hidden", timeout=30000)
    except Exception:
        # Loading may have already completed
        pass

    # Step 10: User verifies Equipment Action Reason Configuration section is shown
    equipment_section_heading = iframe.get_by_role("heading", name="Equipment Action Reason Configuration")
    expect(equipment_section_heading).to_be_visible(timeout=10000)
    equipment_section_heading.scroll_into_view_if_needed()

    # Step 11: Click on Add button in Equipment Action Reason Configuration section
    # Find the Add button that follows the Equipment Action Reason Configuration heading
    add_button = equipment_section_heading.locator("xpath=following::button[contains(text(), 'Add')][1]")
    expect(add_button).to_be_visible(timeout=10000)
    add_button.click()
    page.wait_for_timeout(1000)

    # Step 12: Select 'Cancelled' Action from dropdown
    # Find the last action dropdown (newly added row)
    action_dropdown = iframe.locator("select[name*='pParentKey']").last
    expect(action_dropdown).to_be_visible(timeout=10000)
    action_dropdown.scroll_into_view_if_needed()
    action_dropdown.select_option(label="Cancelled")
    page.wait_for_timeout(500)

    # Step 13: Add Reason ' Duplicate Waybill ' with leading and trailing spaces in the reason text box
    # Find the last reason input field (corresponding to the newly added row)
    reason_input = iframe.locator("input[type='text'][name*='pKey']").last
    expect(reason_input).to_be_visible(timeout=10000)
    reason_input.scroll_into_view_if_needed()
    # Fill with spaces intentionally included as per test requirement
    reason_input.fill(" Duplicate Waybill ")
    page.wait_for_timeout(500)

    # Step 14: Click on Save configuration button
    save_button = iframe.get_by_role("button", name="Save configurations").first
    expect(save_button).to_be_visible(timeout=10000)
    save_button.scroll_into_view_if_needed()
    save_button.click()

    # Wait for save to complete
    page.wait_for_timeout(3000)

    # Step 15: Verify newly added reason is present in the configuration table
    # Check that "Duplicate Waybill" appears in the table
    all_reason_inputs = iframe.locator("input[type='text'][name*='pKey']")

    # Collect all reason values
    reason_values = []
    count = all_reason_inputs.count()
    for i in range(count):
        try:
            value = all_reason_inputs.nth(i).input_value()
            if value:
                reason_values.append(value.strip())
        except Exception:
            continue

    # Verify "Duplicate Waybill" is in the list
    assert "Duplicate Waybill" in reason_values, \
        f"Expected 'Duplicate Waybill' to be present in configuration table. Found reasons: {reason_values}"

    # Additional validation: Verify at least one reason contains "Duplicate Waybill"
    matching_reasons = [r for r in reason_values if "Duplicate Waybill" in r]
    assert len(matching_reasons) > 0, \
        f"No reasons containing 'Duplicate Waybill' found in configuration table"
