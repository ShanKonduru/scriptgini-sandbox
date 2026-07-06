from playwright.sync_api import Page


class ConfigurationPage:
    """Page Object for DSP Configuration page - Equipment Action Reason Configuration."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.iframe = self.page.frame_locator('iframe[name*="PegaGadget"]')

        # Navigation
        self.configuration_link = self.page.locator('a:has-text("Configuration")')

        # Equipment Action Reason Configuration section
        self.equipment_action_config_heading = self.iframe.locator('text=Equipment Action Reason Configuration')

        # Dynamic row locators - will be set by selecting specific row
        self._current_row_index = None

    def navigate_to_configuration(self) -> None:
        """Navigate to Configuration page from the left menu."""
        self.configuration_link.click()
        self.page.wait_for_url("**/configurations**")

    def get_action_dropdown_for_row(self, row_index: int):
        """Get the action dropdown for a specific row (1-based index)."""
        return self.iframe.locator(f'select[name="$PpyDisplayHarness$pActionReason$l{row_index}$pParentKey"]')

    def get_reason_input_for_row(self, row_index: int):
        """Get the reason input field for a specific row (1-based index)."""
        return self.iframe.locator(f'input[name="$PpyDisplayHarness$pActionReason$l{row_index}$pKey"]')

    def get_audit_link_for_row(self, row_index: int):
        """Get the audit history link/icon for a specific row (1-based index)."""
        row = self.iframe.locator(f'tr:has(select[name="$PpyDisplayHarness$pActionReason$l{row_index}$pParentKey"])')
        return row.locator('a, button').last

    def find_row_with_action(self, action_name: str) -> int:
        """
        Find the row index (1-based) where the given action is already selected.
        Returns the row index or 0 if not found.
        """
        for i in range(1, 50):  # Check up to 50 rows
            select = self.get_action_dropdown_for_row(i)
            if select.count() > 0:
                selected_option = select.locator('option:checked')
                if selected_option.count() > 0:
                    text = selected_option.inner_text()
                    if text.strip() == action_name:
                        self._current_row_index = i
                        return i
        return 0

    def select_action(self, row_index: int, action_name: str) -> None:
        """Select an action from the dropdown for a specific row."""
        dropdown = self.get_action_dropdown_for_row(row_index)
        dropdown.select_option(label=action_name)
        self._current_row_index = row_index

    def update_reason(self, row_index: int, reason_text: str) -> None:
        """Update the reason text for a specific row."""
        reason_input = self.get_reason_input_for_row(row_index)
        reason_input.clear()
        reason_input.fill(reason_text)

    def get_selected_action(self, row_index: int) -> str:
        """Get the currently selected action text for a specific row."""
        dropdown = self.get_action_dropdown_for_row(row_index)
        return dropdown.locator('option:checked').inner_text()

    def get_reason_value(self, row_index: int) -> str:
        """Get the current reason text for a specific row."""
        reason_input = self.get_reason_input_for_row(row_index)
        return reason_input.input_value()

    def click_save_configuration(self) -> None:
        """Click the Save Configuration button."""
        save_button = self.iframe.locator('button:has-text("Save Configuration")').first()
        save_button.click()
        # Wait for save to complete
        self.page.wait_for_timeout(1000)

    def click_audit_history(self, row_index: int) -> None:
        """Click the audit history icon for a specific row to view audit log."""
        audit_link = self.get_audit_link_for_row(row_index)
        audit_link.click()
        # Wait for modal to appear
        self.page.wait_for_timeout(500)

    @property
    def audit_modal(self):
        """Get the audit history modal dialog."""
        return self.iframe.locator('[role="dialog"], .modal, [class*="modal"]').first()

    def is_audit_modal_visible(self) -> bool:
        """Check if audit history modal is visible."""
        return self.audit_modal.is_visible()
