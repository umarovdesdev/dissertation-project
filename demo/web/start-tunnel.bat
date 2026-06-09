@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM  Start the FULL demo stack with the REAL model, exposed
REM  publicly via two Cloudflare quick tunnels.
REM
REM  Opens 4 windows:
REM    - Cloudflare Tunnel (frontend)  -> public URL for :3000
REM    - Cloudflare Tunnel (backend)   -> public URL for :8000
REM    - Backend (WSL/CUDA)            -> FastAPI inference, :8000
REM    - Frontend (CRA)                -> React dev server, :3000
REM
REM  Why both tunnels: an HTTPS dashboard cannot call
REM  http://localhost:8000 from a remote browser (mixed-content
REM  block) -> it falls back to the in-browser simulator. So the
REM  backend gets its own HTTPS tunnel, the frontend is pointed at
REM  it (REACT_APP_API_URL), and the backend allows the frontend
REM  tunnel origin (CORS_ORIGINS).
REM
REM  Quick-tunnel URLs are random each run, so we create the
REM  tunnels first, capture their URLs, then start the servers
REM  wired to those URLs.
REM
REM  NOTE: WSL path is hardcoded to /mnt/e/dissertation-project.
REM        This kills any cloudflared.exe and frees :3000 first.
REM ============================================================

cd /d "%~dp0"

set "CFLOG_F=%TEMP%\cf_frontend.log"
set "CFLOG_B=%TEMP%\cf_backend.log"
del "%CFLOG_F%" "%CFLOG_B%" >nul 2>&1

echo [0/5] Cleaning up old processes / freeing ports ...
taskkill /f /im cloudflared.exe >nul 2>&1
for /f "tokens=5" %%p in ('netstat -ano ^| findstr /r /c:":3000 .*LISTENING"') do taskkill /f /pid %%p >nul 2>&1
wsl -d Ubuntu bash -lc "pkill -f 'uvicorn server.app.main' >/dev/null 2>&1; exit 0"

echo [1/5] Starting Cloudflare tunnel for FRONTEND (:3000) ...
start "Cloudflare Tunnel (frontend)" cmd /k cloudflared tunnel --url http://localhost:3000 --logfile "%CFLOG_F%"

echo        Waiting for the frontend tunnel URL ...
:waitF
set "URL_F="
for /f "usebackq delims=" %%u in (`powershell -NoProfile -Command "if(Test-Path '%CFLOG_F%'){$m=Select-String -Path '%CFLOG_F%' -Pattern 'https://[a-z0-9-]+\.trycloudflare\.com';if($m){($m|Select-Object -First 1).Matches[0].Value}}"`) do set "URL_F=%%u"
if not defined URL_F ( timeout /t 1 /nobreak >nul & goto waitF )
echo        Frontend tunnel: !URL_F!

echo [2/5] Starting Cloudflare tunnel for BACKEND (:8000) ...
start "Cloudflare Tunnel (backend)" cmd /k cloudflared tunnel --url http://localhost:8000 --logfile "%CFLOG_B%"

echo        Waiting for the backend tunnel URL ...
:waitB
set "URL_B="
for /f "usebackq delims=" %%u in (`powershell -NoProfile -Command "if(Test-Path '%CFLOG_B%'){$m=Select-String -Path '%CFLOG_B%' -Pattern 'https://[a-z0-9-]+\.trycloudflare\.com';if($m){($m|Select-Object -First 1).Matches[0].Value}}"`) do set "URL_B=%%u"
if not defined URL_B ( timeout /t 1 /nobreak >nul & goto waitB )
echo        Backend tunnel: !URL_B!

echo [3/5] Starting BACKEND (WSL/CUDA) with CORS for the frontend tunnel ...
start "Backend (WSL/CUDA)" cmd /k wsl -d Ubuntu bash -lc "cd /mnt/e/dissertation-project/demo && export CORS_ORIGINS='http://localhost:3000,!URL_F!' && ~/miniconda3/bin/conda run --no-capture-output -n dr-classifier uvicorn server.app.main:app --host 127.0.0.1 --port 8000"

echo [4/5] Starting FRONTEND (CRA) pointed at the backend tunnel ...
start "Frontend (CRA)" cmd /k "set BROWSER=none&&set REACT_APP_API_URL=!URL_B!&&npm start"

echo [5/5] Bringing everything up (give the model ~15s to load) ...
timeout /t 12 /nobreak >nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "$rows=@([pscustomobject]@{Role='Backend (WSL/CUDA)';Location=':8000';Window='Backend (WSL/CUDA)'},[pscustomobject]@{Role='Frontend (CRA)';Location=':3000';Window='Frontend (CRA)'},[pscustomobject]@{Role='Frontend tunnel';Location='!URL_F!';Window='Cloudflare Tunnel (frontend)'},[pscustomobject]@{Role='Backend tunnel';Location='!URL_B!';Window='Cloudflare Tunnel (backend)'});$cols=@('Role','Location','Window');$w=@{};foreach($c in $cols){$m=$c.Length;foreach($r in $rows){if($r.$c.Length -gt $m){$m=$r.$c.Length}};$w[$c]=$m};$H=[char]0x2500;$V=[char]0x2502;$TL=[char]0x250C;$TM=[char]0x252C;$TR=[char]0x2510;$ML=[char]0x251C;$MM=[char]0x253C;$MR=[char]0x2524;$BL=[char]0x2514;$BM=[char]0x2534;$BR=[char]0x2518;function Bd($l,$mid,$rr){$s=$l;for($i=0;$i -lt $cols.Count;$i++){$s+=([string]$H*($w[$cols[$i]]+2));if($i -lt $cols.Count-1){$s+=$mid}else{$s+=$rr}};$s};function Rw($vals){$s=[string]$V;for($i=0;$i -lt $cols.Count;$i++){$s+=' '+([string]$vals[$i]).PadRight($w[$cols[$i]])+' '+$V};$s};[Console]::OutputEncoding=[Text.Encoding]::UTF8;Write-Host '';Write-Host '  Running processes (all session-bound)';Write-Host '';Bd $TL $TM $TR;Rw @('Role','Location','Window');Bd $ML $MM $MR;foreach($r in $rows){Rw @($r.Role,$r.Location,$r.Window)};Bd $BL $BM $BR"

echo.
echo Done. Open the demo at: !URL_F!
echo (The dashboard should show "real model" - it calls the backend tunnel.)
echo Closing the 4 windows above stops the stack.
echo.
pause
endlocal
