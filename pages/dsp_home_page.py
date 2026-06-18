from playwright.sync_api import Page, expect


class DSPHomePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.configurations_link = page.get_by_role("link", name="Configurations")

    def navigate_to_configurations(self) -> None:
        self.configurations_link.click()
        self.page.wait_for_load_state("networkidle")

    def is_displayed(self) -> bool:
        expect(self.configurations_link).to_be_visible()
        return True
