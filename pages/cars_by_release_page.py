from playwright.sync_api import Page, expect, FrameLocator


class CarsByReleasePage:
    """Page Object for Cars By Release Status page"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.cars_by_release_link = page.locator('a:has-text("Cars By Release Status")')

    def navigate_to_cars_by_release(self) -> None:
        """Navigate to Cars By Release Status page from main menu"""
        expect(self.cars_by_release_link).to_be_visible(timeout=10000)
        self.cars_by_release_link.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def get_cars_frame(self) -> FrameLocator:
        """Get the Pega iframe containing cars content"""
        return self.page.frame_locator('iframe[name^="PegaGadget"]')

    def select_status(self, status: str) -> None:
        """Select release status filter (TO BE RELEASED, ON ORIGIN HOLD, etc.)"""
        frame = self.get_cars_frame()
        status_button = frame.get_by_text(status, exact=True).first
        expect(status_button).to_be_visible(timeout=10000)
        status_button.click()
        self.page.wait_for_timeout(2000)

    def select_equipment_checkbox(self, index: int = 1) -> None:
        """Select equipment by checkbox index (1-based, skips Select All checkbox)"""
        frame = self.get_cars_frame()
        checkboxes = frame.locator('input[type="checkbox"]')
        checkbox = checkboxes.nth(index)
        expect(checkbox).to_be_visible(timeout=10000)
        checkbox.check()

    def verify_equipment_checkbox_checked(self, index: int = 1) -> None:
        """Verify equipment checkbox is checked"""
        frame = self.get_cars_frame()
        checkboxes = frame.locator('input[type="checkbox"]')
        checkbox = checkboxes.nth(index)
        expect(checkbox).to_be_checked()

    def click_actions_button(self) -> None:
        """Click Actions button to open actions menu"""
        frame = self.get_cars_frame()
        actions_button = frame.get_by_text("Actions", exact=True).first
        expect(actions_button).to_be_visible(timeout=10000)
        actions_button.click()
        self.page.wait_for_timeout(1000)

    def select_no_despacho_previo_action(self) -> None:
        """Select 'No Despacho Previo' from the actions dropdown"""
        frame = self.get_cars_frame()
        no_despacho_option = frame.get_by_text("No Despacho Previo", exact=True).first
        expect(no_despacho_option).to_be_visible(timeout=10000)
        no_despacho_option.click()
        self.page.wait_for_timeout(2000)

    def select_action_reason(self, reason: str) -> None:
        """Select reason from the No Despacho Previo Action Reason dropdown"""
        frame = self.get_cars_frame()
        reason_dropdown = frame.locator('select[name="$PpyDisplayHarness$ppyUsage"]').first
        expect(reason_dropdown).to_be_visible(timeout=10000)
        reason_dropdown.select_option(label=reason)
        self.page.wait_for_timeout(1000)

    def click_submit(self) -> None:
        """Click Submit button in the action dialog"""
        frame = self.get_cars_frame()
        submit_button = frame.get_by_text("Submit", exact=True).first
        expect(submit_button).to_be_visible(timeout=10000)
        submit_button.click()
        self.page.wait_for_timeout(2000)

    def verify_action_dialog_visible(self) -> None:
        """Verify No Despacho Previo action dialog is visible"""
        frame = self.get_cars_frame()
        reason_dropdown = frame.locator('select[name="$PpyDisplayHarness$ppyUsage"]').first
        expect(reason_dropdown).to_be_visible(timeout=10000)

    def get_available_action_reasons(self) -> list:
        """Get list of available action reasons from dropdown"""
        frame = self.get_cars_frame()
        reason_dropdown = frame.locator('select[name="$PpyDisplayHarness$ppyUsage"]').first
        options = reason_dropdown.locator('option').all_inner_texts()
        return [opt.strip() for opt in options if opt.strip() and opt.strip() != "Select"]
