import pytest
from playwright.sync_api import Page, expect


def test_tc_002_equipment_action_reason_blank_validation(page: Page):
    """
    Title: TC-002 Equipment Action Reason Configuration - Blank Reason Validation
    Business Intent: Verify that when adding a new Equipment Action Reason with the
                     'Cancelled' action but leaving the Reason field blank, appropriate
                     validation is triggered and the user is prevented from saving an
                     incomplete entry.
    Preconditions: Valid DSP user credentials must be available via environment variables
                   DSP_USERNAME and DSP_PASSWORD. User must have access to Configuration
                   section and Equipment Action Reason Configuration.
    """
    # --- Arrange ---
    import os

    dsp_username = os.getenv("DSP_USERNAME", "dsp_test_user")
    dsp_password = os.getenv("DSP_PASSWORD", "test_password")
    base_url = os.getenv("DSP_BASE_URL", "https://dsp-app-url.com")

    # --- Act & Assert ---

    # Step 1: Clear all browser cookies and cache
    page.context.clear_cookies()
    page.context.clear_permissions()

    # Step 2: Navigate to base URL
    page.goto(base_url, wait_until="networkidle")
    expect(page).not_to_have_url("about:blank")

    # Step 3: Click on 'Login with Despachoprevio' button
    # Pega applications often use specific login buttons or SSO integration
    login_with_despacho_button = page.get_by_role("button", name="Login with Despachoprevio").or_(
        page.get_by_role("link", name="Login with Despachoprevio")
    ).or_(
        page.locator("button:has-text('Login with Despachoprevio'), a:has-text('Login with Despachoprevio'), button[id*='despacho' i]")
    ).first
    expect(login_with_despacho_button).to_be_visible(timeout=15000)
    login_with_despacho_button.click()

    # Wait for login page to load (may redirect to SSO/OAuth provider)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # Step 4: Enter email address in the email field
    email_input = page.get_by_role("textbox", name="email").or_(
        page.get_by_label("Email")
    ).or_(
        page.locator("input[name='email'], input[id='email'], input[type='email'], input[placeholder*='email' i]")
    ).first
    expect(email_input).to_be_visible(timeout=10000)
    email_input.fill(dsp_username)

    # Step 5: Click on Next button
    next_button = page.get_by_role("button", name="Next").or_(
        page.locator("button:has-text('Next'), input[type='submit'][value*='Next' i], button[id*='next' i]")
    ).first
    expect(next_button).to_be_visible(timeout=10000)
    next_button.click()

    # Wait for password page to load
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # Step 6: Enter password in the password field
    password_input = page.get_by_role("textbox", name="password").or_(
        page.get_by_label("Password")
    ).or_(
        page.locator("input[name='password'], input[id='password'], input[type='password']")
    ).first
    expect(password_input).to_be_visible(timeout=10000)
    password_input.fill(dsp_password)

    # Step 7: Click on Sign in button
    sign_in_button = page.get_by_role("button", name="Sign in").or_(
        page.get_by_role("button", name="Login")
    ).or_(
        page.locator("button:has-text('Sign in'), button:has-text('Log in'), input[type='submit'][value*='Sign' i]")
    ).first
    expect(sign_in_button).to_be_visible(timeout=10000)
    sign_in_button.click()

    # Wait for successful login - expect dashboard or main page
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Step 8: If cookies acceptance popup appears, click on Accept button
    # This is a conditional step - check if popup exists before attempting to click
    cookies_accept_button = page.get_by_role("button", name="Accept").or_(
        page.get_by_role("button", name="Accept all")
    ).or_(
        page.locator("button:has-text('Accept'), button[id*='accept' i], button[class*='accept' i]")
    )

    # Wait briefly to see if cookies popup appears
    try:
        cookies_accept_button.first.wait_for(state="visible", timeout=3000)
        if cookies_accept_button.first.is_visible():
            cookies_accept_button.first.click()
            page.wait_for_timeout(500)
    except Exception:
        # No cookies popup - continue with test
        pass

    # Verify successful login by checking URL or presence of main navigation
    expect(page).to_have_url(lambda url: "login" not in url.lower(), timeout=15000)

    # Step 9: Click on Configuration icon from the left menu
    # Pega applications typically use left navigation with icons or text links
    configuration_menu = page.get_by_role("link", name="Configuration").or_(
        page.get_by_role("button", name="Configuration")
    ).or_(
        page.locator(
            "a[href*='config' i]:has-text('Configuration'), "
            "button:has-text('Configuration'), "
            "nav a:has-text('Configuration'), "
            "[data-test-id*='config' i], "
            ".nav-item:has-text('Configuration'), "
            "li:has-text('Configuration') a"
        )
    ).first
    expect(configuration_menu).to_be_visible(timeout=10000)
    configuration_menu.click()

    # Wait for configuration page to load
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)

    # Step 10: Verify Equipment Action Reason Configuration section is displayed
    equipment_action_reason_section = page.locator(
        "text=/Equipment Action Reason Configuration/i"
    ).or_(
        page.locator(
            "[class*='equipment' i][class*='action' i], "
            "section:has-text('Equipment Action Reason'), "
            "div:has-text('Equipment Action Reason Configuration'), "
            "[data-test-id*='equipment-action-reason' i]"
        )
    ).first
    expect(equipment_action_reason_section).to_be_visible(timeout=10000)

    # Step 11: Verify Equipment Action Reason Configuration table shows Action, Reason,
    # and Audit History columns with Add and Delete controls
    # Check for table headers
    action_column_header = page.locator("th:has-text('Action'), [data-column='action']").first
    expect(action_column_header).to_be_visible(timeout=5000)

    reason_column_header = page.locator("th:has-text('Reason'), [data-column='reason']").first
    expect(reason_column_header).to_be_visible(timeout=5000)

    audit_history_column_header = page.locator(
        "th:has-text('Audit History'), th:has-text('Audit'), [data-column='audit']"
    ).first
    expect(audit_history_column_header).to_be_visible(timeout=5000)

    # Verify Add button exists in the section
    add_button = page.locator(
        "button:has-text('Add'), button[class*='add' i], [data-test-id*='add' i]"
    ).first
    expect(add_button).to_be_visible(timeout=5000)

    # Verify Delete control exists (may be per-row or bulk action)
    delete_control = page.locator(
        "button:has-text('Delete'), [data-test-id*='delete' i], [class*='delete' i]"
    )
    # At least one delete control should be present
    expect(delete_control.first).to_be_attached()

    # Step 12: Click on Add button in Equipment Action Reason Configuration section
    add_button.click()
    page.wait_for_timeout(1000)

    # Verify that an add form/dialog appears
    # Pega applications often use inline editing or modal dialogs
    add_form = page.locator(
        "[role='dialog'], .modal, form:has-text('Add'), [class*='add-form' i], "
        "[class*='edit-form' i], [data-test-id*='add-form' i]"
    ).first
    # The form may be inline or modal - check if it exists
    if add_form.count() > 0:
        expect(add_form).to_be_visible(timeout=5000)

    # Step 13: Select 'Cancelled' action from the Action dropdown
    action_dropdown = page.get_by_role("combobox", name="Action").or_(
        page.get_by_label("Action")
    ).or_(
        page.locator(
            "select[name*='action' i], select[id*='action' i], "
            "[data-test-id*='action-dropdown' i], "
            "select[class*='action' i]"
        )
    ).first
    expect(action_dropdown).to_be_visible(timeout=10000)

    # Select 'Cancelled' option
    # Try different approaches for selecting the option
    try:
        action_dropdown.select_option(label="Cancelled")
    except Exception:
        try:
            action_dropdown.select_option(value="Cancelled")
        except Exception:
            # If standard select doesn't work, may be a custom dropdown
            action_dropdown.click()
            page.wait_for_timeout(500)
            cancelled_option = page.locator(
                "li:has-text('Cancelled'), option:has-text('Cancelled'), "
                "[role='option']:has-text('Cancelled'), div:has-text('Cancelled')"
            ).first
            cancelled_option.click()

    page.wait_for_timeout(500)

    # Step 14: Leave the Reason text box empty/blank
    # Locate the Reason field but do NOT fill it
    reason_input = page.get_by_role("textbox", name="Reason").or_(
        page.get_by_label("Reason")
    ).or_(
        page.locator(
            "input[name*='reason' i], input[id*='reason' i], "
            "textarea[name*='reason' i], textarea[id*='reason' i], "
            "[data-test-id*='reason-input' i]"
        )
    ).first
    expect(reason_input).to_be_visible(timeout=10000)

    # Explicitly verify the field is empty
    reason_value = reason_input.input_value()
    assert reason_value == "" or reason_value is None, f"Reason field should be empty but contains: {reason_value}"

    # Step 15: Click outside of the Reason text box to trigger validation
    # Click on a neutral area to trigger blur event on the Reason field
    # Find a safe element to click (like a label, heading, or form container)
    safe_click_target = page.locator(
        "label:not([for*='reason' i]), h1, h2, h3, .form-header, [role='heading']"
    ).first.or_(
        page.locator("body")
    ).first

    # Click outside to trigger blur/validation
    safe_click_target.click(force=True)
    page.wait_for_timeout(1000)

    # Verify validation error appears
    # Look for validation messages near the Reason field or general error messages
    validation_error = page.locator(
        "text=/required/i, text=/cannot be empty/i, text=/mandatory/i, "
        "text=/must not be blank/i, [class*='error' i]:has-text('Reason'), "
        "[class*='validation' i], .error-message, .validation-message, "
        "[role='alert']:has-text('Reason'), span[class*='error' i]"
    ).first

    # Assert that validation error is visible
    expect(validation_error).to_be_visible(timeout=5000)

    # Additional assertion: verify error message contains relevant text
    error_text = validation_error.inner_text()
    assert len(error_text.strip()) > 0, "Validation error message is empty"

    # Check that the error is related to the Reason field being required
    error_keywords = ["required", "mandatory", "empty", "blank", "must", "field"]
    assert any(
        keyword in error_text.lower() for keyword in error_keywords
    ), f"Validation error does not contain expected keywords. Error text: {error_text}"

    # Optional: Verify that Save/Submit button is disabled or that save action fails
    save_button = page.locator(
        "button:has-text('Save'), button:has-text('Submit'), "
        "button[type='submit'], [data-test-id*='save' i]"
    ).first

    if save_button.count() > 0 and save_button.is_visible():
        # Check if button is disabled
        is_disabled = save_button.is_disabled()
        assert is_disabled, "Save button should be disabled when Reason field is blank"
