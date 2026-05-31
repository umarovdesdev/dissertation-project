@echo off
REM ============================================================
REM  Запуск React-демо + Cloudflare Quick Tunnel
REM  Откроет два окна: dev-сервер на :3000 и cloudflared tunnel
REM ============================================================

cd /d "%~dp0"

echo [1/2] Запускаю React dev-сервер на http://localhost:3000 ...
start "React dev server" cmd /k "npm start"

echo Жду 15 секунд пока React поднимется...
timeout /t 15 /nobreak >nul

echo [2/2] Запускаю Cloudflare Quick Tunnel ...
start "Cloudflare Tunnel" cmd /k "cloudflared tunnel --url http://localhost:3000"

echo.
echo Готово. В окне "Cloudflare Tunnel" появится публичный URL вида:
echo   https://xxxx-xxxx-xxxx.trycloudflare.com
echo.
pause
