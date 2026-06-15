import os
from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object for Microsoft SSO login flow via Pega"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Pega login page locators
        self.login_with_despachoprevio_button = page.get_by_role("button", name="Login with despachoprevio")
        # Microsoft SSO locators
        self.email_input = page.get_by_role("textbox", name="Enter your email, phone, or")
        self.next_button = page.get_by_role("button", name="Next")
        self.password_input = page.get_by_role("textbox", name="Enter the password for")
        self.signin_button = page.get_by_role("button", name="Sign in")
        # Cookie consent dialog
        self.accept_cookies_button = page.get_by_test_id(":privacy-dialog:accept")

    def navigate(self, base_url: str) -> None:
        """Navigate to the Pega login page"""
        self.page.goto(base_url, wait_until="networkidle")

    def click_login_with_despachoprevio(self) -> None:
        """Click the 'Login with despachoprevio' button"""
        expect(self.login_with_despachoprevio_button).to_be_visible(timeout=10000)
        self.login_with_despachoprevio_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_email(self, email: str) -> None:
        """Enter email address in Microsoft SSO page"""
        expect(self.email_input).to_be_visible(timeout=10000)
        self.email_input.fill(email)

    def click_next(self) -> None:
        """Click Next button on email entry page"""
        expect(self.next_button).to_be_visible(timeout=5000)
        self.next_button.click()
        self.page.wait_for_timeout(2000)

    def enter_password(self, password: str) -> None:
        """Enter password in Microsoft SSO page"""
        expect(self.password_input).to_be_visible(timeout=10000)
        self.password_input.fill(password)

    def click_signin(self) -> None:
        """Click Sign in button"""
        expect(self.signin_button).to_be_visible(timeout=5000)
        self.signin_button.click()
        self.page.wait_for_load_state("networkidle")

    def accept_cookies_if_present(self) -> None:
        """Accept cookie consent dialog if it appears"""
        try:
            if self.accept_cookies_button.is_visible(timeout=5000):
                self.accept_cookies_button.click()
                self.page.wait_for_timeout(1000)
        except Exception:
            pass

    def login(self, base_url: str, email: str, password: str) -> None:
        """Complete login flow"""
        self.navigate(base_url)
        self.click_login_with_despachoprevio()
        self.enter_email(email)
        self.click_next()
        self.enter_password(password)
        self.click_signin()
        self.accept_cookies_if_present()
