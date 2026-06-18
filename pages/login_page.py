from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.despachoprevio_button = page.get_by_role("button", name="Login with despachoprevio")
        self.username_field = page.get_by_role("textbox", name="Enter your email, phone, or")
        self.next_button = page.get_by_role("button", name="Next")
        self.password_field = page.get_by_role("textbox", name="Enter the password for")
        self.signin_button = page.get_by_role("button", name="Sign in")
        self.cookie_accept_button = page.get_by_test_id(":privacy-dialog:accept")

    def navigate(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def click_despachoprevio_sso(self) -> None:
        self.despachoprevio_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_username(self, username: str) -> None:
        self.username_field.fill(username)

    def click_next(self) -> None:
        self.next_button.click()
        self.page.wait_for_load_state("networkidle")

    def enter_password(self, password: str) -> None:
        self.password_field.fill(password)

    def click_signin(self) -> None:
        self.signin_button.click()
        self.page.wait_for_load_state("networkidle")

    def accept_cookies(self) -> None:
        self.cookie_accept_button.click()
        self.page.wait_for_load_state("networkidle")
