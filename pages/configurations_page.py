from playwright.sync_api import Page, FrameLocator


class ConfigurationsPage:
    """Page object for the Configurations page with Equipment Action Reason Configuration."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.configurations_link = page.get_by_role("link", name="Configurations")

    def navigate_to_configurations(self) -> None:
        """Click on the Configurations menu item."""
        self.configurations_link.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)

    def get_main_content_frame(self) -> FrameLocator:
        """Get the main content iframe where the configuration form is loaded."""
        return self.page.frame_locator('iframe[name="PegaGadget0a7ebIfr"]')

    def verify_equipment_action_reason_section_visible(self) -> bool:
        """Verify that Equipment Action Reason Configuration section is displayed."""
        frame = self.get_main_content_frame()
        section_heading = frame.locator("text=Equipment Action Reason Configuration")
        return section_heading.is_visible()

    def find_action_reason_row(self, action_name: str) -> tuple:
        """
        Find the row for a specific action and return the input field locator and current value.

        Returns:
            tuple: (input_locator, current_value) or (None, None) if not found
        """
        frame = self.get_main_content_frame()

        rows = frame.locator("tr").all()
        for row in rows:
            select_element = row.locator("select").first
            if select_element.count() > 0:
                selected_value = select_element.input_value()
                if action_name in selected_value:
                    input_field = row.locator("input[type='text']").first
                    if input_field.count() > 0:
                        current_value = input_field.input_value()
                        return (input_field, current_value)

        return (None, None)

    def clear_reason_for_action(self, action_name: str) -> None:
        """Clear the reason text for a specific action."""
        input_field, _ = self.find_action_reason_row(action_name)
        if input_field:
            input_field.click(click_count=3)
            input_field.press("Backspace")

    def enter_reason_for_action(self, action_name: str, reason_text: str) -> None:
        """Enter reason text for a specific action."""
        input_field, _ = self.find_action_reason_row(action_name)
        if input_field:
            input_field.fill(reason_text)

    def click_save_configurations(self) -> None:
        """Click the Save configurations button."""
        frame = self.get_main_content_frame()
        save_button = frame.locator('button[name="DSPConfiguration_pyDisplayHarness_13"]')
        save_button.scroll_into_view_if_needed()
        save_button.click()
        self.page.wait_for_timeout(2000)

    def get_alert_message(self) -> str:
        """Get the text of any alert/notification message displayed."""
        frame = self.get_main_content_frame()
        try:
            alert = frame.locator('[role="alert"]').first
            alert.wait_for(state="visible", timeout=5000)
            return alert.text_content()
        except Exception:
            return ""

    def is_error_displayed(self) -> bool:
        """Check if an error message is displayed (not a success message)."""
        message = self.get_alert_message()
        return bool(message) and "success" not in message.lower()

    def is_success_displayed(self) -> bool:
        """Check if a success message is displayed."""
        message = self.get_alert_message()
        return "success" in message.lower()
