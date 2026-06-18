from playwright.sync_api import Page


class DSPLoginPage:
    """Page Object for DSP Pega application login via Microsoft SSO."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Pega login page locators
        self.login_with_despachoprevio_button = page.get_by_role("button", name="Login with despachoprevio")

        # Microsoft SSO locators
        self.username_input = page.get_by_role("textbox", name="Enter your email, phone, or")
        self.next_button = page.get_by_role("button", name="Next")
        self.password_input = page.get_by_role("textbox", name="Enter the password for")
        self.sign_in_button = page.get_by_role("button", name="Sign in")
        self.stay_signed_in_yes_button = page.get_by_role("button", name="Yes")
        self.stay_signed_in_no_button = page.get_by_role("button", name="No")

    def navigate(self, url: str) -> None:
        """Navigate to the DSP Pega login page."""
        self.page.goto(url, wait_until="networkidle")

    def click_login_with_despachoprevio(self) -> None:
        """Click the 'Login with despachoprevio' SSO button."""
        self.login_with_despachoprevio_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_username(self, username: str) -> None:
        """Enter username in Microsoft SSO login form."""
        self.username_input.fill(username)

    def click_next(self) -> None:
        """Click Next button after entering username."""
        self.next_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_password(self, password: str) -> None:
        """Enter password in Microsoft SSO login form."""
        self.password_input.fill(password)

    def click_sign_in(self) -> None:
        """Click Sign In button to complete authentication."""
        self.sign_in_button.click()
        self.page.wait_for_load_state("networkidle")

    def handle_stay_signed_in_popup(self, stay_signed_in: bool = True) -> None:
        """
        Handle the 'Stay signed in?' popup that may appear after login.

        Args:
            stay_signed_in: If True, click Yes button; otherwise click No button.
        """
        try:
            if stay_signed_in:
                self.stay_signed_in_yes_button.click(timeout=5000)
            else:
                self.stay_signed_in_no_button.click(timeout=5000)
            self.page.wait_for_load_state("networkidle")
        except Exception:
            pass
