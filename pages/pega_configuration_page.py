"""
Pega Configuration Page Object
Handles interactions with the Pega application configuration interface
"""
from playwright.sync_api import Page, FrameLocator, expect


class PegaConfigurationPage:
    """Page object for Pega configuration screens"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Pega applications typically run inside iframes
        # The main application content frame
        self.app_frame = self._get_app_frame()

    def _get_app_frame(self) -> FrameLocator:
        """
        Locate the main Pega application frame
        Pega apps typically use iframe with name 'PegaGadget0Ifr' or similar
        """
        # Try common Pega iframe patterns
        frame_selectors = [
            "iframe[name*='PegaGadget']",
            "iframe[name*='pega']",
            "iframe#PegaGadget0Ifr",
            "iframe.pega-iframe",
        ]
        for selector in frame_selectors:
            try:
                frame = self.page.frame_locator(selector).first
                return frame
            except Exception:
                continue
        # Fallback: return page as frame locator if no iframe found
        return self.page.locator("body").first

    def accept_cookies_if_present(self) -> None:
        """Click Accept button if cookie consent popup appears"""
        try:
            accept_button = self.page.get_by_role("button", name="Accept").or_(
                self.page.locator("button:has-text('Accept')")
            )
            if accept_button.is_visible(timeout=3000):
                accept_button.click()
                self.page.wait_for_timeout(1000)
        except Exception:
            pass

    def click_configuration_menu(self) -> None:
        """Click on Configuration icon/link from the left navigation menu"""
        # Try multiple selector strategies for Configuration menu
        config_selectors = [
            self.page.get_by_role("link", name="Configuration"),
            self.page.get_by_role("button", name="Configuration"),
            self.page.locator("a:has-text('Configuration')"),
            self.page.locator("button:has-text('Configuration')"),
            self.page.locator("[data-test-id*='configuration' i]"),
            self.page.locator("nav a:has-text('Configuration')"),
        ]

        for selector in config_selectors:
            try:
                if selector.first.is_visible(timeout=5000):
                    selector.first.click()
                    self.page.wait_for_load_state("networkidle")
                    return
            except Exception:
                continue

        raise Exception("Configuration menu item not found")

    def verify_equipment_action_reason_section_visible(self) -> None:
        """Verify Equipment Action Reason Configuration section is displayed"""
        section_heading = self.page.locator(
            "text=/Equipment Action Reason Configuration/i"
        ).or_(
            self.page.locator("[class*='equipment'][class*='action'][class*='reason' i]")
        )
        expect(section_heading.first).to_be_visible(timeout=10000)

    def click_add_button(self) -> None:
        """
        Click on Add button at the left bottom corner of
        Equipment Action Reason Configuration section
        """
        # Look for Add button within the Equipment Action Reason section
        add_button = self.page.get_by_role("button", name="Add").or_(
            self.page.locator("button:has-text('Add')").or_(
                self.page.locator("button:has-text('+')")
            )
        )
        expect(add_button.first).to_be_visible(timeout=10000)
        add_button.first.click()
        self.page.wait_for_timeout(1000)

    def select_action_dropdown(self, action_value: str) -> None:
        """
        Select an action from the Action dropdown
        Args:
            action_value: The action to select (e.g., 'Cancelled')
        """
        # Try standard select element first
        action_dropdown = self.page.get_by_role("combobox", name="Action").or_(
            self.page.locator("select[name*='action' i]").or_(
                self.page.locator("select[id*='action' i]")
            )
        )

        try:
            if action_dropdown.first.is_visible(timeout=5000):
                action_dropdown.first.select_option(label=action_value)
                return
        except Exception:
            pass

        # Try Pega custom dropdown (click to open, then select option)
        try:
            custom_dropdown = self.page.locator("[data-test-id*='action' i]").or_(
                self.page.locator("div[class*='dropdown']:has-text('Action')")
            )
            custom_dropdown.first.click()
            self.page.wait_for_timeout(500)
            option = self.page.locator(f"li:has-text('{action_value}')").or_(
                self.page.locator(f"div[role='option']:has-text('{action_value}')")
            )
            option.first.click()
        except Exception:
            raise Exception(f"Could not select action '{action_value}' from dropdown")

    def enter_reason_text(self, reason: str) -> None:
        """
        Enter text in the Reason text box
        Args:
            reason: The reason text to enter
        """
        reason_input = self.page.get_by_role("textbox", name="Reason").or_(
            self.page.locator("input[name*='reason' i]").or_(
                self.page.locator("input[id*='reason' i]").or_(
                    self.page.locator("textarea[name*='reason' i]")
                )
            )
        )
        expect(reason_input.first).to_be_visible(timeout=10000)
        reason_input.first.fill(reason)

    def click_save_configuration(self) -> None:
        """Click the Save Configuration button"""
        save_button = self.page.get_by_role("button", name="Save Configuration").or_(
            self.page.get_by_role("button", name="Save").or_(
                self.page.locator("button:has-text('Save Configuration')").or_(
                    self.page.locator("button:has-text('Save')")
                )
            )
        )
        expect(save_button.first).to_be_visible(timeout=10000)
        save_button.first.click()
        self.page.wait_for_load_state("networkidle")

    def verify_duplicate_validation_message(self) -> str:
        """
        Verify that a duplicate validation message appears
        Returns the validation message text
        """
        # Look for validation error messages
        error_selectors = [
            self.page.locator("[class*='error']").filter(has_text="duplicate"),
            self.page.locator("[class*='validation']").filter(has_text="duplicate"),
            self.page.locator("[role='alert']"),
            self.page.locator(".validation-message"),
            self.page.locator("text=/duplicate/i"),
            self.page.locator("text=/already exists/i"),
        ]

        for selector in error_selectors:
            try:
                if selector.first.is_visible(timeout=5000):
                    return selector.first.inner_text()
            except Exception:
                continue

        raise Exception("No duplicate validation message found")
