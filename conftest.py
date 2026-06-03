from datetime import datetime
from pathlib import Path
import re

import pytest
from playwright.sync_api import Page


RESULTS_DIR = Path("test-results")


def _safe_name(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return safe or "test"


_HIGHLIGHT_SCRIPT = """
() => {
  const styleId = '__pw-click-highlight-style';
  const markerAttr = 'data-pw-click-highlight-bound';
  const activeClass = '__pw-click-highlight';

  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      .${activeClass} {
        outline: 3px solid darkgreen !important;
        outline-offset: 2px !important;
        box-shadow: 0 0 0 2px rgba(0, 100, 0, 0.3) !important;
        transition: outline 120ms ease-in-out;
      }
    `;
    document.head.appendChild(style);
  }

  if (!document.documentElement.hasAttribute(markerAttr)) {
    document.documentElement.setAttribute(markerAttr, '1');

    document.addEventListener('click', (event) => {
      const target = event.target instanceof Element ? event.target : null;
      if (!target) {
        return;
      }

      const previous = document.querySelector('.' + activeClass);
      if (previous && previous !== target) {
        previous.classList.remove(activeClass);
      }

      target.classList.add(activeClass);
      setTimeout(() => target.classList.remove(activeClass), 1200);
    }, true);
  }
}
"""


@pytest.fixture(autouse=True)
def track_navigation_and_highlight_clicks(page: Page, request: pytest.FixtureRequest):
    """Highlight clicked elements and save screenshots for each main-frame navigation."""
    test_dir = RESULTS_DIR / _safe_name(request.node.name)
    test_dir.mkdir(parents=True, exist_ok=True)

    navigation_counter = {"value": 0}

    page.add_init_script(_HIGHLIGHT_SCRIPT)

    # Also inject into the current document so the first page is covered.
    try:
        page.evaluate(_HIGHLIGHT_SCRIPT)
    except Exception:
        # Some transitional documents can reject evaluation; next navigation re-injects.
        pass

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
