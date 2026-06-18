from playwright.sync_api import Page, FrameLocator, expect


class ConfigurationsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._iframe = None

    @property
    def iframe(self) -> FrameLocator:
        if self._iframe is None:
            self._iframe = self.page.frame_locator("iframe[name*='PegaGadget']")
        return self._iframe

    def verify_equipment_action_reason_section(self) -> None:
        heading = self.iframe.locator("#headerlabel9802")
        expect(heading).to_have_text("Equipment Action Reason Configuration")

    def click_add_button(self) -> None:
        container = self.iframe.locator("div.content-item:has(#headerlabel9802)")
        add_button = container.locator("button.pzbutton").filter(has_text="Add").first()
        add_button.click()
        self.page.wait_for_timeout(1000)

    def select_action(self, action: str) -> None:
        container = self.iframe.locator("div.content-item:has(#headerlabel9802)")
        selects = container.locator("select[name*='pActionReason'][name*='pParentKey']")
        last_select = selects.last()
        last_select.select_option(action)
        self.page.wait_for_timeout(500)

    def enter_reason(self, reason: str) -> None:
        container = self.iframe.locator("div.content-item:has(#headerlabel9802)")
        inputs = container.locator("input[name*='pActionReason'][name*='pKey']")
        last_input = inputs.last()
        last_input.fill(reason)
        self.page.wait_for_timeout(500)

    def click_save_button(self) -> None:
        container = self.iframe.locator("div.content-item:has(#headerlabel9802)")
        save_button = container.locator("button.pzbutton").filter(has_text="Save").first()
        save_button.click()
        self.page.wait_for_timeout(2000)

    def verify_action_reason_persisted(self, action: str, reason: str) -> None:
        container = self.iframe.locator("div.content-item:has(#headerlabel9802)")
        selects = container.locator("select[name*='pActionReason'][name*='pParentKey']")
        inputs = container.locator("input[name*='pActionReason'][name*='pKey']")

        select_count = selects.count()
        found = False

        for i in range(select_count):
            select_value = selects.nth(i).input_value()
            input_value = inputs.nth(i).input_value()

            if select_value == action and input_value == reason:
                found = True
                break

        assert found, f"Action-Reason combination '{action} - {reason}' not found in the list"
