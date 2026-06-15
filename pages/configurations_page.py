from playwright.sync_api import Page, FrameLocator


class ConfigurationsPage:
    """Page Object for the Configurations page with Equipment Action Reason Configuration."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Main navigation
        self.configurations_link = page.locator('a:has-text("Configurations")')
        # Iframe containing the configuration forms
        self.config_iframe = page.frame_locator('iframe[id="PegaGadget6ef5dIfr"]')

    def navigate_to_configurations(self) -> None:
        """Click on Configurations link in the left menu."""
        self.configurations_link.click()
        self.page.wait_for_url("**/configurations")
        self.page.wait_for_timeout(2000)

    def scroll_to_equipment_action_reason_section(self) -> None:
        """Scroll to the Equipment Action Reason Configuration section."""
        self.config_iframe.locator("text=Equipment Action Reason Configuration").first().scroll_into_view_if_needed()
        self.page.wait_for_timeout(1000)

    def click_add_equipment_action_reason(self) -> None:
        """Click the Add button in the Equipment Action Reason Configuration section."""
        # Access the iframe content
        iframe_element = self.page.locator('iframe[id="PegaGadget6ef5dIfr"]').element_handle()
        iframe_content = iframe_element.content_frame()

        # Find the Equipment Action Reason Configuration heading
        equipment_heading = iframe_content.locator("text=Equipment Action Reason Configuration").first()

        # Navigate to parent container to find the section's Add button
        section_container = equipment_heading.locator('xpath=ancestor::div[contains(@class, "content")]').first()

        # Find and click the Add button within this section
        add_button = section_container.locator("button.pzbutton").filter(has_text="Add").first()
        add_button.click()
        self.page.wait_for_timeout(1500)

    def select_action_in_last_row(self, action: str) -> None:
        """Select an action from the dropdown in the last row."""
        iframe_element = self.page.locator('iframe[id="PegaGadget6ef5dIfr"]').element_handle()
        iframe_content = iframe_element.content_frame()

        # Find all action dropdowns
        action_selects = iframe_content.locator('select[name*="pActionReason"][name*="pParentKey"]').all()

        # Get the last one (newly added row)
        last_select = action_selects[-1]
        last_select.select_option(label=action)
        self.page.wait_for_timeout(1000)

    def enter_reason_in_last_row(self, reason: str) -> None:
        """Enter reason text in the last row."""
        iframe_element = self.page.locator('iframe[id="PegaGadget6ef5dIfr"]').element_handle()
        iframe_content = iframe_element.content_frame()

        # Find all reason input fields
        reason_inputs = iframe_content.locator('input[name*="pActionReason"][name*="pKey"]').all()

        # Find the last empty input or use the last one
        target_input = None
        for i in range(len(reason_inputs) - 1, -1, -1):
            value = reason_inputs[i].input_value()
            if not value or value.strip() == "":
                target_input = reason_inputs[i]
                break

        if not target_input:
            target_input = reason_inputs[-1]

        # Clear and fill the reason field
        target_input.clear()
        target_input.fill(reason)
        self.page.wait_for_timeout(1000)

    def click_save_configuration(self) -> None:
        """Click the Save configurations button in the Equipment Action Reason Configuration section."""
        iframe_element = self.page.locator('iframe[id="PegaGadget6ef5dIfr"]').element_handle()
        iframe_content = iframe_element.content_frame()

        # Find the Equipment Action Reason Configuration heading
        equipment_heading = iframe_content.locator("text=Equipment Action Reason Configuration").first()

        # Navigate to parent container
        section_container = equipment_heading.locator('xpath=ancestor::div[contains(@class, "content")]').first()

        # Find and click the Save button within this section
        save_button = section_container.locator("button.pzbutton").filter(has_text="Save configurations").first()
        save_button.click()
        self.page.wait_for_timeout(2000)

    def verify_action_reason_exists(self, action: str, reason: str) -> bool:
        """
        Verify that a specific action-reason combination exists in the table.
        Returns True if found, False otherwise.
        """
        iframe_element = self.page.locator('iframe[id="PegaGadget6ef5dIfr"]').element_handle()
        iframe_content = iframe_element.content_frame()

        # Get all action dropdowns and reason inputs
        action_selects = iframe_content.locator('select[name*="pActionReason"][name*="pParentKey"]').all()
        reason_inputs = iframe_content.locator('input[name*="pActionReason"][name*="pKey"]').all()

        # Check if the combination exists
        for i in range(len(action_selects)):
            selected_option = action_selects[i].locator("option[selected]").first()
            action_text = selected_option.text_content() if selected_option.count() > 0 else ""
            reason_text = reason_inputs[i].input_value() if i < len(reason_inputs) else ""

            if action_text == action and reason in reason_text:
                return True

        return False

    def get_action_reason_count(self, action: str, reason: str) -> int:
        """
        Count how many times a specific action-reason combination appears in the table.
        """
        iframe_element = self.page.locator('iframe[id="PegaGadget6ef5dIfr"]').element_handle()
        iframe_content = iframe_element.content_frame()

        # Get all action dropdowns and reason inputs
        action_selects = iframe_content.locator('select[name*="pActionReason"][name*="pParentKey"]').all()
        reason_inputs = iframe_content.locator('input[name*="pActionReason"][name*="pKey"]').all()

        count = 0
        for i in range(len(action_selects)):
            selected_option = action_selects[i].locator("option[selected]").first()
            action_text = selected_option.text_content() if selected_option.count() > 0 else ""
            reason_text = reason_inputs[i].input_value() if i < len(reason_inputs) else ""

            if action_text == action and reason in reason_text:
                count += 1

        return count
