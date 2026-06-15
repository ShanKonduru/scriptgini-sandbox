"""
Test Case: DSP Configuration - Navigate to General Settings
Test ID: TC-002 (inferred)
Business Intent: Verify that a Super User can access the General configuration section
                 through the Configuration menu.
Preconditions: Valid DSP Super User credentials must be available via environment variables.
"""
import os
import pytest
from playwright.sync_api import Page, expect

from pages.dsp_login_page import DSPLoginPage
from pages.dsp_configuration_page import DSPConfigurationPage


def test_navigate_to_general_configuration(page: Page):
    """
    Test Steps:
    1. Log in DSP with Super User credentials
    2. Click on Configuration icon
    3. Click on General

    Expected Result: User successfully navigates to the General configuration page.
    """
    # --- Arrange ---
    base_url = os.getenv("DSP_BASE_URL", "https://dsp-app-url.com")

    # Initialize page objects
    login_page = DSPLoginPage(page)
    config_page = DSPConfigurationPage(page)

    # --- Act ---

    # Step 1: Log in DSP with Super User credentials
    login_page.login_as_super_user(base_url)

    # Step 2: Click on Configuration icon
    config_page.click_configuration_icon()

    # Step 3: Click on General
    config_page.click_general()

    # --- Assert ---

    # Verify navigation to General configuration page
    assert config_page.is_on_general_page(), "Failed to navigate to General configuration page"

    # Additional validation: Check URL or page heading
    page_url = page.url.lower()
    assert "general" in page_url or "config" in page_url, (
        f"Expected URL to contain 'general' or 'config', but got: {page_url}"
    )

    # Verify page is loaded and stable
    expect(page.locator("body")).to_be_visible(timeout=5000)
