# Demo — launch runbook

> How to run the defense demo (FastAPI backend + React frontend), locally and publicly.
> Machine-readable source of truth for Claude: `PROJECT_MEMORY/demo-stack.md`.

Stack = **`demo/server/`** (FastAPI inference, CUDA) + **`demo/web/`** (React CRA dashboard).
The uvicorn module is `server.app.main:app`, run **from `demo/`** (not repo root).

**Checkpoint:** `demo/server/checkpoints/config_d_fold0.pt` (EfficientNet-B3 4-ch, ~129 MB,
gitignored) + `eyepacs_norm_stats.json` (APTOS interim, n=3662 — NOT thesis-faithful; swap
for the EyePACS/Colab checkpoint before defense).

## Local

**Backend** (WSL2 Ubuntu, conda `dr-classifier`; conda not on PATH; default WSL distro is
docker-desktop, so pass `-d Ubuntu`):
```
wsl -d Ubuntu bash -lc "cd /mnt/e/dissertation-project/demo && \
  ~/miniconda3/bin/conda run --no-capture-output -n dr-classifier \
  uvicorn server.app.main:app --host 127.0.0.1 --port 8000"
```
Check: `/api/health` → `checkpoint_loaded:true, device:cuda`; `/api/selftest` → all pass.
CORS allowlist from env `CORS_ORIGINS` (default `http://localhost:3000`).

**Frontend** (Windows, Node, CRA), from `demo/web`:
```
set BROWSER=none && npm start      # → http://localhost:3000
```
`demo/web/.env.development` sets `REACT_APP_API_URL=http://localhost:8000`. CRA reads
`REACT_APP_*` at startup — override via env, don't edit the file mid-session.

## Public (real model) — Cloudflare quick tunnels

The dashboard shows "simulator (backend offline)" for remote users unless the backend is
ALSO tunnelled (browser mixed-content blocks calling `http://localhost:8000` from an HTTPS
page). cloudflared: `C:\Program Files (x86)\cloudflared\cloudflared.exe`.

1. `cloudflared tunnel --url http://localhost:3000` → FRONTEND url `https://<a>.trycloudflare.com`
2. `cloudflared tunnel --url http://localhost:8000` → BACKEND url `https://<b>.trycloudflare.com`
3. Relaunch **backend** with `export CORS_ORIGINS='http://localhost:3000,https://<a>.trycloudflare.com'`
4. Relaunch **frontend** with `set REACT_APP_API_URL=https://<b>.trycloudflare.com`
5. Verify CORS: `curl -X OPTIONS <backend>/api/predict -H "Origin: <frontend>"` → 200.

URLs are random per launch → set the frontend API target AFTER the backend tunnel exists;
restart the frontend whenever the backend tunnel changes. `demo/web/start-tunnel.bat` only
tunnels the frontend and ends on a blocking `pause` — don't use it in a non-interactive shell.
Free ports: WSL `pkill -f 'uvicorn server.app.main'`; Windows kill the PID on :3000.
All servers/tunnels are session-bound — they die with the session/WSL; relaunch as above.
