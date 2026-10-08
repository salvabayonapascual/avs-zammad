@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0montar-zammad.ps1" %*
exit /b %errorlevel%
