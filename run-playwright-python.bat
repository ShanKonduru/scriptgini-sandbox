@echo off
setlocal

REM set "DEFAULT_SCRIPT=generated-scripts\demo-shop\tc-002-homepage-rendering-verification-17.py"
set "DEFAULT_SCRIPT=generated-scripts\demo-shop\tc-003-graceful-error-page-handling-18.py"

set "SCRIPT=%~1"
if "%SCRIPT%"=="" (
  set "SCRIPT=%DEFAULT_SCRIPT%"
) else (
  shift
)
set "VENV_PY=.venv\Scripts\python.exe"
set "PLAYWRIGHT_ARGS=--headed --browser chromium --browser-channel chrome"

if not exist "%SCRIPT%" (
  echo Error: Script not found: %SCRIPT%
  exit /b 1
)

echo Running Playwright pytest: %SCRIPT%

set "KNOWN_PY=C:\Users\Ravi.Konduru\AppData\Local\Python\pythoncore-3.14-64\python.exe"

if exist "%VENV_PY%" (
  "%VENV_PY%" -m pytest -v %PLAYWRIGHT_ARGS% "%SCRIPT%" %*
  goto :done
)

if exist "%KNOWN_PY%" (
  "%KNOWN_PY%" -m pytest -v %PLAYWRIGHT_ARGS% "%SCRIPT%" %*
  goto :done
)

where python >nul 2>&1
if %ERRORLEVEL%==0 (
  python -m pytest -v %PLAYWRIGHT_ARGS% "%SCRIPT%" %*
  goto :done
)

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  py -3 -m pytest -v %PLAYWRIGHT_ARGS% "%SCRIPT%" %*
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
