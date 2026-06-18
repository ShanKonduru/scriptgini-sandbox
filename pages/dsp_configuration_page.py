from playwright.sync_api import Page, FrameLocator


class DSPConfigurationPage:
    """Page Object for DSP Pega Configuration page - Equipment Action Reason Configuration."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self._main_frame: FrameLocator | None = None

    def _get_main_frame(self) -> FrameLocator:
        """
        Get the main Pega iframe. Pega applications run inside iframes.
        Tries common iframe patterns used by Pega.
        """
        if self._main_frame is None:
            # Try common Pega iframe selectors
            try:
                self._main_frame = self.page.frame_locator("iframe[name='PegaGadget0Ifr']")
            except Exception:
                try:
                    self._main_frame = self.page.frame_locator("iframe[id*='Ifr']").first
                except Exception:
                    # Fallback to first iframe
                    self._main_frame = self.page.frame_locator("iframe").first
        return self._main_frame

    def click_configuration_icon(self) -> None:
        """Click on Configuration icon to open configuration page."""
        frame = self._get_main_frame()
        # Try multiple selector strategies for Configuration
        config_button = frame.locator(
            "button[data-test-id*='Configuration'], "
            "button[title*='Configuration'], "
            "a:has-text('Configuration')"
        ).first
        config_button.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def is_equipment_action_reason_section_visible(self) -> bool:
        """Verify Equipment Action Reason Configuration section is displayed."""
        frame = self._get_main_frame()
        section = frame.locator(
            "div:has-text('Equipment Action Reason Configuration'), "
            "section:has-text('Equipment Action Reason'), "
            "[id*='EquipmentActionReason']"
        ).first
        return section.is_visible(timeout=10000)

    def click_add_button_in_equipment_section(self) -> None:
        """Click Add button within Equipment Action Reason Configuration section."""
        frame = self._get_main_frame()
        # Locate the section first, then find Add button within it
        section = frame.locator(
            "div:has-text('Equipment Action Reason Configuration'), "
            "section:has-text('Equipment Action Reason')"
        ).first
        add_button = section.locator("button:has-text('Add'), button[title='Add']").first
        add_button.click()
        self.page.wait_for_timeout(500)

    def select_action_dropdown(self, action_value: str) -> None:
        """
        Select an option from the Action column dropdown.

        Args:
            action_value: The action to select (e.g., 'Cancelled')
        """
        frame = self._get_main_frame()
        # Find the last row (newly added) and locate Action dropdown
        action_dropdown = frame.locator(
            "select[name*='Action'], "
            "select[id*='Action'], "
            "select[class*='Action']"
        ).last
        action_dropdown.select_option(label=action_value)
        self.page.wait_for_timeout(300)

    def enter_reason_text(self, reason: str) -> None:
        """
        Enter text in the Reason column input field.

        Args:
            reason: The reason text to enter (e.g., 'Duplicate Waybill')
        """
        frame = self._get_main_frame()
        # Find the last row (newly added) and locate Reason input
        reason_input = frame.locator(
            "input[name*='Reason'], "
            "input[id*='Reason'], "
            "input[class*='Reason']"
        ).last
        reason_input.fill(reason)

    def click_inactive_tab(self) -> None:
        """Click on Inactive tab without saving."""
        frame = self._get_main_frame()
        inactive_tab = frame.locator(
            "a:has-text('Inactive'), "
            "button:has-text('Inactive'), "
            "div[role='tab']:has-text('Inactive'), "
            "[data-test-id*='Inactive']"
        ).first
        inactive_tab.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)

    def click_active_tab(self) -> None:
        """Click on Active tab."""
        frame = self._get_main_frame()
        active_tab = frame.locator(
            "a:has-text('Active'), "
            "button:has-text('Active'), "
            "div[role='tab']:has-text('Active'), "
            "[data-test-id*='Active']"
        ).first
        active_tab.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)

    def verify_action_reason_entry_exists(self, action: str, reason: str) -> bool:
        """
        Verify that the action-reason entry exists in the table.

        Args:
            action: The action value to verify (e.g., 'Cancelled')
            reason: The reason value to verify (e.g., 'Duplicate Waybill')

        Returns:
            True if the entry is found, False otherwise
        """
        frame = self._get_main_frame()
        # Look for a table row containing both action and reason
        row_with_both = frame.locator(
            f"tr:has(td:has-text('{action}')):has(td:has-text('{reason}'))"
        ).first
        try:
            return row_with_both.is_visible(timeout=5000)
        except Exception:
            return False

    def get_action_reason_entry_text(self, action: str) -> str:
        """
        Get the reason text for a given action from the table.

        Args:
            action: The action value (e.g., 'Cancelled')

        Returns:
            The reason text found in the table
        """
        frame = self._get_main_frame()
        row = frame.locator(f"tr:has(td:has-text('{action}'))").first
        reason_cell = row.locator("td").nth(1)
        return reason_cell.inner_text()
