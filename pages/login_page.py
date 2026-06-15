"""
LoginPage - Handles authentication flow for Pega application with SSO
"""
from playwright.sync_api import Page


class LoginPage:
    """Page Object for Pega Login page with SSO authentication"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Pega login page locators
        self.despachoprevio_button = page.get_by_role("button", name="Login with despachoprevio")
        # Microsoft SSO locators
        self.email_input = page.get_by_placeholder("Email, phone, or Skype")
        self.next_button = page.get_by_role("button", name="Next")
        self.password_input = page.get_by_placeholder("Password")
        self.signin_button = page.get_by_role("button", name="Sign in")
        self.stay_signed_in_no = page.get_by_role("button", name="No")

    def navigate(self, url: str) -> None:
        """Navigate to the Pega login page"""
        self.page.goto(url, wait_until="networkidle")

    def click_despachoprevio_login(self) -> None:
        """Click the 'Login with Despachoprevio' SSO button"""
        self.despachoprevio_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_email(self, email: str) -> None:
        """Enter email in Microsoft SSO login form"""
        self.email_input.fill(email)

    def click_next(self) -> None:
        """Click Next button on Microsoft SSO page"""
        self.next_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_password(self, password: str) -> None:
        """Enter password in Microsoft SSO login form"""
        self.password_input.wait_for(state="visible", timeout=15000)
        self.password_input.fill(password)

    def click_signin(self) -> None:
        """Click Sign in button on Microsoft SSO page"""
        self.signin_button.click()
        self.page.wait_for_load_state("networkidle")

    def handle_stay_signed_in(self) -> None:
        """Handle 'Stay signed in?' prompt by clicking No"""
        try:
            self.stay_signed_in_no.wait_for(state="visible", timeout=5000)
            self.stay_signed_in_no.click()
            self.page.wait_for_load_state("networkidle")
        except Exception:
            # Prompt may not appear, continue
            pass
