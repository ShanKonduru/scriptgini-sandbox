import os
import pytest
from playwright.sync_api import Page, expect


def test_tc_002_equipment_action_reason_config_verification(page: Page):
    """
    Title: TC-002 Equipment Action Reason Configuration Verification
    Business Intent: Verify that the Equipment Action Reason Configuration section
                     displays all required actions and their associated reasons correctly.
    Preconditions: Valid Despachoprevio SSO credentials must be available
    Test Steps:
      1. Navigate to base URL: https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth
      2. Click on 'Login with Despachoprevio' button to authenticate
      3. Click on Configuration icon from the left menu
      4. Navigate to Equipment Action Reason Configuration section
      5. Verify presence of all specified actions and their associated reasons
    """
    # --- Arrange ---
    base_url = os.getenv(
        "DSP_BASE_URL",
        "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth"
    )

    # Expected actions and reasons for validation
    # Note: Update this list based on actual business requirements
    expected_actions = [
        "Cargue Diferido",
        "Descargue Diferido",
        "Liberación Diferida",
        "No Despacho previo",
        "Rechazo",
    ]

    # --- Act & Assert ---

    # Step 1: Navigate to base URL
    page.goto(base_url, wait_until="networkidle")
    expect(page).to_have_title("Login Page", timeout=10000)

    # Step 2: Click on 'Login with Despachoprevio' button to authenticate
    despachoprevio_button = page.get_by_role("button", name="Login with despachoprevio")
    expect(despachoprevio_button).to_be_visible(timeout=10000)
    despachoprevio_button.click()

    # Wait for SSO authentication to complete
    # The application redirects to Microsoft SSO, then back to Pega after auth
    # User must complete authentication manually or via pre-configured session
    page.wait_for_load_state("networkidle")

    # Wait for post-login page to load (expect URL to contain /prweb/ or application identifier)
    # Timeout extended to allow SSO authentication flow
    page.wait_for_url("**/prweb/**", timeout=60000)
    page.wait_for_load_state("networkidle")

    # Additional stabilization wait for Pega application to fully initialize
    page.wait_for_timeout(2000)

    # Step 3: Click on Configuration icon from the left menu
    # Pega applications typically use iframe-based layout for navigation
    # Look for Configuration menu item in left navigation panel

    # Try multiple selector strategies for Configuration menu
    config_menu_item = page.locator(
        "a:has-text('Configuration'), "
        "a:has-text('Configuración'), "
        "[data-test-id*='config'], "
        "[aria-label*='Configuration'], "
        "nav a:has-text('Configuration'), "
        ".pega-menu-item:has-text('Configuration')"
    ).first

    # If Configuration is within an iframe, locate the frame first
    # Pega often uses PegaGadget frames for navigation
    main_frame = page.frame_locator("iframe[name*='PegaGadget'], iframe[id*='main']").first
    if main_frame:
        config_menu_frame = main_frame.locator(
            "a:has-text('Configuration'), "
            "span:has-text('Configuration'), "
            "[role='menuitem']:has-text('Configuration')"
        ).first
        if config_menu_frame.count() > 0:
            expect(config_menu_frame).to_be_visible(timeout=15000)
            config_menu_frame.click()
        else:
            # Fallback to page-level selector
            expect(config_menu_item).to_be_visible(timeout=15000)
            config_menu_item.click()
    else:
        # No iframe detected, use page-level selector
        expect(config_menu_item).to_be_visible(timeout=15000)
        config_menu_item.click()

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)

    # Step 4: Navigate to Equipment Action Reason Configuration section
    equipment_action_config_link = page.locator(
        "a:has-text('Equipment Action Reason Configuration'), "
        "a:has-text('Equipment Action Reason'), "
        "span:has-text('Equipment Action Reason Configuration'), "
        "[role='link']:has-text('Equipment Action Reason'), "
        "[data-test-id*='equipment-action-reason']"
    ).first

    # Check within iframe if present
    if main_frame:
        equipment_action_frame = main_frame.locator(
            "a:has-text('Equipment Action Reason Configuration'), "
            "a:has-text('Equipment Action Reason'), "
            "span:has-text('Equipment Action Reason Configuration')"
        ).first
        if equipment_action_frame.count() > 0:
            expect(equipment_action_frame).to_be_visible(timeout=15000)
            equipment_action_frame.click()
        else:
            expect(equipment_action_config_link).to_be_visible(timeout=15000)
            equipment_action_config_link.click()
    else:
        expect(equipment_action_config_link).to_be_visible(timeout=15000)
        equipment_action_config_link.click()

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Step 5: Verify presence of all specified actions and their associated reasons
    # Pega typically renders configuration data in tables or grid layouts
    # Look for table structure containing actions and reasons

    # Locate the main configuration table/grid
    config_table = page.locator(
        "table, "
        "[role='grid'], "
        "[role='table'], "
        ".pega-table, "
        ".pega-grid, "
        "[data-test-id*='config-table'], "
        "[class*='config-table']"
    ).first

    # Check within iframe if present
    if main_frame:
        config_table_frame = main_frame.locator(
            "table, "
            "[role='grid'], "
            "[role='table'], "
            ".pega-table"
        ).first
        if config_table_frame.count() > 0:
            expect(config_table_frame).to_be_visible(timeout=15000)
            # Verify each expected action is present in the table
            for action_name in expected_actions:
                action_cell = config_table_frame.locator(
                    f"td:has-text('{action_name}'), "
                    f"[role='gridcell']:has-text('{action_name}'), "
                    f"span:has-text('{action_name}')"
                ).first
                expect(action_cell).to_be_visible(
                    timeout=10000
                ), f"Action '{action_name}' not found in configuration table"

                # Verify associated reason column exists for this action
                # Pega tables typically have consistent row structure
                action_row = action_cell.locator("xpath=ancestor::tr").first
                reason_cell = action_row.locator(
                    "td:nth-child(2), "
                    "[role='gridcell']:nth-child(2), "
                    ".reason-column"
                ).first
                expect(reason_cell).to_be_visible(
                    timeout=5000
                ), f"Reason column not found for action '{action_name}'"

                # Verify reason cell is not empty
                reason_text = reason_cell.inner_text()
                assert reason_text.strip() != "", \
                    f"Reason for action '{action_name}' is empty"
        else:
            # Fallback to page-level table
            expect(config_table).to_be_visible(timeout=15000)
            for action_name in expected_actions:
                action_cell = config_table.locator(
                    f"td:has-text('{action_name}'), "
                    f"[role='gridcell']:has-text('{action_name}')"
                ).first
                expect(action_cell).to_be_visible(
                    timeout=10000
                ), f"Action '{action_name}' not found in configuration table"

                action_row = action_cell.locator("xpath=ancestor::tr").first
                reason_cell = action_row.locator("td:nth-child(2)").first
                expect(reason_cell).to_be_visible(
                    timeout=5000
                ), f"Reason column not found for action '{action_name}'"

                reason_text = reason_cell.inner_text()
                assert reason_text.strip() != "", \
                    f"Reason for action '{action_name}' is empty"
    else:
        # No iframe, use page-level validation
        expect(config_table).to_be_visible(timeout=15000)
        for action_name in expected_actions:
            action_cell = config_table.locator(
                f"td:has-text('{action_name}'), "
                f"[role='gridcell']:has-text('{action_name}')"
            ).first
            expect(action_cell).to_be_visible(
                timeout=10000
            ), f"Action '{action_name}' not found in configuration table"

            action_row = action_cell.locator("xpath=ancestor::tr").first
            reason_cell = action_row.locator("td:nth-child(2)").first
            expect(reason_cell).to_be_visible(
                timeout=5000
            ), f"Reason column not found for action '{action_name}'"

            reason_text = reason_cell.inner_text()
            assert reason_text.strip() != "", \
                f"Reason for action '{action_name}' is empty"

    # Final validation: count total actions displayed
    all_action_rows = config_table.locator("tr").count()
    assert all_action_rows >= len(expected_actions), \
        f"Expected at least {len(expected_actions)} action rows, found {all_action_rows}"
