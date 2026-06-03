@echo off
setlocal

set "KNOWN_PY=C:\Users\Ravi.Konduru\AppData\Local\Python\pythoncore-3.14-64\python.exe"
set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_ACTIVATE=%VENV_DIR%\Scripts\activate.bat"

if not exist "%VENV_PY%" (
  echo Creating virtual environment in %VENV_DIR%...

  if exist "%KNOWN_PY%" (
    "%KNOWN_PY%" -m venv "%VENV_DIR%"
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
    goto :venv_ready
  )

  where python >nul 2>&1
  if %ERRORLEVEL%==0 (
    python -m venv "%VENV_DIR%"
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
    goto :venv_ready
  )

  where py >nul 2>&1
  if %ERRORLEVEL%==0 (
    py -3 -m venv "%VENV_DIR%"
    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
    goto :venv_ready
  )

  echo Error: Could not find a working Python interpreter to create a virtual environment.
  exit /b 1
)

:venv_ready

call "%VENV_ACTIVATE%"
if %ERRORLEVEL% neq 0 (
  echo Error: Failed to activate virtual environment.
  exit /b %ERRORLEVEL%
)

echo Installing Python dependencies for Playwright tests in %VENV_DIR%...
python -m pip install -U pip
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
python -m pip install -U pytest pytest-playwright playwright
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
python -m playwright install chromium
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo.
echo Setup complete.
echo Current script used environment: %CD%\%VENV_DIR%
echo To activate in CMD: call %VENV_ACTIVATE%
echo To activate in PowerShell: .\%VENV_DIR%\Scripts\Activate.ps1
exit /b 0
