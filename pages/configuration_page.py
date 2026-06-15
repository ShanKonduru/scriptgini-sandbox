"""
ConfigurationPage - Handles Equipment Action Reason Configuration section
"""
from playwright.sync_api import Page, Locator


class ConfigurationPage:
    """Page Object for Equipment Action Reason Configuration in Pega application"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Pega uses iframes extensively - main content is often in PegaGadget0Ifr or similar
        self.main_frame = None

        # Configuration menu locators (will be resolved in iframe context)
        self.configuration_icon = None
        self.equipment_action_reason_section = None
        self.add_button = None
        self.delete_icons = None
        self.save_configuration_button = None

    def _get_main_frame(self):
        """Get the main Pega content frame (PegaGadgetXIfr)"""
        if self.main_frame is None:
            # Pega typically uses frames like PegaGadget0Ifr, PegaGadget1Ifr, etc.
            # Try to locate the main content frame
            try:
                self.main_frame = self.page.frame_locator("iframe[name^='PegaGadget']").first
            except Exception:
                # Fallback to main page if no iframe
                self.main_frame = self.page
        return self.main_frame

    def click_configuration_icon(self) -> None:
        """Click on Configuration icon from the left menu"""
        # Pega left menu is typically in the main page context
        # Configuration icon might be in a navigation sidebar
        config_icon = self.page.locator(
            "button[title*='Configuration' i], "
            "a[title*='Configuration' i], "
            "[data-test-id*='configuration' i], "
            "button:has-text('Configuration'), "
            "a:has-text('Configuration')"
        ).first
        config_icon.click()
        self.page.wait_for_load_state("networkidle")
        # Allow Pega to load the configuration panel
        self.page.wait_for_timeout(1000)

    def navigate_to_equipment_action_reason_config(self) -> None:
        """Navigate to Equipment Action Reason Configuration section"""
        frame = self._get_main_frame()

        # Look for the Equipment Action Reason Configuration link/section
        equipment_section = frame.locator(
            "a:has-text('Equipment Action Reason Configuration'), "
            "button:has-text('Equipment Action Reason Configuration'), "
            "[data-test-id*='equipment-action-reason' i], "
            "text=/Equipment Action Reason Configuration/i"
        ).first
        equipment_section.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def get_add_button(self) -> Locator:
        """Get the Add button locator in Equipment Action Reason Configuration section"""
        frame = self._get_main_frame()

        # Look for Add button in the configuration section
        add_button = frame.locator(
            "button:has-text('Add'), "
            "button[title*='Add' i], "
            "[data-test-id*='add-button' i], "
            "button:has-text('+ Add'), "
            "button:has-text('Agregar')"
        ).first
        return add_button

    def get_delete_icons(self) -> Locator:
        """Get all delete icon locators in the configuration table"""
        frame = self._get_main_frame()

        # Look for delete icons/buttons in table rows
        delete_icons = frame.locator(
            "button[title*='Delete' i], "
            "button[aria-label*='Delete' i], "
            "[data-test-id*='delete' i], "
            "button:has-text('Delete'), "
            "button:has-text('Eliminar'), "
            "svg[data-icon='trash'], "
            "i.fa-trash, "
            ".delete-icon"
        )
        return delete_icons

    def get_save_configuration_button(self) -> Locator:
        """Get the Save Configuration button locator"""
        frame = self._get_main_frame()

        # Look for Save button
        save_button = frame.locator(
            "button:has-text('Save Configuration'), "
            "button:has-text('Save'), "
            "button[title*='Save Configuration' i], "
            "[data-test-id*='save-configuration' i], "
            "button:has-text('Guardar Configuración')"
        ).first
        return save_button

    def verify_add_button_present(self) -> bool:
        """Verify Add button is visible"""
        add_button = self.get_add_button()
        try:
            add_button.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def verify_delete_icons_present(self) -> bool:
        """Verify at least one delete icon is visible next to configuration items"""
        delete_icons = self.get_delete_icons()
        try:
            delete_icons.first.wait_for(state="visible", timeout=10000)
            return delete_icons.count() > 0
        except Exception:
            return False

    def verify_save_configuration_button_present(self) -> bool:
        """Verify Save Configuration button is visible"""
        save_button = self.get_save_configuration_button()
        try:
            save_button.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False
