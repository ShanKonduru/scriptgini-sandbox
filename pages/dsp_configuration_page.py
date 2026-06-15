"""
DSP Configuration Page Object
Handles navigation to configuration sections including General settings.
"""
from playwright.sync_api import Page, expect


class DSPConfigurationPage:
    """Page Object for DSP Configuration navigation."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators
        # IMPORTANT: DSP (Pega) applications often use:
        # - Nested iframes (use frame_locator() if needed)
        # - Dynamic table-based layouts
        # - Data attributes like data-test-id, pega-specific attributes
        # These selectors are best-practice but MUST be verified against the live app.

        # Configuration icon - typically in header/toolbar
        self.configuration_icon = page.get_by_role("button", name="configuration").or_(
            page.locator(
                "[aria-label*='configuration' i], "
                "[title*='configuration' i], "
                "button[data-testid*='config'], "
                "button:has-text('Configuration'), "
                "[class*='config-icon'], "
                "[id*='config']"
            )
        ).first

        # General menu item - typically in a dropdown or side menu
        self.general_menu_item = page.get_by_role("menuitem", name="general").or_(
            page.get_by_role("link", name="general")
        ).or_(
            page.locator(
                "a:has-text('General'), "
                "li:has-text('General'), "
                "[role='menuitem']:has-text('General'), "
                "nav a:has-text('General'), "
                "[data-testid*='general']"
            )
        ).first

    def click_configuration_icon(self) -> None:
        """Click the Configuration icon to open configuration menu."""
        expect(self.configuration_icon).to_be_visible(timeout=10000)
        self.configuration_icon.click()
        # Wait for menu/dropdown to appear
        self.page.wait_for_timeout(500)

    def click_general(self) -> None:
        """Click on General menu item in configuration."""
        expect(self.general_menu_item).to_be_visible(timeout=10000)
        self.general_menu_item.click()
        self.page.wait_for_load_state("networkidle")

    def is_on_general_page(self) -> bool:
        """Verify we are on the General configuration page."""
        # Check URL contains 'general' or page heading contains 'General'
        url = self.page.url.lower()
        if "general" in url:
            return True

        # Check for page heading
        heading = self.page.locator("h1, h2, [role='heading']").first
        if heading.count() > 0:
            heading_text = heading.inner_text().lower()
            return "general" in heading_text

        return False

    def navigate_to_general_configuration(self) -> None:
        """
        Complete navigation flow: Configuration icon -> General.
        """
        self.click_configuration_icon()
        self.click_general()
