@echo off
REM Di chuyen den thu muc chua file .bat nay
cd /d "%~dp0"

REM === Thay đổi tên file Python chính tại đây ===
set MAIN_SCRIPT=manager.py

REM Lenh tasklist de tim tien trinh python.exe dang chay file script cu the
REM (Thay 'manager.py' nếu bạn đổi tên file)
tasklist /V /FI "IMAGENAME eq python.exe" | find "%MAIN_SCRIPT%" > nul

REM Kiem tra ma loi. Neu khong tim thay, thi chay lai script
if %ERRORLEVEL% NEQ 0 (
    echo %date% %time%: Script %MAIN_SCRIPT% is not running. Starting it now...
    REM Chay script trong nen
    start /B python "%MAIN_SCRIPT%"
) else (
    echo %date% %time%: Script %MAIN_SCRIPT% is already running.
)

REM Giu cua so CMD mo de xem ket qua
echo.
echo ============================================
echo Da kiem tra xong. Nhan phim bat ky de dong.
pause > nul
