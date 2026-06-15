"""
DSP Login Page Object
Handles authentication for DSP application with Super User credentials.
"""
import os
from playwright.sync_api import Page, expect


class DSPLoginPage:
    """Page Object for DSP login functionality."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators - defined once in constructor
        # Note: These are best-practice selectors. Actual DSP application may use
        # Pega-specific structure (iframes, dynamic IDs). Verify against live app.
        self.username_input = page.get_by_role("textbox", name="username").or_(
            page.locator("input[name='username'], input[id='username'], input[type='text']")
        ).first
        self.password_input = page.get_by_role("textbox", name="password").or_(
            page.locator("input[name='password'], input[id='password'], input[type='password']")
        ).first
        self.login_button = page.get_by_role("button", name="login").or_(
            page.get_by_role("button", name="sign in")
        ).or_(
            page.locator("button[type='submit'], input[type='submit'], button:has-text('Login')")
        ).first

    def navigate(self, base_url: str) -> None:
        """Navigate to DSP login page."""
        self.page.goto(f"{base_url}/login", wait_until="networkidle")

    def enter_username(self, username: str) -> None:
        """Fill username field."""
        expect(self.username_input).to_be_visible(timeout=10000)
        self.username_input.fill(username)

    def enter_password(self, password: str) -> None:
        """Fill password field."""
        expect(self.password_input).to_be_visible(timeout=10000)
        self.password_input.fill(password)

    def click_login(self) -> None:
        """Click the login button."""
        expect(self.login_button).to_be_visible(timeout=5000)
        self.login_button.click()

    def wait_for_login_success(self) -> None:
        """Wait for login to complete and redirect away from login page."""
        self.page.wait_for_load_state("networkidle")
        expect(self.page).to_have_url(lambda url: "login" not in url.lower(), timeout=15000)

    def login_as_super_user(self, base_url: str) -> None:
        """
        Complete login flow using Super User credentials from environment.
        Expects DSP_SUPER_USERNAME and DSP_SUPER_PASSWORD environment variables.
        """
        username = os.getenv("DSP_SUPER_USERNAME", "super_user")
        password = os.getenv("DSP_SUPER_PASSWORD", "super_password")

        self.navigate(base_url)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        self.wait_for_login_success()
