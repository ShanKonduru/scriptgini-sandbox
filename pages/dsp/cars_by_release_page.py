"""
DSP Cars By Release Page Object
Handles interactions on the Cars By Release page including filtering, equipment selection, and actions
"""
from playwright.sync_api import Page, expect


class CarsByReleasePage:
    """Page object for DSP Cars By Release page"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators
        self.status_filter = page.locator(
            "select[name*='status' i], "
            "[data-testid*='status'], "
            "select[id*='status' i]"
        ).first
        self.equipment_table = page.locator("table, [role='table'], [class*='table']").first
        self.actions_button = page.get_by_role("button", name="Actions").or_(
            page.locator("button:has-text('Actions'), button[id*='action' i]")
        ).first
        self.export_to_excel_button = page.get_by_role("button", name="Export to Excel").or_(
            page.locator("button:has-text('Export'), button:has-text('Excel')")
        ).first

    def verify_cars_by_release_page_loaded(self) -> None:
        """Verify Cars By Release page is displayed with key elements"""
        expect(self.status_filter).to_be_visible(timeout=10000)
        expect(self.equipment_table).to_be_visible(timeout=10000)
        expect(self.actions_button).to_be_visible(timeout=10000)

    def select_status_to_be_released(self) -> None:
        """Select 'to be released' status from the status filter options"""
        self.status_filter.select_option(label="to be released")
        self.page.wait_for_load_state("networkidle")

    def select_equipment_by_checkbox(self) -> None:
        """
        Select an equipment by clicking the checkbox next to it
        (selects the first available equipment checkbox)
        """
        # Find checkboxes within the equipment table
        equipment_checkbox = self.equipment_table.locator(
            "input[type='checkbox']:not([disabled])"
        ).first
        expect(equipment_checkbox).to_be_visible(timeout=10000)
        equipment_checkbox.check()
        expect(equipment_checkbox).to_be_checked()

    def click_actions_button(self) -> None:
        """Click on 'Actions' button to open actions dropdown"""
        self.actions_button.click()
        self.page.wait_for_timeout(500)  # Allow dropdown to render

    def select_no_despacho_previo_action(self) -> None:
        """Select 'No Despacho Previo' option from the actions dropdown"""
        no_despacho_option = self.page.locator(
            "text='No Despacho Previo', "
            "[role='menuitem']:has-text('No Despacho Previo'), "
            "li:has-text('No Despacho Previo'), "
            "a:has-text('No Despacho Previo')"
        ).first
        expect(no_despacho_option).to_be_visible(timeout=10000)
        no_despacho_option.click()

    def get_action_reason_dropdown(self):
        """
        Get the 'Select No Despacho Previo Action Reason' dropdown locator
        Returns a locator for the reason selection dropdown
        """
        reason_dropdown = self.page.locator(
            "select[name*='reason' i], "
            "[data-testid*='reason'], "
            "select[id*='reason' i], "
            "select:has-text('Cancelled waybill')"
        ).first
        return reason_dropdown

    def click_action_reason_dropdown(self) -> None:
        """Click on 'Select No Despacho Previo Action Reason' dropdown"""
        reason_dropdown = self.get_action_reason_dropdown()
        expect(reason_dropdown).to_be_visible(timeout=10000)
        reason_dropdown.click()

    def select_reason_cancelled_waybill(self) -> None:
        """
        Select 'Cancelled waybill' from the reason dropdown options
        Available options: Duplicate waybill, Released on other waybill, Cancelled waybill
        """
        reason_dropdown = self.get_action_reason_dropdown()
        expect(reason_dropdown).to_be_visible(timeout=10000)
        reason_dropdown.select_option(label="Cancelled waybill")

    def click_submit_button(self) -> None:
        """Click on 'Submit' button to complete the action"""
        submit_button = self.page.get_by_role("button", name="Submit").or_(
            self.page.locator("button:has-text('Submit'), button[type='submit']")
        ).first
        expect(submit_button).to_be_visible(timeout=10000)
        submit_button.click()
        self.page.wait_for_load_state("networkidle")

    def verify_action_completed(self) -> None:
        """Verify that the action is completed successfully and popup closes"""
        # Wait for popup/modal to close (absence of dialog role)
        self.page.wait_for_timeout(2000)
        # Verify no modal/dialog is visible
        modal_count = self.page.locator("[role='dialog'], .modal, [class*='popup']").count()
        assert modal_count == 0, "Action popup did not close after submission"
