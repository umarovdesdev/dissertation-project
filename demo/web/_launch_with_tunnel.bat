@echo off
set "PATH=C:\Program Files (x86)\cloudflared;%PATH%"
cd /d "%~dp0"
call start-tunnel.bat
