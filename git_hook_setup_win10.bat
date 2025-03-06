@echo off
chcp 65001 > nul
echo Git Hooks 심볼릭 링크 생성 스크립트를 실행합니다...

:: 관리자 권한 확인
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 이 스크립트는 관리자 권한이 필요합니다.
    echo 명령 프롬프트를 관리자 권한으로 실행한 후 다시 시도해주세요.
    pause
    exit /B 1
)

:: 현재 디렉토리 설정
set CURRENT_DIR=%CD%
set SOURCE_DIR=%CURRENT_DIR%\hooks
set TARGET_DIR=%CURRENT_DIR%\.git\hooks

:: hooks 폴더가 존재하는지 확인
if not exist "%SOURCE_DIR%" (
    echo hooks 폴더가 존재하지 않습니다. 폴더를 생성합니다...
    mkdir "%SOURCE_DIR%"
    echo hooks 폴더가 생성되었습니다.
)

:: .git 폴더가 존재하는지 확인
if not exist "%CURRENT_DIR%\.git" (
    echo .git 폴더가 존재하지 않습니다. 이 스크립트는 Git 저장소에서 실행해야 합니다.
    pause
    exit /B 1
)

:: 기존 hooks 폴더 처리
if exist "%TARGET_DIR%" (
    echo 기존 .git\hooks 폴더를 백업합니다...
    if not exist "%CURRENT_DIR%\.git\hooks_backup" (
        mkdir "%CURRENT_DIR%\.git\hooks_backup"
    )
    
    :: 백업
    for %%f in ("%TARGET_DIR%\*") do (
        if not "%%~nxf"=="." if not "%%~nxf"==".." (
            copy "%%f" "%CURRENT_DIR%\.git\hooks_backup\" > nul
        )
    )
    
    :: 삭제
    rmdir /S /Q "%TARGET_DIR%"
    echo 기존 .git\hooks 폴더를 삭제했습니다.
)

:: 심볼릭 링크 생성
mklink /D "%TARGET_DIR%" "%SOURCE_DIR%"

if %errorlevel% equ 0 (
    echo 폴더 심볼릭 링크가 성공적으로 생성되었습니다.
    echo 소스 폴더: %SOURCE_DIR%
    echo 대상 폴더: %TARGET_DIR%
)

echo 스크립트 실행이 완료되었습니다. 아무 키나 누르면 종료합니다...
pause > nul 