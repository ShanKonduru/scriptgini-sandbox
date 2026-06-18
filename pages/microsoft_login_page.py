"""
Microsoft SSO Login Page Object
Handles authentication through Microsoft OAuth/SAML login flow
"""
from playwright.sync_api import Page


class MicrosoftLoginPage:
    """Page object for Microsoft Single Sign-On authentication"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Email/username input field
        self.email_input = page.get_by_role("textbox", name="Enter your email, phone, or Skype.")
        # Next button on email screen
        self.next_button = page.get_by_role("button", name="Next")
        # Password input field
        self.password_input = page.get_by_role("textbox", name="Enter the password for")
        # Sign in button on password screen
        self.signin_button = page.get_by_role("button", name="Sign in")
        # Stay signed in button (optional prompt)
        self.stay_signed_in_yes = page.get_by_role("button", name="Yes")
        self.stay_signed_in_no = page.get_by_role("button", name="No")

    def enter_email(self, email: str) -> None:
        """Fill in the email/username field"""
        self.email_input.fill(email)

    def click_next(self) -> None:
        """Click the Next button after entering email"""
        self.next_button.click()

    def enter_password(self, password: str) -> None:
        """Fill in the password field"""
        self.password_input.fill(password)

    def click_signin(self) -> None:
        """Click the Sign In button"""
        self.signin_button.click()

    def handle_stay_signed_in(self, stay_signed_in: bool = False) -> None:
        """
        Handle the 'Stay signed in?' prompt if it appears
        Args:
            stay_signed_in: True to stay signed in, False to not stay signed in
        """
        try:
            if stay_signed_in:
                self.stay_signed_in_yes.click(timeout=5000)
            else:
                self.stay_signed_in_no.click(timeout=5000)
        except Exception:
            pass

    def complete_login(self, email: str, password: str, stay_signed_in: bool = False) -> None:
        """
        Complete the full Microsoft SSO login flow
        Args:
            email: User email address
            password: User password
            stay_signed_in: Whether to stay signed in
        """
        self.enter_email(email)
        self.click_next()
        self.page.wait_for_load_state("networkidle")
        self.enter_password(password)
        self.click_signin()
        self.page.wait_for_load_state("networkidle")
        self.handle_stay_signed_in(stay_signed_in)
