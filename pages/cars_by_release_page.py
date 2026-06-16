from playwright.sync_api import Page, FrameLocator, expect


class CarsByReleasePage:
    """
    Page Object for Cars By Release Status page in Despacho Previo application.

    NOTE: This page uses Pega Constellation framework with iframe-based content.
    All interactive elements are inside an iframe that must be accessed via frame_locator().
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        # Get the main content iframe
        self.iframe: FrameLocator = page.frame_locator("iframe").first

        # Filter section locators (inside iframe)
        # NOTE: Pega uses dynamic IDs - these selectors may need adjustment based on actual DOM
        self.status_dropdown = self.iframe.locator(
            "select[id*='Status'], select[name*='Status'], select[id*='status'], "
            "[role='combobox'][aria-label*='status' i], "
            "button[aria-label*='Status' i][aria-haspopup='listbox']"
        ).first

        self.waybill_date_from_input = self.iframe.locator(
            "input[type='date'], input[id*='Date'], input[id*='date'], "
            "input[name*='Date'], input[name*='date'], input[placeholder*='date' i]"
        ).first

        self.filter_button = self.iframe.locator(
            "button:has-text('Filter'), button:has-text('Search'), "
            "button[type='submit'], button[id*='filter' i], button[id*='search' i]"
        ).first

        # Equipment selection locators (inside iframe)
        self.equipment_checkbox_first = self.iframe.locator("input[type='checkbox']:not([disabled])").first

        # Actions button and menu (inside iframe)
        self.actions_button = self.iframe.locator(
            "button:has-text('Actions'), button[id*='Action' i], button[id*='action' i]"
        ).first

        self.no_despacho_previo_option = self.iframe.locator(
            "button:has-text('No Despacho previo'), a:has-text('No Despacho previo'), "
            "li:has-text('No Despacho previo'), [role='menuitem']:has-text('No Despacho previo')"
        ).first

        # Dropdown/dialog for action reasons (inside iframe)
        self.action_reason_dropdown = self.iframe.locator(
            "select, [role='combobox'], button[aria-haspopup='listbox'], "
            "[id*='reason' i], [id*='Reason' i]"
        ).first

        # Dropdown options (inside iframe)
        self.dropdown_options = self.iframe.locator("[role='option'], select option, li[role='option']")

    def wait_for_page_load(self) -> None:
        """Wait for the Cars By Release page to fully load."""
        # Wait for iframe to be attached and loaded
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)  # Give Pega Constellation time to render

    def select_status(self, status_text: str) -> None:
        """
        Select a status from the status dropdown.

        Args:
            status_text: Status to select (e.g., "To be released")
        """
        expect(self.status_dropdown).to_be_visible(timeout=10000)

        # Try select element first
        if self.status_dropdown.evaluate("el => el.tagName") == "SELECT":
            self.status_dropdown.select_option(label=status_text)
        else:
            # Handle custom dropdown (click to open, then select option)
            self.status_dropdown.click()
            self.iframe.locator(f"[role='option']:has-text('{status_text}'), li:has-text('{status_text}')").first.click()

        self.page.wait_for_timeout(500)

    def enter_waybill_date_from(self, date_string: str) -> None:
        """
        Enter date in waybill date from field.

        Args:
            date_string: Date in format YYYY-MM-DD (e.g., "2025-06-06")
        """
        expect(self.waybill_date_from_input).to_be_visible(timeout=10000)
        self.waybill_date_from_input.fill(date_string)
        self.page.wait_for_timeout(500)

    def click_filter_button(self) -> None:
        """Click the filter/search button to apply filters."""
        if self.filter_button.count() > 0:
            self.filter_button.click()
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(1000)

    def select_first_equipment(self) -> None:
        """Select the first equipment checkbox in the list."""
        expect(self.equipment_checkbox_first).to_be_visible(timeout=10000)
        self.equipment_checkbox_first.check()
        expect(self.equipment_checkbox_first).to_be_checked()

    def click_actions_button(self) -> None:
        """Click the Actions button to open the actions menu."""
        expect(self.actions_button).to_be_visible(timeout=10000)
        self.actions_button.click()
        self.page.wait_for_timeout(1000)  # Wait for menu to appear

    def select_no_despacho_previo(self) -> None:
        """Select 'No Despacho previo' option from the actions menu."""
        expect(self.no_despacho_previo_option).to_be_visible(timeout=10000)
        self.no_despacho_previo_option.click()
        self.page.wait_for_timeout(1000)  # Wait for dialog/popup

    def click_action_reason_dropdown(self) -> None:
        """Click the action reason dropdown to expand options."""
        expect(self.action_reason_dropdown).to_be_visible(timeout=10000)
        self.action_reason_dropdown.click()
        self.page.wait_for_timeout(500)

    def verify_dropdown_options(self, expected_options: list[str]) -> list[str]:
        """
        Verify that expected options are present in the dropdown.

        Args:
            expected_options: List of option text values to verify

        Returns:
            List of options that are actually present
        """
        # Wait for options to be visible
        expect(self.dropdown_options.first).to_be_visible(timeout=5000)

        # Get all option texts
        all_options = self.dropdown_options.all_text_contents()

        found_options = []
        for expected in expected_options:
            for actual in all_options:
                if expected.lower() in actual.lower():
                    found_options.append(expected)
                    break

        return found_options

    def is_option_present(self, option_text: str) -> bool:
        """
        Check if a specific option is present in the dropdown.

        Args:
            option_text: Text of the option to check

        Returns:
            True if option is present, False otherwise
        """
        option_locator = self.dropdown_options.filter(has_text=option_text)
        return option_locator.count() > 0
