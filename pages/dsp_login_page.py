"""
DSP Login Page Object
Handles authentication for the DSP Pega application.
"""
from playwright.sync_api import Page


class DSPLoginPage:
    """Page object for DSP login interactions."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators defined as instance attributes
        self.username_input = page.get_by_role("textbox", name="User name")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Log in")

    def navigate(self, url: str) -> None:
        """Navigate to the DSP login page."""
        self.page.goto(url, wait_until="networkidle")

    def enter_username(self, username: str) -> None:
        """Fill the username field."""
        self.username_input.fill(username)

    def enter_password(self, password: str) -> None:
        """Fill the password field."""
        self.password_input.fill(password)

    def click_login(self) -> None:
        """Click the login button."""
        self.login_button.click()

    def login(self, username: str, password: str) -> None:
        """Complete login flow: fill credentials and submit."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
