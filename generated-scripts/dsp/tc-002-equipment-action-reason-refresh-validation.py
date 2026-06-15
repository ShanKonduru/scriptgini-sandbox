import os
import pytest
from playwright.sync_api import Page, expect


def test_tc_002_equipment_action_reason_refresh_validation(page: Page):
    """
    Test Case: TC-002 Equipment Action Reason Configuration - Browser Refresh Validation

    Business Intent: Verify that unsaved changes in Equipment Action Reason Configuration
                     are discarded when the browser is refreshed, ensuring data integrity
                     and preventing accidental additions without explicit save.

    Preconditions: Valid user credentials must be available via environment variables
                   DSP_USERNAME and DSP_PASSWORD

    Test Steps:
    1. Clear all browser cookies and cache
    2. Navigate to base URL
    3. Click on 'Login with Despachoprevio' button
    4. Enter username on Microsoft SSO page
    5. Click Next button
    6. Enter password on Microsoft SSO page
    7. Click on Sign In button
    8. Handle accept cookies popup if it appears
    9. Click on Configuration icon from the left menu
    10. Navigate to Equipment Action Reason Configuration section and verify it is displayed
    11. Click on Add button in Equipment Action Reason Configuration section
    12. Select 'Cancelled' Action from the Action dropdown
    13. Enter reason 'Duplicate Waybill' in the Reason text box
    14. Click on browser refresh button without saving changes
    15. Verify the newly added reason 'Duplicate Waybill' for 'Cancelled' action is absent
    """

    # --- Arrange ---
    dsp_username = os.getenv("DSP_USERNAME", "SivaRajesh.Gottumukkala@cpkcr.com")
    dsp_password = os.getenv("DSP_PASSWORD")
    base_url = os.getenv("DSP_BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")

    if not dsp_password:
        pytest.skip("DSP_PASSWORD environment variable not set")

    # --- Act & Assert ---

    # Step 1: Clear all browser cookies and cache
    page.context.clear_cookies()

    # Step 2: Navigate to base URL
    page.goto(base_url, wait_until="networkidle")
    expect(page).to_have_title("Login Page", timeout=15000)

    # Step 3: Click on 'Login with Despachoprevio' button
    login_despachoprevio_btn = page.get_by_role("button", name="Login with despachoprevio")
    expect(login_despachoprevio_btn).to_be_visible(timeout=10000)
    login_despachoprevio_btn.click()

    # Wait for Microsoft SSO page to load
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(lambda url: "microsoftonline.com" in url, timeout=15000)

    # Step 4: Enter username on Microsoft SSO page
    username_field = page.get_by_role("textbox", name="Enter your email, phone, or")
    expect(username_field).to_be_visible(timeout=10000)
    username_field.fill(dsp_username)

    # Step 5: Click Next button
    next_button = page.get_by_role("button", name="Next")
    expect(next_button).to_be_visible(timeout=5000)
    next_button.click()

    # Wait for password page to load
    page.wait_for_timeout(2000)

    # Step 6: Enter password on Microsoft SSO page
    password_field = page.get_by_role("textbox", name="Enter the password for")
    expect(password_field).to_be_visible(timeout=10000)
    password_field.fill(dsp_password)

    # Step 7: Click on Sign In button
    signin_button = page.get_by_role("button", name="Sign in")
    expect(signin_button).to_be_visible(timeout=5000)
    signin_button.click()

    # Wait for successful login and redirect to Pega application
    page.wait_for_load_state("networkidle", timeout=30000)
    expect(page).to_have_url(lambda url: "pegacloud.net" in url and "PRAuth" not in url, timeout=30000)

    # Step 8: Handle accept cookies popup if it appears
    try:
        accept_cookies_btn = page.get_by_role("button", name="Accept").or_(
            page.get_by_role("button", name="Aceptar")
        ).or_(
            page.locator("button:has-text('Accept'), button:has-text('Aceptar')")
        ).first
        if accept_cookies_btn.is_visible(timeout=3000):
            accept_cookies_btn.click()
            page.wait_for_timeout(500)
    except Exception:
        # No cookies popup appeared, continue
        pass

    # Pega applications typically use iframes - locate the main application iframe
    # Wait for the main Pega iframe to be available
    page.wait_for_timeout(3000)

    # Try to locate the main Pega iframe (common patterns: PegaGadget0Ifr, PegaGadget1Ifr, or iframe with title)
    main_frame = None
    for frame_name in ["PegaGadget0Ifr", "PegaGadget1Ifr", "PegaGadget2Ifr"]:
        try:
            frame_candidate = page.frame_locator(f"iframe[name='{frame_name}']")
            # Test if frame is accessible by checking for any element
            if frame_candidate.locator("body").count() > 0:
                main_frame = frame_candidate
                break
        except Exception:
            continue

    # If no standard frame found, try by title or class
    if main_frame is None:
        try:
            main_frame = page.frame_locator("iframe[title*='Main'], iframe.main-frame, iframe#main").first
        except Exception:
            # Work directly with page if no iframe detected
            main_frame = page

    # Step 9: Click on Configuration icon from the left menu
    # Pega left navigation typically uses specific patterns
    config_menu_item = main_frame.locator(
        "a[title*='Configuration' i], a:has-text('Configuration'), "
        "button:has-text('Configuration'), [data-test-id*='Configuration'], "
        "nav a:has-text('Configuration')"
    ).first.or_(
        main_frame.get_by_role("link", name="Configuration")
    ).or_(
        main_frame.get_by_role("button", name="Configuration")
    )

    # Wait for left menu to be available
    page.wait_for_timeout(2000)
    expect(config_menu_item).to_be_visible(timeout=15000)
    config_menu_item.click()

    # Wait for configuration page to load
    page.wait_for_load_state("networkidle", timeout=10000)
    page.wait_for_timeout(2000)

    # Step 10: Navigate to Equipment Action Reason Configuration section and verify it is displayed
    equipment_action_reason_section = main_frame.locator(
        "text='Equipment Action Reason Configuration', "
        "[data-test-id*='EquipmentActionReason'], "
        "h2:has-text('Equipment Action Reason'), "
        "h3:has-text('Equipment Action Reason')"
    ).first.or_(
        main_frame.get_by_text("Equipment Action Reason Configuration")
    )
    expect(equipment_action_reason_section).to_be_visible(timeout=10000)

    # Verify the section header or container is displayed
    config_container = main_frame.locator(
        "[id*='EquipmentActionReason'], [class*='equipment-action-reason'], "
        "section:has-text('Equipment Action Reason')"
    ).first
    expect(config_container).to_be_visible(timeout=5000)

    # Step 11: Click on Add button in Equipment Action Reason Configuration section
    # Look for Add button within the Equipment Action Reason section
    add_button = config_container.locator(
        "button:has-text('Add'), button[title*='Add'], "
        "button[data-test-id*='Add'], a:has-text('Add')"
    ).first.or_(
        config_container.get_by_role("button", name="Add")
    )
    expect(add_button).to_be_visible(timeout=10000)
    add_button.click()

    # Wait for the add form/modal to appear
    page.wait_for_timeout(1500)

    # Step 12: Select 'Cancelled' Action from the Action dropdown
    # Pega dropdowns can be standard select elements or custom components
    action_dropdown = main_frame.locator(
        "select[name*='Action' i], select[id*='Action' i], "
        "[data-test-id*='Action'] select, "
        "div[role='combobox']:has-text('Action')"
    ).first.or_(
        main_frame.get_by_role("combobox", name="Action")
    ).or_(
        main_frame.locator("label:has-text('Action') + select, label:has-text('Action') ~ select")
    )

    expect(action_dropdown).to_be_visible(timeout=10000)

    # Try to select 'Cancelled' - handle both standard select and custom dropdowns
    try:
        action_dropdown.select_option(label="Cancelled")
    except Exception:
        # If standard select doesn't work, try clicking and selecting from list
        action_dropdown.click()
        page.wait_for_timeout(500)
        cancelled_option = main_frame.locator("li:has-text('Cancelled'), option:has-text('Cancelled')").first
        cancelled_option.click()

    page.wait_for_timeout(500)

    # Step 13: Enter reason 'Duplicate Waybill' in the Reason text box
    reason_input = main_frame.locator(
        "input[name*='Reason' i], input[id*='Reason' i], "
        "[data-test-id*='Reason'] input, "
        "label:has-text('Reason') + input, label:has-text('Reason') ~ input"
    ).first.or_(
        main_frame.get_by_role("textbox", name="Reason")
    ).or_(
        main_frame.get_by_placeholder("Reason")
    )

    expect(reason_input).to_be_visible(timeout=10000)
    reason_input.fill("Duplicate Waybill")

    # Verify the text was entered
    expect(reason_input).to_have_value("Duplicate Waybill")

    # Take a moment to ensure the form is fully populated
    page.wait_for_timeout(1000)

    # Step 14: Click on browser refresh button without saving changes
    # Do NOT click Save button - directly refresh the page
    page.reload(wait_until="networkidle")

    # Wait for page to fully reload
    page.wait_for_timeout(3000)

    # Re-locate the main frame after reload (page reload clears frame references)
    main_frame_after_reload = None
    for frame_name in ["PegaGadget0Ifr", "PegaGadget1Ifr", "PegaGadget2Ifr"]:
        try:
            frame_candidate = page.frame_locator(f"iframe[name='{frame_name}']")
            if frame_candidate.locator("body").count() > 0:
                main_frame_after_reload = frame_candidate
                break
        except Exception:
            continue

    if main_frame_after_reload is None:
        try:
            main_frame_after_reload = page.frame_locator("iframe[title*='Main'], iframe.main-frame, iframe#main").first
        except Exception:
            main_frame_after_reload = page

    # Step 15: Verify the newly added reason 'Duplicate Waybill' for 'Cancelled' action is absent
    # Navigate back to Equipment Action Reason Configuration section if needed
    try:
        equipment_section_check = main_frame_after_reload.locator(
            "text='Equipment Action Reason Configuration', "
            "[data-test-id*='EquipmentActionReason']"
        ).first
        expect(equipment_section_check).to_be_visible(timeout=10000)
    except Exception:
        # May need to click Configuration again
        config_menu_after_reload = main_frame_after_reload.locator(
            "a[title*='Configuration' i], a:has-text('Configuration')"
        ).first
        config_menu_after_reload.click()
        page.wait_for_timeout(2000)

    # Look for the configuration table/list
    config_table = main_frame_after_reload.locator(
        "table, [role='grid'], [role='table'], "
        "[class*='table'], [class*='grid'], [id*='table']"
    ).first

    expect(config_table).to_be_visible(timeout=10000)

    # Search for 'Duplicate Waybill' in the table - it should NOT be present
    duplicate_waybill_entry = config_table.locator("text='Duplicate Waybill'")

    # Assert that the entry is NOT visible (count should be 0)
    expect(duplicate_waybill_entry).to_have_count(0)

    # Additionally verify by searching in the entire configuration section
    config_section_full = main_frame_after_reload.locator(
        "[id*='EquipmentActionReason'], [class*='equipment-action-reason'], "
        "section:has-text('Equipment Action Reason')"
    ).first

    all_text = config_section_full.inner_text()
    assert "Duplicate Waybill" not in all_text, (
        "ERROR: 'Duplicate Waybill' found in configuration after refresh. "
        "Unsaved changes were not discarded as expected."
    )

    # Verify that the Cancelled action section exists but without our new reason
    # This confirms we're looking at the right place and the data simply isn't there
    cancelled_rows = config_table.locator("tr:has-text('Cancelled'), [data-action='Cancelled']")
    if cancelled_rows.count() > 0:
        # Check that none of the Cancelled rows contain 'Duplicate Waybill'
        for i in range(cancelled_rows.count()):
            row_text = cancelled_rows.nth(i).inner_text()
            assert "Duplicate Waybill" not in row_text, (
                f"ERROR: Found 'Duplicate Waybill' in Cancelled action row after refresh: {row_text}"
            )
