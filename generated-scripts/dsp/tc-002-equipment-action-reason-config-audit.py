import os
import pytest
from playwright.sync_api import Page, expect


def test_tc_002_equipment_action_reason_config_audit(page: Page):
    """
    Title: TC-002 Equipment Action Reason Configuration - Audit Icon Verification
    Business Intent: Verify that the Equipment Action Reason Configuration section
                     displays the correct column headers (Action, Reason, Audit History)
                     and that each reason entry has an associated Audit icon.
    Preconditions: Valid DSP user credentials must be available via environment variables
                   DSP_USERNAME and DSP_PASSWORD. User must have access to Configuration
                   and Equipment Action Reason Configuration sections.
    """
    # --- Arrange ---
    dsp_username = os.getenv("DSP_USERNAME", "")
    dsp_password = os.getenv("DSP_PASSWORD", "")
    base_url = os.getenv("DSP_BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth/")

    assert dsp_username, "DSP_USERNAME environment variable must be set"
    assert dsp_password, "DSP_PASSWORD environment variable must be set"

    # --- Act & Assert ---

    # Step 1: Clear browser cookies and cache (handled automatically by pytest-playwright per-test context)
    # Step 2: Navigate to base URL
    page.goto(base_url, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")

    # Step 3: Click on 'Login with Despachoprevio' button
    login_with_despachoprevio = page.get_by_role("link", name="Login with despachoprevio").or_(
        page.get_by_role("link", name="despachoprevio")
    ).or_(
        page.locator("a[href*='despachoprevio']")
    ).first
    expect(login_with_despachoprevio).to_be_visible(timeout=10000)
    login_with_despachoprevio.click()

    # Wait for SSO redirect and authentication page
    page.wait_for_load_state("networkidle")

    # Handle Microsoft SSO login if redirected
    # Check if we're on Microsoft login page
    if "login.microsoftonline.com" in page.url or "microsoftonline" in page.url:
        # Fill email/username field
        email_input = page.get_by_placeholder("Email, phone, or Skype").or_(
            page.locator("input[type='email'], input[name='loginfmt']")
        ).first
        expect(email_input).to_be_visible(timeout=10000)
        email_input.fill(dsp_username)

        # Click Next button
        next_button = page.get_by_role("button", name="Next").or_(
            page.locator("input[type='submit'][value='Next']")
        ).first
        expect(next_button).to_be_visible(timeout=5000)
        next_button.click()

        # Wait for password page
        page.wait_for_load_state("networkidle")

        # Fill password field
        password_input = page.get_by_placeholder("Password").or_(
            page.locator("input[type='password'], input[name='passwd']")
        ).first
        expect(password_input).to_be_visible(timeout=10000)
        password_input.fill(dsp_password)

        # Click Sign in button
        sign_in_button = page.get_by_role("button", name="Sign in").or_(
            page.locator("input[type='submit'][value='Sign in']")
        ).first
        expect(sign_in_button).to_be_visible(timeout=5000)
        sign_in_button.click()

        # Handle "Stay signed in?" prompt if it appears
        page.wait_for_load_state("networkidle")
        stay_signed_in_no = page.get_by_role("button", name="No").or_(
            page.locator("input[type='button'][value='No']")
        )
        if stay_signed_in_no.count() > 0:
            stay_signed_in_no.first.click()

    # Wait for successful login and redirect to Pega application
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)  # Allow Pega application to initialize

    # Verify we're logged in (no longer on auth page)
    expect(page).to_have_url(lambda url: "PRAuth" not in url or "default" in url, timeout=20000)

    # Step 4: Click on Configuration icon from the left menu
    # Pega applications typically use left navigation with icons
    # Look for Configuration menu item using multiple strategies
    configuration_menu = page.get_by_role("button", name="Configuration").or_(
        page.get_by_role("link", name="Configuration")
    ).or_(
        page.locator(
            "[title='Configuration'], "
            "[aria-label='Configuration'], "
            "nav a:has-text('Configuration'), "
            "nav button:has-text('Configuration'), "
            ".pega-nav a:has-text('Configuration'), "
            "[data-node-id*='Configuration'], "
            "a[data-test-id*='Configuration']"
        )
    ).first

    expect(configuration_menu).to_be_visible(timeout=15000)
    configuration_menu.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)  # Allow submenu to expand

    # Step 5: Navigate to Equipment Action Reason Configuration section
    equipment_action_reason_config = page.get_by_role("link", name="Equipment Action Reason Configuration").or_(
        page.get_by_role("button", name="Equipment Action Reason Configuration")
    ).or_(
        page.locator(
            "a:has-text('Equipment Action Reason Configuration'), "
            "button:has-text('Equipment Action Reason Configuration'), "
            "[title*='Equipment Action Reason'], "
            "[aria-label*='Equipment Action Reason']"
        )
    ).first

    expect(equipment_action_reason_config).to_be_visible(timeout=15000)
    equipment_action_reason_config.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)  # Allow configuration table to load

    # Step 6: Verify column headers are displayed: Action, Reason and Audit History
    # Pega tables typically use th elements or div with role='columnheader'
    action_header = page.locator(
        "th:has-text('Action'), "
        "[role='columnheader']:has-text('Action'), "
        ".column-header:has-text('Action'), "
        "thead th:text-is('Action')"
    ).first
    expect(action_header).to_be_visible(timeout=10000)

    reason_header = page.locator(
        "th:has-text('Reason'), "
        "[role='columnheader']:has-text('Reason'), "
        ".column-header:has-text('Reason'), "
        "thead th:text-is('Reason')"
    ).first
    expect(reason_header).to_be_visible(timeout=10000)

    audit_history_header = page.locator(
        "th:has-text('Audit History'), "
        "[role='columnheader']:has-text('Audit History'), "
        ".column-header:has-text('Audit History'), "
        "thead th:text-is('Audit History')"
    ).first
    expect(audit_history_header).to_be_visible(timeout=10000)

    # Step 7: Verify Audit icon is present next to each reason in the configuration table
    # Locate the table body and all rows
    table_body = page.locator(
        "tbody, "
        "[role='rowgroup'], "
        ".table-body, "
        "table tbody"
    ).first
    expect(table_body).to_be_visible(timeout=10000)

    # Get all data rows (excluding header rows)
    data_rows = page.locator(
        "tbody tr, "
        "[role='row']:not([role='row'][class*='header']), "
        "table tbody tr"
    )

    # Ensure at least one row exists
    row_count = data_rows.count()
    assert row_count > 0, "Expected at least one row in Equipment Action Reason Configuration table"

    # Verify each row has an audit icon
    # Audit icons are typically represented by:
    # - Icons with 'audit' in class/id/title/aria-label
    # - History icons
    # - Clock/time icons
    for i in range(row_count):
        row = data_rows.nth(i)

        # Look for audit icon within the row using multiple strategies
        audit_icon = row.locator(
            "[title*='Audit' i], "
            "[aria-label*='Audit' i], "
            "[class*='audit' i], "
            "[data-icon*='audit' i], "
            "[title*='History' i], "
            "[aria-label*='History' i], "
            "button[title*='Audit' i], "
            "a[title*='Audit' i], "
            "i[class*='history'], "
            "svg[class*='audit'], "
            "img[alt*='Audit' i]"
        ).first

        expect(audit_icon).to_be_visible(
            timeout=5000
        ), f"Expected Audit icon to be visible in row {i + 1}"

    # Final verification: Print row count for logging
    print(f"✓ Verified {row_count} rows in Equipment Action Reason Configuration table")
    print(f"✓ All {row_count} rows have Audit icons present")
