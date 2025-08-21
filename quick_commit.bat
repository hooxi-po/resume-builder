@echo off
chcp 65001 >nul
echo ========================================
echo GitHub Quick Commit Script
echo ========================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed!
    echo Please run install_git.bat first to install Git
    pause
    exit /b 1
)

REM Check if current directory is a Git repository
if not exist ".git" (
    echo Error: Current directory is not a Git repository!
    echo Please run install_git.bat first to initialize repository
    pause
    exit /b 1
)

echo Current Git status:
git status --porcelain
echo.

REM Check if remote repository exists
git remote -v >nul 2>&1
if %errorlevel% neq 0 (
    echo Remote repository not configured yet
    echo.
    set /p repo_url="Enter GitHub repository URL (https://github.com/username/repo.git): "
    echo Adding remote repository...
    git remote add origin !repo_url!
    if %errorlevel% neq 0 (
        echo Error: Failed to add remote repository!
        pause
        exit /b 1
    )
    echo Remote repository added successfully!
    echo.
)

echo Remote repository info:
git remote -v
echo.

REM Get commit message
set /p commit_msg="Enter commit message (default: Update code): "
if "%commit_msg%"=="" set commit_msg=Update code

echo.
echo ========================================
echo Starting Commit Process
echo ========================================
echo.

echo 1. Adding all files to staging area...
git add .
if %errorlevel% neq 0 (
    echo Error: Failed to add files!
    pause
    exit /b 1
)
echo ✓ Files added successfully

echo.
echo 2. Committing to local repository...
git commit -m "%commit_msg%"
if %errorlevel% neq 0 (
    echo Warning: No new changes to commit
)
echo ✓ Local commit completed

echo.
echo 3. Pushing to GitHub...
git push -u origin main
if %errorlevel% neq 0 (
    echo Trying to push to master branch...
    git push -u origin master
    if %errorlevel% neq 0 (
        echo Error: Push failed!
        echo Possible reasons:
        echo - Network connection issues
        echo - Authentication failed (need GitHub Token)
        echo - Branch name mismatch
        echo.
        echo Please check network connection and GitHub authentication
        pause
        exit /b 1
    )
)
echo ✓ Push completed

echo.
echo ========================================
echo 🎉 Code successfully committed to GitHub!
echo ========================================
echo.
echo Commit message: %commit_msg%
echo Remote repository: 
git remote get-url origin
echo.
echo You can visit GitHub to view your code updates
pause