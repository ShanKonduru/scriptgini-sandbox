import os
from playwright.sync_api import Page, FrameLocator


class DSPLoginPage:
    """Page Object for DSP Login via Microsoft SSO."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Selectors for Pega SSO selection page
        self.sso_despachoprevio_button = page.locator('button:has(a[href*="despachoprevio"])')

        # Selectors for Microsoft SSO login page
        self.username_input = page.locator('input[type="email"]')
        self.next_button = page.get_by_role('button', name='Next')
        self.password_input = page.locator('input[type="password"]')
        self.signin_button = page.get_by_role('button', name='Sign in')

        # Cookie consent dialog
        self.cookie_accept_button = page.get_by_test_id(':privacy-dialog:accept')

    def navigate(self, base_url: str) -> None:
        """Navigate to the DSP authentication page."""
        self.page.goto(base_url, wait_until='networkidle')

    def click_despachoprevio_sso(self) -> None:
        """Click on Despachoprevio SSO login button."""
        self.sso_despachoprevio_button.click()
        self.page.wait_for_load_state('networkidle')

    def enter_username(self, username: str) -> None:
        """Enter username in Microsoft SSO login."""
        self.username_input.wait_for(state='visible', timeout=10000)
        self.username_input.fill(username)

    def click_next(self) -> None:
        """Click Next button after username entry."""
        self.next_button.click()
        self.page.wait_for_load_state('networkidle')

    def enter_password(self, password: str) -> None:
        """Enter password in Microsoft SSO login."""
        self.password_input.wait_for(state='visible', timeout=10000)
        self.password_input.fill(password)

    def click_signin(self) -> None:
        """Click Sign in button to authenticate."""
        self.signin_button.click()
        self.page.wait_for_load_state('networkidle')

    def accept_cookies(self) -> None:
        """Accept cookie consent if present."""
        try:
            self.cookie_accept_button.wait_for(state='visible', timeout=5000)
            self.cookie_accept_button.click()
            self.page.wait_for_timeout(1000)
        except Exception:
            pass

    def login(self, base_url: str, username: str, password: str) -> None:
        """Complete login flow from start to authenticated state."""
        self.navigate(base_url)
        self.click_despachoprevio_sso()
        self.enter_username(username)
        self.click_next()
        self.enter_password(password)
        self.click_signin()
        self.accept_cookies()
        self.page.wait_for_load_state('networkidle')
