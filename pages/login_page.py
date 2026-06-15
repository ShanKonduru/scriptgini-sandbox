from playwright.sync_api import Page


class LoginPage:
    """Page Object for the Pega authentication and Microsoft SSO login flow."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Pega login page locators
        self.login_with_despachoprevio_button = page.get_by_role("button", name="Login with despachoprevio")
        # Microsoft SSO locators
        self.email_input = page.get_by_role("textbox", name="Enter your email, phone, or")
        self.next_button = page.get_by_role("button", name="Next")
        self.password_input = page.get_by_role("textbox", name="Enter the password for")
        self.signin_button = page.get_by_role("button", name="Sign in")
        # Cookie consent locators
        self.accept_cookies_button = page.get_by_test_id(":privacy-dialog:accept")

    def navigate(self, url: str) -> None:
        """Navigate to the login page."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def click_login_with_despachoprevio(self) -> None:
        """Click the 'Login with despachoprevio' button."""
        self.login_with_despachoprevio_button.click()
        self.page.wait_for_url("**/saml2")

    def enter_email(self, email: str) -> None:
        """Enter email in the Microsoft SSO email field."""
        self.email_input.fill(email)

    def click_next(self) -> None:
        """Click the Next button on Microsoft SSO email page."""
        self.next_button.click()
        self.page.wait_for_timeout(1000)

    def enter_password(self, password: str) -> None:
        """Enter password in the Microsoft SSO password field."""
        self.password_input.fill(password)

    def click_signin(self) -> None:
        """Click the Sign in button on Microsoft SSO password page."""
        self.signin_button.click()
        self.page.wait_for_load_state("networkidle")

    def accept_cookies_if_present(self) -> None:
        """Accept cookies if the consent dialog appears."""
        try:
            if self.accept_cookies_button.is_visible(timeout=5000):
                self.accept_cookies_button.click()
                self.page.wait_for_timeout(1000)
        except Exception:
            pass
