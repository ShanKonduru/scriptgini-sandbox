@echo off
setlocal

set "DEFAULT_SCRIPT=generated-scripts\demo-shop\tc-002-homepage-rendering-verification-17.py"
REM set "DEFAULT_SCRIPT=generated-scripts\demo-shop\tc-003-graceful-error-page-handling-18.py"

REM Run mode options: headless | headed | maximized
set "DEFAULT_RUN_MODE=maximized"
set "RUN_MODE=%PW_RUN_MODE%"
if "%RUN_MODE%"=="" set "RUN_MODE=%DEFAULT_RUN_MODE%"

if /I "%RUN_MODE%"=="max" set "RUN_MODE=maximized"
if /I "%RUN_MODE%"=="maximize" set "RUN_MODE=maximized"
if /I "%RUN_MODE%"=="head" set "RUN_MODE=headed"

if /I "%RUN_MODE%"=="headless" goto :run_mode_ok
if /I "%RUN_MODE%"=="headed" goto :run_mode_ok
if /I "%RUN_MODE%"=="maximized" goto :run_mode_ok

echo Error: Invalid RUN_MODE '%RUN_MODE%'. Use headless, headed, or maximized.
exit /b 1

:run_mode_ok

set "SCRIPT=%~1"
if "%SCRIPT%"=="" (
  set "SCRIPT=%DEFAULT_SCRIPT%"
) else (
  shift
)
set "VENV_PY=.venv\Scripts\python.exe"
set "PLAYWRIGHT_ARGS=--browser chromium --browser-channel chrome"

if not exist "%SCRIPT%" (
  echo Error: Script not found: %SCRIPT%
  exit /b 1
)

echo Running Playwright pytest: %SCRIPT%
echo Run mode: %RUN_MODE%

set "KNOWN_PY=C:\Users\Ravi.Konduru\AppData\Local\Python\pythoncore-3.14-64\python.exe"

if exist "%VENV_PY%" (
  "%VENV_PY%" -m pytest -v %PLAYWRIGHT_ARGS% --run-mode "%RUN_MODE%" "%SCRIPT%" %*
  goto :done
)

if exist "%KNOWN_PY%" (
  "%KNOWN_PY%" -m pytest -v %PLAYWRIGHT_ARGS% --run-mode "%RUN_MODE%" "%SCRIPT%" %*
  goto :done
)

where python >nul 2>&1
if %ERRORLEVEL%==0 (
  python -m pytest -v %PLAYWRIGHT_ARGS% --run-mode "%RUN_MODE%" "%SCRIPT%" %*
  goto :done
)

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  py -3 -m pytest -v %PLAYWRIGHT_ARGS% --run-mode "%RUN_MODE%" "%SCRIPT%" %*
  goto :done
)

echo Error: Could not find a working Python interpreter.
exit /b 1

:done

set "EXITCODE=%ERRORLEVEL%"
if not "%EXITCODE%"=="0" (
  echo Script failed with exit code %EXITCODE%.
)

exit /b %EXITCODE%
