@echo off
chcp 65001 > nul
echo Git Hooks 심볼릭 링크 생성 스크립트를 실행합니다...

:: check admin authority
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo 관리자 권한이 필요합니다. 관리자 권한으로 다시 실행합니다...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

set CURRENT_DIR=%CD%
set SOURCE_DIR=%CURRENT_DIR%\hooks
set TARGET_DIR=%CURRENT_DIR%\.git\hooks

:: if exist
if exist "%TARGET_DIR%" (
    echo 기존 .git\hooks 폴더를 백업합니다...
    if not exist "%CURRENT_DIR%\.git\hooks_backup" (
        mkdir "%CURRENT_DIR%\.git\hooks_backup"
    )
    
    :: back up
    for %%f in ("%TARGET_DIR%\*") do (
        if not "%%~nxf"=="." if not "%%~nxf"==".." (
            copy "%%f" "%CURRENT_DIR%\.git\hooks_backup\" > nul
        )
    )
    
    :: remove
    rmdir /S /Q "%TARGET_DIR%"
    echo 기존 .git\hooks 폴더를 삭제했습니다.
)

:: generate symbolic link
mklink /D "%TARGET_DIR%" "%SOURCE_DIR%"

if %errorlevel% equ 0 (
    echo 폴더 심볼릭 링크가 성공적으로 생성되었습니다.
    echo 소스 폴더: %SOURCE_DIR%
    echo 대상 폴더: %TARGET_DIR%
) else (
    echo 폴더 심볼릭 링크 생성 중 오류가 발생했습니다.
)

echo 스크립트 실행이 완료되었습니다. 아무 키나 누르면 종료합니다...
pause > nul