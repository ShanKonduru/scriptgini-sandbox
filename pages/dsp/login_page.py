"""
DSP Login Page Object
Handles Microsoft OAuth login flow for DSP application
"""
from playwright.sync_api import Page


class LoginPage:
    """Page object for DSP Microsoft OAuth login flow"""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators
        self.login_with_despachoprevio_button = page.get_by_role("button", name="Login with Despachoprevio")
        self.username_field = page.locator("input[type='email'], input[name='loginfmt'], input[placeholder*='email' i]")
        self.next_button = page.get_by_role("button", name="Next")
        self.password_field = page.locator("input[type='password'], input[name='passwd']")
        self.sign_in_button = page.get_by_role("button", name="Sign in")
        self.accept_cookies_button = page.get_by_role("button", name="Accept")

    def navigate(self, base_url: str) -> None:
        """Navigate to the DSP authentication page"""
        self.page.goto(base_url, wait_until="networkidle")

    def click_login_with_despachoprevio(self) -> None:
        """Click on 'Login with Despachoprevio' button"""
        self.login_with_despachoprevio_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_username(self, username: str) -> None:
        """Enter username/email in the username field"""
        self.username_field.fill(username)

    def click_next(self) -> None:
        """Click on 'Next' button"""
        self.next_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_password(self, password: str) -> None:
        """Enter password in the password field"""
        self.password_field.fill(password)

    def click_sign_in(self) -> None:
        """Click on 'Sign in' button"""
        self.sign_in_button.click()
        self.page.wait_for_load_state("networkidle")

    def handle_accept_cookies_if_present(self) -> None:
        """Handle 'Accept Cookies' popup if it appears"""
        try:
            if self.accept_cookies_button.is_visible(timeout=3000):
                self.accept_cookies_button.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass  # Popup not present, continue
