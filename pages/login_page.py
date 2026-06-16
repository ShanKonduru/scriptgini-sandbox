import os
from playwright.sync_api import Page


class LoginPage:
    """
    Page Object for Pega SSO Login flow via Microsoft authentication.
    Handles navigation from Pega login page through Microsoft SSO and back to application.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        # Pega login page locators
        self.despachoprevio_button = page.get_by_role("link", name="Login with despachoprevio")

        # Microsoft SSO locators
        self.email_input = page.get_by_role("textbox", name="Enter your email, phone, or")
        self.next_button = page.get_by_role("button", name="Next")
        self.password_input = page.get_by_role("textbox", name="Enter the password for")
        self.signin_button = page.get_by_role("button", name="Sign in")

        # Cookies dialog locators
        self.accept_cookies_button = page.get_by_test_id(":privacy-dialog:accept")

    def navigate(self, base_url: str) -> None:
        """Navigate to the Pega authentication page."""
        self.page.goto(base_url, wait_until="networkidle")

    def click_login_with_despachoprevio(self) -> None:
        """Click the 'Login with despachoprevio' SSO button."""
        self.despachoprevio_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_email(self, email: str) -> None:
        """Enter email address in Microsoft SSO login form."""
        self.email_input.fill(email)

    def click_next(self) -> None:
        """Click the Next button after entering email."""
        self.next_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_password(self, password: str) -> None:
        """Enter password in Microsoft SSO login form."""
        self.password_input.fill(password)

    def click_sign_in(self) -> None:
        """Click the Sign in button to complete authentication."""
        self.signin_button.click()
        self.page.wait_for_load_state("networkidle")

    def accept_cookies(self) -> None:
        """Accept cookies dialog if it appears."""
        if self.accept_cookies_button.is_visible(timeout=5000):
            self.accept_cookies_button.click()
            self.page.wait_for_load_state("networkidle")

    def login(self, base_url: str, email: str, password: str) -> None:
        """
        Complete full login flow from Pega login page to authenticated application state.

        Args:
            base_url: Pega authentication URL
            email: User email address
            password: User password
        """
        self.navigate(base_url)
        self.click_login_with_despachoprevio()
        self.enter_email(email)
        self.click_next()
        self.enter_password(password)
        self.click_sign_in()
        self.accept_cookies()
