"""
DSP Configuration Page Object
Handles interactions on the Configuration page including Equipment Action Reason Configuration
"""
from playwright.sync_api import Page, expect


class ConfigurationPage:
    """Page object for DSP Configuration page"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators
        self.equipment_action_reason_container = page.locator(
            "[class*='equipment-action'], "
            "[id*='equipment-action'], "
            "text='Equipment Action Reason Configuration'"
        ).first
        self.save_configuration_button = page.get_by_role("button", name="Save Configuration").or_(
            page.locator("button:has-text('Save Configuration'), button:has-text('Save'), button[type='submit']")
        ).first

    def verify_configuration_page_loaded(self) -> None:
        """Verify Configuration page is displayed"""
        expect(self.equipment_action_reason_container).to_be_visible(timeout=10000)

    def select_action_no_despacho_previo(self) -> None:
        """
        Inside Equipment Action Reason Configuration container,
        select existing action 'No Despacho Previo'
        """
        # Look for 'No Despacho Previo' action within the container
        action_item = self.equipment_action_reason_container.locator(
            "text='No Despacho Previo', "
            "[data-action='No Despacho Previo'], "
            "div:has-text('No Despacho Previo'), "
            "label:has-text('No Despacho Previo')"
        ).first
        expect(action_item).to_be_visible(timeout=10000)
        action_item.click()

    def get_reason_text_field(self):
        """
        Get the reason text field locator (editable field for action reason)
        Returns a locator that can be used to fill/clear text
        """
        # Look for text input, textarea, or contenteditable field
        reason_field = self.page.locator(
            "input[name*='reason' i], "
            "textarea[name*='reason' i], "
            "[contenteditable='true'], "
            "input[type='text']:focus, "
            "textarea:focus"
        ).first
        return reason_field

    def update_reason_text(self, new_reason: str) -> None:
        """Update the reason text to the new value"""
        reason_field = self.get_reason_text_field()
        expect(reason_field).to_be_visible(timeout=10000)
        expect(reason_field).to_be_editable(timeout=5000)
        reason_field.clear()
        reason_field.fill(new_reason)

    def click_save_configuration(self) -> None:
        """Click on 'Save Configuration' button"""
        self.save_configuration_button.click()
        self.page.wait_for_load_state("networkidle")

    def verify_reason_saved(self, expected_reason: str) -> None:
        """
        Verify that the updated reason is present in the configuration
        for 'No Despacho Previo' action
        """
        # Look for the expected reason text in the Equipment Action Reason Configuration area
        saved_reason = self.equipment_action_reason_container.locator(
            f"text='{expected_reason}', "
            f"[value='{expected_reason}'], "
            f"*:has-text('{expected_reason}')"
        ).first
        expect(saved_reason).to_be_visible(timeout=10000)
