"""
DSP Home Page Object
Handles navigation and interactions on the DSP Home page
"""
from playwright.sync_api import Page, expect


class HomePage:
    """Page object for DSP Home page with left navigation menu"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators for left navigation menu items
        self.car_by_release_menu = page.locator(
            "nav a:has-text('Car By Release'), "
            "a[href*='car'], "
            "a:has-text('Car History'), "
            "[role='navigation'] >> text='Car By Release'"
        ).first
        self.configuration_menu = page.locator(
            "nav a:has-text('Configuration'), "
            "a[href*='configuration'], "
            "[role='navigation'] >> text='Configuration'"
        ).first
        self.dsp_reports_menu = page.locator(
            "nav a:has-text('DSP Reports'), "
            "a[href*='reports'], "
            "[role='navigation'] >> text='DSP Reports'"
        ).first

    def verify_home_page_loaded(self) -> None:
        """Verify DSP Home page is displayed with main menu items"""
        expect(self.configuration_menu).to_be_visible(timeout=15000)
        expect(self.car_by_release_menu).to_be_visible(timeout=10000)

    def navigate_to_configuration(self) -> None:
        """Navigate to Configuration page from left navigation menu"""
        self.configuration_menu.click()
        self.page.wait_for_load_state("networkidle")

    def navigate_to_cars_by_release(self) -> None:
        """Navigate to Cars By Release page from left navigation menu"""
        self.car_by_release_menu.click()
        self.page.wait_for_load_state("networkidle")
