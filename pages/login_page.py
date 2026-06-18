from playwright.sync_api import Page


class LoginPage:
    """Page object for the Pega login page and Microsoft SSO authentication."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.despachoprevio_button = page.get_by_role("button", name="Login with despachoprevio")
        self.username_input = page.get_by_role("textbox", name="Enter your email, phone, or")
        self.next_button = page.get_by_role("button", name="Next")
        self.password_input = page.get_by_role("textbox", name="Enter the password for")
        self.signin_button = page.get_by_role("button", name="Sign in")
        self.accept_cookies_button = page.get_by_test_id(":privacy-dialog:accept")

    def navigate(self, base_url: str) -> None:
        """Navigate to the Pega authentication page."""
        self.page.goto(base_url, wait_until="networkidle")

    def click_login_with_despachoprevio(self) -> None:
        """Click the 'Login with Despachoprevio' button to initiate SSO."""
        self.despachoprevio_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_username(self, username: str) -> None:
        """Enter username in the Microsoft login form."""
        self.username_input.fill(username)

    def click_next(self) -> None:
        """Click the Next button on Microsoft login page."""
        self.next_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_password(self, password: str) -> None:
        """Enter password in the Microsoft login form."""
        self.password_input.fill(password)

    def click_sign_in(self) -> None:
        """Click the Sign In button to complete authentication."""
        self.signin_button.click()
        self.page.wait_for_load_state("networkidle")

    def accept_cookies(self) -> None:
        """Accept cookies if the popup appears."""
        try:
            self.accept_cookies_button.wait_for(state="visible", timeout=5000)
            self.accept_cookies_button.click()
            self.page.wait_for_load_state("networkidle")
        except Exception:
            pass
