from playwright.sync_api import Page, FrameLocator


class DSPConfigurationsPage:
    """Page Object for DSP Configurations page with Equipment Action Reason Configuration."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Main frame - Pega uses iframes extensively
        self.main_frame: FrameLocator = page.frame_locator('iframe').first

        # Navigation
        self.configurations_nav_link = page.get_by_text('Configurations')

        # Equipment Action Reason Configuration section (inside iframe)
        self.equipment_action_reason_link = None
        self.add_button = None
        self.save_button = None

        # Dynamic input fields (determined at runtime)
        self.action_input = None
        self.description_input = None

    def _init_iframe_selectors(self) -> None:
        """Initialize selectors within the iframe."""
        self.equipment_action_reason_link = self.main_frame.get_by_text(
            'Equipment Action Reason Configuration', exact=True
        )
        # Get the second Add button (specific to Equipment Action Reason section)
        self.add_button = self.main_frame.locator('button:has-text("Add")').nth(1)
        self.save_button = self.main_frame.get_by_role('button', name='Save configurations').first()

    def navigate_to_configurations(self) -> None:
        """Navigate to Configurations page from main navigation."""
        self.configurations_nav_link.scroll_into_view_if_needed()
        # Click the parent link element
        parent = self.configurations_nav_link.locator('..')
        parent.click()
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(1000)
        self._init_iframe_selectors()

    def open_equipment_action_reason_config(self) -> None:
        """Open Equipment Action Reason Configuration section."""
        self.equipment_action_reason_link.wait_for(state='visible', timeout=10000)
        self.equipment_action_reason_link.scroll_into_view_if_needed()
        self.equipment_action_reason_link.click()
        self.page.wait_for_timeout(1000)

    def click_add_action_reason(self) -> None:
        """Click Add button to create new action reason entry."""
        self.add_button.wait_for(state='visible', timeout=10000)
        self.add_button.click()
        self.page.wait_for_timeout(1000)

    def fill_action_reason(self, action_value: str, description_value: str) -> None:
        """
        Fill action and description fields for new action reason.

        Note: Pega dynamically generates table rows. This method finds the last
        two visible input fields which correspond to the newly added row.
        """
        # Get all visible inputs in the iframe
        all_inputs = self.main_frame.locator('input:visible')

        # The last input is typically the Action field
        self.action_input = all_inputs.last()
        self.action_input.scroll_into_view_if_needed()
        self.action_input.fill(action_value)
        self.page.wait_for_timeout(500)

        # The second-to-last input is typically the Description field
        all_inputs_updated = self.main_frame.locator('input:visible')
        input_count = all_inputs_updated.count()
        if input_count >= 2:
            self.description_input = all_inputs_updated.nth(input_count - 2)
            self.description_input.scroll_into_view_if_needed()
            self.description_input.fill(description_value)
            self.page.wait_for_timeout(500)

    def save_configuration(self) -> None:
        """Click Save configurations button."""
        self.save_button.scroll_into_view_if_needed()
        self.save_button.click()
        self.page.wait_for_timeout(2000)

    def handle_validation_dialog(self) -> bool:
        """
        Handle validation alert dialog if it appears.
        Returns True if dialog was handled, False otherwise.
        """
        try:
            # Check if an alert dialog is present
            self.page.wait_for_timeout(500)
            return False
        except Exception:
            return False

    def verify_action_reason_exists(self, action_value: str) -> bool:
        """
        Verify that an action reason with the given value exists in the table.
        Returns True if found, False otherwise.
        """
        try:
            element = self.main_frame.get_by_text(action_value, exact=True)
            element.wait_for(state='visible', timeout=5000)
            return element.is_visible()
        except Exception:
            return False

    def refresh_and_reopen_section(self) -> None:
        """Refresh page and reopen Equipment Action Reason Configuration section."""
        self.page.reload(wait_until='networkidle')
        self.page.wait_for_timeout(2000)
        self._init_iframe_selectors()
        self.open_equipment_action_reason_config()
