import os
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.dsp_home_page import DSPHomePage
from pages.configurations_page import ConfigurationsPage


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Fixture to handle login flow and return authenticated page."""
    base_url = os.environ.get("BASE_URL", "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth")
    username = os.environ["APP_USERNAME"]
    password = os.environ["APP_PASSWORD"]

    login_page = LoginPage(page)
    login_page.navigate(base_url)
    login_page.click_despachoprevio_sso()
    login_page.enter_username(username)
    login_page.click_next()
    login_page.enter_password(password)
    login_page.click_signin()
    login_page.accept_cookies()

    page.wait_for_url("**/dsp-cont**")
    return page


def test_add_equipment_action_reason_cancelled_duplicate_waybill(logged_in_page: Page):
    """
    Test Case: Add Equipment Action Reason - Cancelled with Duplicate Waybill

    Steps:
    1. Navigate to DSP Home page (via logged_in_page fixture)
    2. Verify DSP Home page is displayed
    3. Navigate to Configurations page
    4. Verify Equipment Action Reason Configuration section is displayed
    5. Click Add button to add new action reason
    6. Select 'Cancelled' from Action dropdown
    7. Enter 'Duplicate Waybill' in Reason field
    8. Click Save button
    9. Verify the newly added action-reason 'Cancelled - Duplicate Waybill' is persisted
    """
    page = logged_in_page

    dsp_home = DSPHomePage(page)
    dsp_home.is_displayed()

    dsp_home.navigate_to_configurations()

    config_page = ConfigurationsPage(page)
    config_page.verify_equipment_action_reason_section()

    config_page.click_add_button()

    config_page.select_action("Cancelled")

    config_page.enter_reason("Duplicate Waybill")

    config_page.click_save_button()

    config_page.verify_action_reason_persisted("Cancelled", "Duplicate Waybill")
