import pytest
from playwright.sync_api import Page, expect

def test_tc_001_add_a_new_todo_item(page: Page):
    """
    Title: TC-001 Add a new todo item
    Business Intent: TC-001 Add a new todo item
    Preconditions:
    """
    # Test Data
    BASE_URL = "https://demo.playwright.dev/todomvc"
    TODO_ITEM_TEXT = "Buy groceries"

    # --- Arrange ---
    # No specific arrange steps beyond navigation for this test.

    # --- Act ---
    # Step 1: Navigate to the TodoMVC app
    page.goto(BASE_URL)

    # Step 2: Type "Buy groceries" into the new todo input field
    page.get_by_placeholder("What needs to be done?").fill(TODO_ITEM_TEXT)

    # Step 3: Press Enter to submit the todo
    page.get_by_placeholder("What needs to be done?").press("Enter")

    # --- Assert ---
    # Assert: The item "Buy groceries" appears in the todo list
    expect(page.get_by_text(TODO_ITEM_TEXT)).to_be_visible()

    # Assert: The todo count shows 1 item left
    expect(page.locator(".todo-count")).to_have_text("1 item left")