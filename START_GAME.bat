@echo off
cd /d "%~dp0"
if exist "%~dp0START_GAME.exe" (
 "%~dp0START_GAME.exe"
) else (
 echo Extract the WHOLE project ZIP first. START_GAME.exe must be beside this file.
)
pause
