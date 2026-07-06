# ScriptGini Sandbox

This repository is the execution and storage framework for Worktop AI-generated QE scripts.

Worktop should use this document as the source of truth for:
- Where to generate and push scripts
- How to store and read test data
- How to execute scripts consistently in this framework
- What standards generated scripts must follow

## Purpose

Worktop ingests functional test steps and generates Playwright + Python pytest scripts.
Generated assets are pushed to the main branch and executed directly from this repository.

Framework stack:
- Python
- pytest
- pytest-playwright
- Playwright (Chromium with Chrome channel by default)

## Repository Structure

- generated-scripts/
	- Project-wise generated tests and their metadata
- generated-scripts/<project-slug>/
	- Python tests: <userstory-id>-<testcase-id>-<testcase-title-slug>.py
	- Metadata: <userstory-id>-<testcase-id>-<testcase-title-slug>.json
	- Optional test data files: .csv, .json, .txt
- integration-tests-shan/
	- Optional integration payload assets used by scenarios
- test-results/
	- Runtime evidence (screenshots and navigation captures), auto-generated
- conftest.py
	- Shared runtime hooks and fixtures (run mode + screenshot instrumentation)
- pytest.ini
	- Default pytest/playwright options
- setup-playwright-python.bat / setup-playwright-python.sh
	- One-time environment setup
- run-playwright-python.bat / run-playwright-python.sh
	- Script execution entry points

## Where Worktop Must Push Scripts

All generated scripts must be committed under:
- generated-scripts/<project-slug>/

Do not write generated scripts into root or unrelated folders.

For each generated test case, Worktop should create:
1. One Python test file (.py)
2. One metadata file (.json)
3. Optional test data file(s) when needed (.csv/.json/.txt)

## Naming Standards

### File naming

Use lowercase kebab-case with this pattern:
- <userstory-id>-<testcase-id>-<testcase-title-slug>.py
- <userstory-id>-<testcase-id>-<testcase-title-slug>.json

Naming convention (authoritative):
- <userstory id>-<testcase id>-<testcase title-slug>

Examples from this repository:
- generated-scripts/demo-shop/tc-002-homepage-rendering-verification-17.py
- generated-scripts/demo-shop/tc-002-homepage-rendering-verification-17.json

Example for the new convention:
- generated-scripts/demo-shop/us-101-tc-002-homepage-rendering-verification.py

### Python test function naming

Each script should expose at least one pytest test function:
- test_tc_<3-digit-case-number>_<snake_case_scenario>

Example:
- test_tc_002_homepage_rendering_verification

## Metadata JSON Contract

Each generated .py file must have a matching .json metadata file.

Required metadata keys:
- script_id
- project_name
- test_case_title
- framework (must be playwright_python)
- llm_provider
- llm_model
- exported_at (ISO timestamp)
- script_path (relative path to the generated .py script)

Example script_path value:
- generated-scripts/demo-shop/tc-001-add-a-new-todo-item-14.py

## Test Data Standards

### Preferred location

Keep test data close to the test script in the same project folder:
- generated-scripts/<project-slug>/

Example:
- generated-scripts/demo-shop/tc-003-shopify-login-search-add-to-cart.csv

### Data access rules

Generated scripts must:
- Use repository-relative paths or Path-based relative resolution
- Avoid absolute machine-specific paths
- Fail with a clear assertion if required data is missing

Recommended pattern:
- Resolve data file path from __file__ (script location), not current working directory assumptions

## Execution Guide

## 1) One-time setup

Windows (CMD/PowerShell):
- setup-playwright-python.bat

Linux/macOS (bash):
- ./setup-playwright-python.sh

This creates .venv, installs dependencies, and installs Playwright browser support.

## 2) Run a generated script

Windows:
- run-playwright-python.bat generated-scripts\demo-shop\tc-002-homepage-rendering-verification-17.py

Linux/macOS:
- ./run-playwright-python.sh generated-scripts/demo-shop/tc-002-homepage-rendering-verification-17.py

If no script path is passed, runner defaults to its configured default script.

## 3) Run mode options

Supported run modes:
- headless
- headed
- maximized

Windows examples:
- set PW_RUN_MODE=headless
- run-playwright-python.bat generated-scripts\demo-shop\tc-002-homepage-rendering-verification-17.py

PowerShell example:
- $env:PW_RUN_MODE = "maximized"
- .\run-playwright-python.bat generated-scripts\demo-shop\tc-003-shopify-login-search-add-to-cart.py

Mode can also be passed through pytest option --run-mode.

## 4) Direct pytest execution

From repository root:
- .venv\Scripts\python.exe -m pytest -v generated-scripts\demo-shop\tc-002-homepage-rendering-verification-17.py

Defaults from pytest.ini include:
- --headed
- --browser chromium
- --browser-channel chrome

## Runtime Evidence and Debug Artifacts

The framework auto-captures screenshots in test-results/ via conftest.py:
- Before and after key Locator interactions
- On main-frame navigations

Generated tests should not disable this behavior.

## Worktop Script Generation Standards

All Worktop-generated scripts must follow these quality standards.

### Required imports and style

- Use pytest and Playwright sync API:
	- from playwright.sync_api import Page, expect
- Keep code deterministic and readable
- Use clear Arrange / Act / Assert flow

### Assertions and validations

- Include step-level validations, not only end-state validation
- Use explicit assertions with actionable error messages
- Validate critical page state after navigation and key user actions

### Locator strategy

- Prefer robust locators in this priority:
	1. get_by_role / accessible selectors
	2. Stable attributes (id, data-*, name)
	3. CSS fallback selectors
- Avoid brittle nth-child or layout-only selectors unless no alternative exists

### Wait strategy

- Use Playwright waits and expect-based synchronization
- Do not use arbitrary long hard sleeps
- Prefer wait_for_load_state and explicit expect visibility/state checks

### Resilience and failure handling

- Handle expected transient conditions gracefully
- Keep helper methods focused and reusable for complex scenarios
- Fail fast with clear assertion messages when preconditions are not met

### Security and credentials

- Do not hardcode real credentials in generated scripts
- Prefer environment variables for secrets and sensitive test data
- Mask or avoid sensitive output in logs and assertions

## Worktop Output Checklist (Mandatory)

For each generated test case, verify all items before committing:
1. Script saved under generated-scripts/<project-slug>/
2. Matching metadata JSON created beside the script
3. Naming follows <userstory-id>-<testcase-id>-<testcase-title-slug> pattern
4. Test function name follows test_tc_xxx_<scenario>
5. Data files (if any) stored in same project folder and referenced relatively
6. Script executes via run-playwright-python.bat or run-playwright-python.sh
7. Assertions are present at key steps and final outcome
8. No absolute local paths and no hardcoded credentials

## Branch and Commit Guidance for Automation

Worktop automation targeting this repository should:
- Push generated scripts and metadata to main branch (as per demo flow)
- Commit only relevant generated files and required supporting test data
- Avoid modifying framework bootstrap files unless intentionally updating framework behavior

## Known Framework Defaults

- Browser: Chromium
- Channel: Chrome
- Default pytest mode from pytest.ini: headed
- Runtime screenshots: enabled through conftest.py hooks

## Required Environment Variables

The following environment variables must be set before running tests that require authentication or access to external systems:

| Variable | Description | Example |
|----------|-------------|---------|
| `BASE_URL` | Application base URL for login | `https://your-application-url.com/` |
| `APP_USERNAME` | Application username or email for authentication | `your_username` |
| `APP_PASSWORD` | Application password for authentication | `your_password` |

### Setting Environment Variables

**Windows (CMD):**
```cmd
set BASE_URL=https://your-application-url.com/
set APP_USERNAME=your_username
set APP_PASSWORD=your_password
```

**Windows (PowerShell):**
```powershell
$env:BASE_URL="https://your-application-url.com/"
$env:APP_USERNAME="your_username"
$env:APP_PASSWORD="your_password"
```

**Linux/macOS (bash):**
```bash
export BASE_URL="https://your-application-url.com/"
export APP_USERNAME="your_username"
export APP_PASSWORD="your_password"
```

**Using a .env file (recommended for local development):**

Create a `.env` file in the repository root:

```env
BASE_URL=https://your-application-url.com/
APP_USERNAME=your_username
APP_PASSWORD=your_password
```

**Note:** Never commit the `.env` file or any file containing real credentials to version control.

## Maintainers Notes

If framework conventions change, update this README first so Worktop generation remains aligned with the active standard.
