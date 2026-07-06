import os
from playwright.sync_api import Page


class LoginPage:
    """Page Object for Pega SSO Login via Microsoft authentication."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Pega login page elements
        self.despachoprevio_button = self.page.get_by_role("button", name="Login with despachoprevio")

        # Microsoft SSO elements
        self.username_input = self.page.get_by_role("textbox", name="Enter your email, phone, or")
        self.next_button = self.page.get_by_role("button", name="Next")
        self.password_input = self.page.get_by_role("textbox", name="Enter the password for")
        self.signin_button = self.page.get_by_role("button", name="Sign in")

        # Cookies popup elements
        self.accept_cookies_button = self.page.get_by_test_id(":privacy-dialog:accept")

    def navigate(self, url: str) -> None:
        """Navigate to the base URL (from env: BASE_URL)."""
        self.page.goto(url)
        self.page.wait_for_url("**/PRAuth**")

    def click_despachoprevio_login(self) -> None:
        """Click on Login with Despachoprevio button to initiate SSO."""
        self.despachoprevio_button.click()
        self.page.wait_for_url("**/login.microsoftonline.com/**")

    def enter_username(self, username: str) -> None:
        """Enter username (from env: APP_USERNAME) in the SSO login field."""
        self.username_input.fill(username)

    def click_next(self) -> None:
        """Click Next button after entering username."""
        self.next_button.click()

    def enter_password(self, password: str) -> None:
        """Enter password (from env: APP_PASSWORD) in the SSO password field."""
        self.password_input.fill(password)

    def click_signin(self) -> None:
        """Click Sign in button to authenticate."""
        self.signin_button.click()
        self.page.wait_for_url("**/prweb/PRAuth/app/dsp-cont**")

    def accept_cookies_if_present(self) -> None:
        """Accept cookies popup if it appears."""
        if self.accept_cookies_button.is_visible(timeout=5000):
            self.accept_cookies_button.click()
