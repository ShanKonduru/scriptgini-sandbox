from datetime import datetime
import os
from pathlib import Path
import re
import threading

import pytest
from playwright.sync_api import Locator, Page


RESULTS_DIR = Path("test-results")

# Thread-local storage so the Locator patches know which test is active.
_test_state = threading.local()

# Locator action methods that represent real user interactions.
_INTERACTION_METHODS = [
    "click",
    "dblclick",
    "fill",
    "press",
    "type",
    "check",
    "uncheck",
    "select_option",
    "tap",
    "hover",
    "focus",
    "clear",
    "press_sequentially",
    "set_input_files",
    "drag_to",
    "dispatch_event",
]

_LOCATOR_CLASS_PATCHED = False


def _patch_locator_class() -> None:
    """
    Monkey-patch Playwright Locator action methods once at module load so that
    every interaction:
      1. Highlights the target element with a dark-green rectangle.
      2. Takes a 'before' screenshot showing the highlighted element.
      3. Executes the real action.
      4. Takes an 'after' screenshot showing the resulting page state.
    """
    global _LOCATOR_CLASS_PATCHED
    if _LOCATOR_CLASS_PATCHED:
        return
    _LOCATOR_CLASS_PATCHED = True

    def make_wrapper(orig, mname):
        def wrapper(self, *args, **kwargs):
            state = getattr(_test_state, "current", None)

            if state:
                # --- Highlight the element with a dark-green rectangle ---
                try:
                    self.evaluate(
                        """el => {
                            el.style.setProperty('outline', '4px solid darkgreen', 'important');
                            el.style.setProperty('outline-offset', '2px', 'important');
                            el.style.setProperty('box-shadow', '0 0 0 3px rgba(0, 100, 0, 0.35)', 'important');
                        }"""
                    )
                    # Give the browser a short moment to paint the highlight
                    # before the screenshot is captured.
                    state["page"].wait_for_timeout(120)
                except Exception:
                    pass  # Element may not be in DOM yet; proceed anyway.

                # --- Screenshot BEFORE the action (highlight is visible) ---
                try:
                    state["counter"]["value"] += 1
                    ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
                    spath = (
                        state["dir"]
                        / f"step-{state['counter']['value']:03d}-{mname}-before-{ts}.png"
                    )
                    state["page"].screenshot(path=str(spath), full_page=True)
                except Exception:
                    pass

            # --- Execute the real Playwright action ---
            result = orig(self, *args, **kwargs)

            if state:
                # --- Screenshot AFTER the action (result / new page state) ---
                try:
                    state["counter"]["value"] += 1
                    ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
                    spath = (
                        state["dir"]
                        / f"step-{state['counter']['value']:03d}-{mname}-after-{ts}.png"
                    )
                    state["page"].screenshot(path=str(spath), full_page=True)
                except Exception:
                    pass

            return result

        return wrapper

    for method_name in _INTERACTION_METHODS:
        if not hasattr(Locator, method_name):
            continue
        original = getattr(Locator, method_name)
        setattr(Locator, method_name, make_wrapper(original, method_name))


# Patch once when conftest is first imported.
_patch_locator_class()


def _safe_name(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return safe or "test"


def _normalize_run_mode(value: str) -> str:
    mode = (value or "").strip().lower()
    if mode in {"max", "maximize", "maximized"}:
        return "maximized"
    if mode in {"head", "headed"}:
        return "headed"
    if mode in {"headless", "nohead"}:
        return "headless"
    return "maximized"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-mode",
        action="store",
        default=os.getenv("PW_RUN_MODE", "maximized"),
        help="UI run mode: headless, headed, maximized",
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig: pytest.Config):
    run_mode = _normalize_run_mode(pytestconfig.getoption("run_mode"))
    merged_args = list(browser_type_launch_args.get("args", []))

    launch_headless = run_mode == "headless"
    if run_mode == "maximized" and "--start-maximized" not in merged_args:
        merged_args.append("--start-maximized")
    if run_mode == "maximized" and not any(arg.startswith("--window-size=") for arg in merged_args):
        # Fallback for environments where start-maximized is ignored.
        merged_args.append("--window-size=1920,1080")

    return {
        **browser_type_launch_args,
        "headless": launch_headless,
        "args": merged_args,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig: pytest.Config):
    run_mode = _normalize_run_mode(pytestconfig.getoption("run_mode"))
    if run_mode == "maximized":
        # Remove fixed viewport so page uses the real maximized window size.
        return {
            **browser_context_args,
            "viewport": None,
        }
    return browser_context_args


def _activate_page_window(page: Page, run_mode: str) -> None:
    try:
        page.bring_to_front()
    except Exception:
        pass

    if run_mode != "maximized":
        return

    try:
        session = page.context.new_cdp_session(page)
        window_info = session.send("Browser.getWindowForTarget")
        session.send(
            "Browser.setWindowBounds",
            {
                "windowId": window_info["windowId"],
                "bounds": {"windowState": "maximized"},
            },
        )
        return
    except Exception:
        pass

    try:
        page.evaluate(
            """() => {
                window.moveTo(0, 0);
                window.resizeTo(screen.availWidth, screen.availHeight);
            }"""
        )
    except Exception:
        pass


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """
    Fixture that provides a page with completed Despachoprevio (Microsoft SSO) authentication.

    Environment variables required:
    - DSP_BASE_URL: Base URL for the Pega application
    - DSP_USERNAME: Microsoft SSO username/email
    - DSP_PASSWORD: Microsoft SSO password
    """
    import os
    from pages.microsoft_login_page import MicrosoftLoginPage

    base_url = os.environ.get(
        "DSP_BASE_URL",
        "https://cndral-termmg-stg2.pegacloud.net/prweb/PRAuth"
    )
    username = os.environ["DSP_USERNAME"]
    password = os.environ["DSP_PASSWORD"]

    # Navigate to Pega login page
    page.goto(base_url, wait_until="networkidle")

    # Click 'Login with Despachoprevio' button
    login_button = page.get_by_role("button", name="Login with despachoprevio")
    login_button.click()

    # Complete Microsoft SSO authentication
    page.wait_for_load_state("networkidle")
    ms_login = MicrosoftLoginPage(page)
    ms_login.complete_login(username, password, stay_signed_in=False)

    # Wait for redirect back to Pega application
    page.wait_for_load_state("networkidle", timeout=30000)
    page.wait_for_url("**/pegacloud.net/**", timeout=30000)

    return page


@pytest.fixture(autouse=True)
def track_navigation_and_highlight_clicks(page: Page, request: pytest.FixtureRequest):
    """
    Per-test fixture that:
    - Registers the current test's page/dir/counter in thread-local state so the
      Locator patches can access them.
    - Saves a screenshot on every main-frame navigation.
    """
    run_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
    test_dir = RESULTS_DIR / _safe_name(request.node.name) / run_timestamp
    test_dir.mkdir(parents=True, exist_ok=True)

    action_counter = {"value": 0}
    navigation_counter = {"value": 0}
    run_mode = _normalize_run_mode(request.config.getoption("run_mode"))

    _activate_page_window(page, run_mode)

    # Make the current test state available to the patched Locator methods.
    _test_state.current = {
        "page": page,
        "dir": test_dir,
        "counter": action_counter,
    }

    def _on_frame_navigated(frame):
        if frame != page.main_frame:
            return
        navigation_counter["value"] += 1
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
        file_name = f"nav-{navigation_counter['value']:03d}-{timestamp}.png"
        screenshot_path = test_dir / file_name
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
        except Exception:
            # Ignore transient failures if navigation races with page lifecycle.
            pass

    page.on("framenavigated", _on_frame_navigated)

    yield

    page.remove_listener("framenavigated", _on_frame_navigated)
    _test_state.current = None
