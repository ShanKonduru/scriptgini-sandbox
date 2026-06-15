from playwright.sync_api import Page, expect, FrameLocator


class ConfigurationsPage:
    """Page Object for Configurations page with Equipment Action Reason Configuration"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.configurations_link = page.locator('a:has-text("Configurations")')

    def navigate_to_configurations(self) -> None:
        """Navigate to Configurations page from main menu"""
        expect(self.configurations_link).to_be_visible(timeout=10000)
        self.configurations_link.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def get_configuration_frame(self) -> FrameLocator:
        """Get the Pega iframe containing configuration content"""
        return self.page.frame_locator('iframe[name^="PegaGadget"]')

    def verify_equipment_action_reason_section_visible(self) -> None:
        """Verify Equipment Action Reason Configuration section is shown"""
        frame = self.get_configuration_frame()
        section_text = frame.locator('text=Equipment Action Reason Configuration')
        expect(section_text).to_be_visible(timeout=10000)

    def select_action_for_row(self, row_number: int, action: str) -> None:
        """Select action from dropdown for a specific row"""
        frame = self.get_configuration_frame()
        action_dropdown = frame.locator(f'select[name*="pActionReason$l{row_number}$pParentKey"]')
        action_dropdown.select_option(label=action)

    def update_reason_for_row(self, row_number: int, reason: str) -> None:
        """Update reason text for a specific row"""
        frame = self.get_configuration_frame()
        reason_input = frame.locator(f'input[name*="pActionReason$l{row_number}$pKey"]')
        reason_input.click()
        reason_input.fill(reason)

    def find_row_by_action_and_reason(self, action: str, reason: str) -> int:
        """Find row number by action and reason values (returns -1 if not found)"""
        frame = self.get_configuration_frame()
        for row_num in range(1, 43):
            try:
                select = frame.locator(f'select[name*="pActionReason$l{row_num}$pParentKey"]').first
                selected_value = select.input_value()
                selected_option = select.locator(f'option[value="{selected_value}"]')
                selected_text = selected_option.inner_text()

                if selected_text == action:
                    reason_input = frame.locator(f'input[name*="pActionReason$l{row_num}$pKey"]').first
                    reason_value = reason_input.input_value()
                    if reason_value == reason:
                        return row_num
            except Exception:
                continue
        return -1

    def click_save_configurations(self) -> None:
        """Click Save configurations button"""
        frame = self.get_configuration_frame()
        save_button = frame.locator('button:has-text("Save configurations")')
        expect(save_button).to_be_visible(timeout=10000)
        save_button.click()
        self.page.wait_for_timeout(2000)

    def verify_reason_in_table(self, action: str, reason: str) -> bool:
        """Verify that a specific action-reason pair exists in the configuration table"""
        row_num = self.find_row_by_action_and_reason(action, reason)
        return row_num != -1

    def get_all_action_reason_pairs(self) -> list:
        """Get all action-reason pairs from the configuration table"""
        frame = self.get_configuration_frame()
        pairs = []
        for row_num in range(1, 43):
            try:
                select = frame.locator(f'select[name*="pActionReason$l{row_num}$pParentKey"]').first
                selected_value = select.input_value()
                selected_option = select.locator(f'option[value="{selected_value}"]')
                action = selected_option.inner_text()

                if action and action != "Select":
                    reason_input = frame.locator(f'input[name*="pActionReason$l{row_num}$pKey"]').first
                    reason = reason_input.input_value()
                    pairs.append({"row": row_num, "action": action, "reason": reason})
            except Exception:
                continue
        return pairs
