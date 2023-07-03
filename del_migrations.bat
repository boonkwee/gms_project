@echo off
echo You are about to clear migration, are you sure (Y/N)
choice /C YN

if errorlevel 2 (
    echo Selected No, bye.
) else (
    for /d %%i in (*) do if EXIST "%%i\migrations" del "%%i\migrations\000?_*.py
    echo Migrations patch scripts cleared
    echo Please proceed to clear the data migration data in the DB
)
