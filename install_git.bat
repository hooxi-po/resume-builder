@echo off
chcp 65001 >nul
echo ========================================
echo Git Installation and Configuration Script
echo ========================================
echo.

echo Downloading Git for Windows...
echo Download URL: https://registry.npmmirror.com/-/binary/git-for-windows/v2.47.1.windows.1/Git-2.47.1-64-bit.exe
echo.
echo Please manually download and install Git:
echo 1. Open browser and visit: https://gitforwindows.org/
echo 2. Or use China mirror: https://registry.npmmirror.com/-/binary/git-for-windows/v2.47.1.windows.1/Git-2.47.1-64-bit.exe
echo 3. Run the installer after download
echo 4. Keep default settings during installation
echo.
echo After installation, please run this script again for configuration
echo.
pause

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed or not added to PATH
    echo Please install Git first and then run this script
    pause
    exit /b 1
)

echo Git is installed, version info:
git --version
echo.

echo ========================================
echo Configure Git User Information
echo ========================================
echo.

set /p username="Enter your GitHub username: "
set /p email="Enter your GitHub email: "

echo.
echo Configuring Git user information...
git config --global user.name "%username%"
git config --global user.email "%email%"

echo Configuration completed!
echo Username: %username%
echo Email: %email%
echo.

echo ========================================
echo Initialize Git Repository
echo ========================================
echo.

if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo Repository initialization completed!
) else (
    echo Git repository already exists
)

echo.
echo ========================================
echo Create .gitignore File
echo ========================================
echo.

if not exist ".gitignore" (
    echo Creating .gitignore file...
    echo # Ignore temporary files > .gitignore
    echo *.tmp >> .gitignore
    echo *.log >> .gitignore
    echo .DS_Store >> .gitignore
    echo Thumbs.db >> .gitignore
    echo node_modules/ >> .gitignore
    echo .gitignore file created successfully!
) else (
    echo .gitignore file already exists
)

echo.
echo ========================================
echo Configuration Completed!
echo ========================================
echo.
echo Next steps:
echo 1. Create a new repository on GitHub
echo 2. Copy the repository HTTPS or SSH address
echo 3. Run quick_commit.bat script for quick commit
echo.
pause