@echo off
echo WARNING: This will force close ALL Python processes running on this machine.
echo Press Ctrl+C to cancel, or any key to continue.
pause

taskkill /F /IM python.exe

echo.
echo All Python processes have been terminated.
pause
