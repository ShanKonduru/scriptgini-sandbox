"""
DSP Configuration Page Object
Handles navigation and interactions within the DSP Configuration module.
Pega applications typically use iframes for content rendering.
"""
from playwright.sync_api import Page, FrameLocator


class DSPConfigurationPage:
    """Page object for DSP Configuration interactions."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def get_main_content_frame(self) -> FrameLocator:
        """
        Pega applications render content in iframes.
        Try common iframe names used by Pega.
        """
        # Try multiple iframe selectors as Pega uses dynamic iframe names
        iframe_selectors = [
            "iframe[name^='PegaGadget']",
            "iframe[id^='PegaGadget']",
            "iframe.content-frame",
            "iframe[title='Main Content']"
        ]

        for selector in iframe_selectors:
            if self.page.locator(selector).count() > 0:
                return self.page.frame_locator(selector).first

        # If no iframe found, work directly with page
        return None

    def click_configuration_icon(self) -> None:
        """
        Click the Configuration icon in the navigation menu.
        Pega typically has configuration in the top menu bar or sidebar.
        """
        # Try multiple selector strategies
        config_button = (
            self.page.get_by_role("button", name="Configuration")
            .or_(self.page.get_by_role("link", name="Configuration"))
            .or_(self.page.locator("button[title*='Configuration' i]"))
            .or_(self.page.locator("a[title*='Configuration' i]"))
            .or_(self.page.locator("[data-test-id*='config' i]"))
            .or_(self.page.locator("button:has-text('Configuration')"))
        )
        config_button.first.click()
        self.page.wait_for_load_state("networkidle")

    def navigate_to_equipment_action_reason_config(self) -> None:
        """
        Navigate to the Equipment Action Reason Configuration section.
        This might be a link, menu item, or expandable section.
        """
        frame = self.get_main_content_frame()

        if frame:
            # Work within iframe
            equipment_link = (
                frame.get_by_role("link", name="Equipment Action Reason")
                .or_(frame.locator("a:has-text('Equipment Action Reason')"))
                .or_(frame.locator("[data-test-id*='EquipmentActionReason']"))
            )
        else:
            # Work with page directly
            equipment_link = (
                self.page.get_by_role("link", name="Equipment Action Reason")
                .or_(self.page.locator("a:has-text('Equipment Action Reason')"))
                .or_(self.page.locator("[data-test-id*='EquipmentActionReason']"))
            )

        equipment_link.first.click()
        self.page.wait_for_load_state("networkidle")

    def find_and_click_action_reason_entry(self, action: str, reason: str) -> None:
        """
        Locate a table row containing the specified Action and Reason values, then click it.
        Pega uses table-based layouts extensively.
        """
        frame = self.get_main_content_frame()

        # Build a selector that finds a row containing both values
        # XPath is more suitable for complex table queries in Pega
        row_xpath = f"//tr[contains(., '{action}') and contains(., '{reason}')]"

        if frame:
            row = frame.locator(f"xpath={row_xpath}")
        else:
            row = self.page.locator(f"xpath={row_xpath}")

        row.first.click()
        self.page.wait_for_timeout(500)  # Allow form to load

    def clear_reason_field(self) -> None:
        """
        Clear the Reason field by filling it with an empty string.
        """
        frame = self.get_main_content_frame()

        # Try multiple strategies to find the reason field
        if frame:
            reason_field = (
                frame.locator("input[name*='Reason' i]")
                .or_(frame.locator("textarea[name*='Reason' i]"))
                .or_(frame.locator("input[id*='Reason' i]"))
                .or_(frame.locator("input[placeholder*='Reason' i]"))
            )
        else:
            reason_field = (
                self.page.locator("input[name*='Reason' i]")
                .or_(self.page.locator("textarea[name*='Reason' i]"))
                .or_(self.page.locator("input[id*='Reason' i]"))
                .or_(self.page.locator("input[placeholder*='Reason' i]"))
            )

        reason_field.first.clear()
        # Alternative: reason_field.first.fill("")

    def click_save_configuration(self) -> None:
        """
        Click the Save button to save configuration changes.
        """
        frame = self.get_main_content_frame()

        if frame:
            save_button = (
                frame.get_by_role("button", name="Save")
                .or_(frame.locator("button:has-text('Save')"))
                .or_(frame.locator("button[type='submit']"))
                .or_(frame.locator("input[type='submit'][value*='Save' i]"))
            )
        else:
            save_button = (
                self.page.get_by_role("button", name="Save")
                .or_(self.page.locator("button:has-text('Save')"))
                .or_(self.page.locator("button[type='submit']"))
                .or_(self.page.locator("input[type='submit'][value*='Save' i]"))
            )

        save_button.first.click()
        self.page.wait_for_load_state("networkidle")
