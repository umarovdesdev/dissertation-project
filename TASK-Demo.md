# TASK.md — Demo Production Launch (Academic Beta)

**Owner:** Yesmukhamedov N.S.
**Executor:** Claude Code
**Goal:** Take `demo/` from its current simulated state to a **beta release** accessible to a closed academic audience — the candidate's supervisor, the department's professors, and the dissertation committee — that demonstrates the dissertation thesis end-to-end on arbitrary fundus uploads.

**Companion task:** This document depends on `TASK-Config-D.md` (Parts A–C) for the model checkpoint, the FastAPI backend, and the initial frontend wiring. TASK-Demo.md is the *launch layer* on top of that: scope, access, polish, on-demand visualization, and the QA gate before sharing the URL.

---

## 0. Decisions already made

| Question | Answer |
|---|---|
| Audience | Closed academic beta — supervisor, department professors, committee members (~15 people). No public exposure. |
| Purpose | Demonstrate the dissertation thesis (P2 paradigm: V5 preprocessing + EfficientNet-B3 = Config D) on arbitrary fundus uploads. |
| Out of scope for beta | Legal disclaimers beyond a one-line research-prototype banner; clinical certification; marketing copy; rate limiting; user accounts; analytics; multi-tenancy; PII handling beyond "don't persist images". |
| Inference path | FastAPI backend + PyTorch (per TASK-Config-D Part B). Browser-only inference rejected — would diverge from the thesis-defended pipeline. |
| Model | Config D, EfficientNet-B3, single best fold (fold with highest `val_weighted_f1`). No ensemble — overkill for a demo. |
| Preprocessing | Full V5 pipeline (all 8 stages) at inference, imported from `experiments/src/preprocessing/pipeline_v5.py`. No re-implementation. |
| OD/Fovea detection | Classical CV from `experiments/src/preprocessing/od_fovea_detect.py`. No ML model — preserves SC-F contribution framing. |
| Grad-CAM | Computed on demand from the live checkpoint (not pre-rendered stubs). Pre-rendered walkthrough assets stay only as offline fallback. |
| Access control | Shared URL gated by a single static password (env-var on backend). Adequate for a ~15-person academic audience. |
| Hosting | HuggingFace Spaces (Docker SDK) for backend, static hosting (Vercel / GitHub Pages) for the React frontend. |
| Image retention | None. All uploads processed in memory, dropped after response. No disk writes, no logs containing image bytes. |

---

## Part A — Audience & scope contract

### A.1 Who can use it

- The candidate's scientific supervisor.
- IITU department professors involved in supervision.
- Dissertation committee members.
- The candidate and co-authors of own publications (`literature/self/`).

Anyone outside this list is out of scope. The single shared password is the access boundary; no per-user accounts.

### A.2 What the beta must demonstrate

These are the deliverables the demo exists to show, mapped to contributions in `thesis/governance/CONTRIBUTIONS.md`:

| Demo capability | Backed by contribution |
|---|---|
| Arbitrary fundus image → DR grade (0–4) | C-1 (V5 + CNN as integrated model) |
| Per-eye + patient-level (worst-eye) prediction | Implementation §8 (PatientHead optional, not required for beta) |
| Real Grad-CAM overlay on uploaded image | C-3 (ALO, lesion preservation analysis) |
| OD/Fovea center visualization on uploaded image | SC-F (classical-CV-based OD/fovea detection) |
| FOV mask preview (the 4th input channel) | SC-E (FOV mask as explicit pipeline component) |
| Side-by-side baseline-vs-V5 preprocessing strip | C-1 (P2 paradigm contrast, visual evidence of preprocessing as model component) |

If any of the six above does not work for arbitrary uploads at launch, the beta is not ready.

### A.3 What the beta deliberately does NOT do

- No regulatory framing, no FDA/MDR/EAEU posture.
- No clinical decision support claims in copy.
- No persistent storage of uploaded images.
- No anonymization audit — the audience is academic, the assumption is no real-patient PHI is being uploaded; the one-line banner says so.
- No A/B variants, telemetry, growth tooling.

---

## Part B — What must be REAL vs simulated at launch

The current `Demo.js` uses simulated `predictEye` and pre-rendered Grad-CAM. For the beta, the following must be **live model output**:

| Component | Current state | Required state for beta |
|---|---|---|
| Per-eye DR grade prediction | Hash-based RNG (`predictEye`) | Call to `POST /api/predict`, real EfficientNet-B3 output |
| Per-eye softmax probabilities | RNG-derived | Real model softmax |
| Confidence | `probs[pred]` from RNG | `probs[pred]` from real softmax |
| Latency | Simulated `setTimeout(700ms)` | Real wall-clock from backend (`latency_ms` in response) |
| Grad-CAM heatmap | Pre-rendered PNG for dr00–dr04 only | Computed on demand for any upload via `POST /api/gradcam` |
| Attention overlay | Pre-rendered PNG | Computed alongside Grad-CAM (alpha blend over original RGB) |
| OD/Fovea markers | Not shown | Drawn on the uploaded image: two circles (OD radius, fovea radius), axis line, confidence chip |
| FOV mask | Not shown | Small thumbnail toggle next to the eye preview |

The simulator stays in the codebase as **fallback only**: triggered when the backend `/api/health` is unreachable, with a visible amber chip saying "simulator (backend offline)". This keeps offline demos working but is never the default during the beta.

---

## Part C — Backend hardening for the beta

Picks up from `TASK-Config-D.md` Part B. Additions specifically for production:

### C.1 New endpoints

```
GET  /api/health
      → { status, model, checkpoint_id, device, git_sha, version }
      version = semver string from server/__version__.py — used in the demo footer

POST /api/predict
      multipart { left?: File, right?: File, password: str }
      → PatientPredictionResponse (same shape as TASK-Config-D.md §B.3)
      additionally: od_fovea: { left?: ODFoveaPayload, right?: ODFoveaPayload }

POST /api/gradcam
      multipart { eye: "left"|"right", image: File, password: str }
      → { gradcam_png_b64, attention_overlay_png_b64, target_class: int }

POST /api/visualize
      multipart { image: File, password: str }
      → { fov_mask_png_b64, v5_preview_png_b64, od_fovea: ODFoveaPayload }
      v5_preview = grid of intermediate stages (canonical flip, OD-rotation,
                   FOV crop, flat-field, CLAHE) for the "what preprocessing
                   does" panel
```

`ODFoveaPayload` schema:
```json
{
  "od_center": [x, y],
  "od_radius": 38.2,
  "fovea_center": [x, y],
  "fovea_radius": 19.1,
  "angle_deg": 4.7,
  "rotation_sigma_deg": 7.3,
  "confident": true
}
```

### C.2 Password gate

Implementation:
- Env var `DEMO_PASSWORD` set on the Space. Single static string.
- Every endpoint except `/api/health` checks `password` field. Mismatch → 401.
- Frontend stores the password in `sessionStorage` after first successful submit and includes it in every subsequent request. No login screen — a single input on the landing page with "Enter access password" and a Submit button.
- Wrong password → frontend shows a polite "Access denied — contact the candidate for the beta password" message.

This is intentionally minimal. Anything stronger (OAuth, magic links) is out of scope for ~15 academics.

### C.3 In-memory image handling

- All endpoints accept image bytes via FastAPI's `UploadFile`, decode to `numpy` in memory, never write to disk.
- Tempfile usage banned. If a library needs a path (rare), use `tempfile.NamedTemporaryFile` with `delete=True` inside a `with` block; assert deletion in a unit test.
- Logging: log only `request_id, ip_hash, has_left, has_right, image_size_bytes, grade, latency_ms`. Never log image bytes, never log raw IPs, never log filenames.

### C.4 Safety limits (cheap insurance, not security)

- Max file size: 8 MB per image (FastAPI middleware).
- Allowed MIME: `image/jpeg`, `image/png`, `image/webp`. Reject everything else with 415.
- Max decoded resolution: 4096×4096 (reject larger to prevent decode bombs).
- Per-request timeout: 30 s total.

### C.5 Grad-CAM implementation

- Library: `pytorch-grad-cam`.
- Target layer for EfficientNet-B3: last MBConv block (the layer just before the head). Confirm via `model.features[-1]` after loading the checkpoint; print the layer name once at startup so it's clear which one is being CAM'd.
- Target class: predicted class (argmax of softmax). Optionally accept `target_class` query param for the panel where the user can ask "why class 2?" — out of scope for v1 beta but leave the function signature ready.
- Overlay: resize CAM to original (pre-preprocessing) image size using bilinear, normalize to [0,1], apply JET colormap, alpha-blend at 0.5 over the original RGB. The overlay is over the **original** image, not the preprocessed one — clearer to a non-technical audience.

### C.6 V5 preview strip

`POST /api/visualize` returns one composite PNG showing six panels left-to-right:
1. Original uploaded image (raw).
2. After canonical flip (Stage 0a) — annotated "right-eye orientation".
3. After OD–Fovea rotation (Stage 1) — annotated with the angle applied.
4. After FOV crop + isotropic resize (Stage 2/3).
5. After flat-field correction (Stage 4).
6. After CLAHE (Stage 5).

This panel is the most direct visual argument for P2 (preprocessing as part of the model). It's the picture the committee will remember.

Implementation: a helper `experiments/src/preprocessing/pipeline_v5.py::stage_breakdown(image_rgb)` returns the list of intermediate tensors; the server composes them into a single PNG with stage labels via PIL.

If `stage_breakdown` doesn't exist yet, add it — mirror the main pipeline but capture each intermediate and return them alongside the final tensor.

### C.7 Smoke endpoint for QA

```
GET /api/selftest?password=<DEMO_PASSWORD>
  → runs predict + gradcam + visualize on three fixed bundled test images
    (one from EyePACS DR=0, one DR=2, one DR=4) and returns a pass/fail
    report. Used by the pre-launch checklist in Part F.
```

---

## Part D — Frontend polish for the showcase

### D.1 Landing screen changes

Above the existing two-eye uploader, add a short framing block (3 lines max):

> **Diabetic Retinopathy Diagnosis Demo — V5 Preprocessing + EfficientNet-B3 (Config D)**
> Research prototype accompanying the dissertation by Yesmukhamedov N.S. (IITU). Not a medical device.
> The model demonstrated here is the P2 paradigm formulation: preprocessing as an integral model component.

Render in muted text, no large hero, no marketing copy. Localized in EN and RU.

### D.2 Per-image visualization panel (NEW)

When an image is loaded into a slot — before the user clicks Run — show under the preview a small "what the model sees" widget that calls `/api/visualize` and displays:

- Two overlay markers on the input: OD circle (teal) + fovea circle (coral) + line connecting them.
- A small chip: "OD–fovea angle: 4.7° · σ_rot: 7.3° · ✓ confident" (or "⚠ low confidence, classical rotation skipped").
- A "Show preprocessing stages" expandable that reveals the 6-panel V5 strip.
- A "Show FOV mask" toggle that swaps the preview for the binary mask channel.

This widget is the visual core of contributions C-1, SC-E, and SC-F. It must work on arbitrary uploads, not just the walkthrough cases.

### D.3 Result panel changes

After Run completes, the existing Result section (`Demo.js` lines ~614–683) keeps its layout but:

- Replace pre-rendered `HeatmapPair` with the live Grad-CAM PNG returned by `/api/gradcam`. Same two-pane grid: heatmap + attention overlay.
- Add a third sub-panel "Predicted class rationale": a one-line auto-generated sentence like "Model attends to N pixels coincident with the upper-temporal arcade, consistent with DR grade 2 features." (Generated on backend from CAM region statistics, no LLM.)
- Drop the existing `// <div>⚠ {t('demo.disclaimer')}</div>` (currently commented out) — replace with a single muted footnote: "Beta research demo. Predictions are model output on the dissertation pipeline; not a clinical recommendation."

### D.4 Walkthrough cases for the beta

Curate **exactly five cases** that always work and always look impressive — one per DR grade (0–4) — using EyePACS images where:

- All preprocessing stages succeed (`od_fovea.confident=True`).
- The ground-truth label is unambiguous (no disagreement in EyePACS expert relabeling).
- Grad-CAM falls on a clinically interpretable region (microaneurysm cluster for DR=1, hemorrhage for DR=2, exudates for DR=3, NV/IRMA for DR=4, vessel pattern only for DR=0).

These replace the current `WALKTHROUGH_POOL`. The buttons stay in the same UI position. Selection criteria — five images cherry-picked by the candidate from EyePACS, copied to `demo/public/pipeline/demo_cases/dr0N/`, plus pre-computed Grad-CAMs as offline fallback (in case the backend is briefly unavailable during a demo session).

### D.5 Random EyePACS pair button

Kept as-is from current `Demo.js` (calls `pickRandomEyePacsPair`). Useful for committee members who want to see the model on un-curated data. No change required beyond pointing the inference to the real backend.

### D.6 Feedback & history

Existing relabel/JSONL flow kept as-is. The candidate uses it to harvest committee feedback during the defense.

### D.7 Status badges (visible to user)

In the Run section, render a small status row:

- `● real model` — backend healthy, predictions are live.
- `⚠ simulator (backend offline)` — fallback path active.
- `version v0.1.0 · git f7a3c2 · checkpoint config-d-fold2` — model provenance string, pulled from `/api/health`.

The provenance string is what tells a committee member "I can trust that this is the model from the dissertation, fold 2 of Experiment 1."

---

## Part E — Deployment & access

### E.1 Backend: HuggingFace Space

1. Create Space: `<user>/dr-demo-config-d`, **set to Private** initially.
2. SDK: Docker. Push `Dockerfile` from TASK-Config-D §B.6.
3. Env vars on the Space:
   - `DEMO_PASSWORD` — single static string, shared via direct message to invited academics.
   - `DEMO_VERSION` — semver, bumped per release.
   - `MODEL_CHECKPOINT_ID` — e.g., `config-d-fold2-2026-06-15`.
4. Hardware: CPU Basic tier sufficient for ~15 users. First request after idle: ~10–15 s (model cold-load). Subsequent: 0.5–2 s per `/api/predict` for both eyes, 1–3 s for `/api/gradcam`. Upgrade to T4-small only if multiple committee members hit it simultaneously during the defense.
5. After Space is healthy, **switch visibility to Public** so the React frontend can call it without HF auth. The `DEMO_PASSWORD` gate is what restricts access, not Space visibility.

### E.2 Frontend: static hosting

1. `cd demo && npm run build`.
2. Deploy `demo/build/` to Vercel (recommended) or GitHub Pages.
3. Set `REACT_APP_API_URL=https://<user>-dr-demo-config-d.hf.space` in deployment env.
4. Frontend URL is the one shared with the academic audience.

### E.3 Distribution

- The candidate sends a single email to the invited list with: URL, password, one-paragraph context (what the demo shows, link to thesis abstract).
- No registration form, no Slack/Discord, no tracking pixel in the email.

### E.4 Versioning

Tag every release on the demo repo: `demo-v0.1.0`, `demo-v0.1.1`, etc. The `/api/health` response always returns the running version + git SHA + checkpoint ID. The audience can quote these in feedback.

---

## Part F — Pre-launch verification

Run all of this **before** sending the URL to anyone.

### F.1 Backend self-test

```bash
curl "https://<space>.hf.space/api/health"
# expect: { "status": "ok", "model": "config-D", ... }

curl "https://<space>.hf.space/api/selftest?password=$DEMO_PASSWORD"
# expect: { "predict": "pass", "gradcam": "pass", "visualize": "pass" }
```

### F.2 Frontend smoke (manual, browser)

1. Open the public URL in an incognito window.
2. Enter the password → access granted.
3. Click each of the five walkthrough buttons → verify each loads two images, displays OD/fovea markers, Run produces the expected grade ±1, Grad-CAM renders, V5 strip renders.
4. Click "Random EyePACS pair" five times → verify each loads both eyes, all visualizations produce, no console errors.
5. Upload a non-fundus image (a selfie) → verify "⚠ image does not look like a fundus" chip appears, but submission still works without crash.
6. Upload one custom fundus image → verify full pipeline including live Grad-CAM, live OD/fovea overlay, V5 strip.
7. Take the backend down (pause Space). Reload demo → verify `⚠ simulator (backend offline)` badge appears and walkthrough still works on pre-rendered assets.
8. Restart backend → verify badge returns to `● real model` within 30 s of reload.

### F.3 Provenance check

- `/api/health` returns the checkpoint ID.
- The checkpoint ID matches a fold actually present in `experiments/outputs/exp1/checkpoints/`.
- The git SHA matches a tagged release.
- The footer in the running demo displays the same triple.

### F.4 Sanity prediction range

- On the five curated walkthroughs, accuracy should be 4/5 or 5/5 (predicted grade within ±1 of ground truth). If 3/5 or worse — re-select curated cases or check that the checkpoint is the intended one.
- On 10 random EyePACS pairs, no crashes, all probabilities sum to 1±0.01.

### F.5 Privacy spot-check

- Backend logs (HF Space → Logs) contain no image data, no filenames, no raw IPs. Only `request_id`, `ip_hash`, sizes, grades, latencies.
- No `/tmp` writes — `ls /tmp` on the Space after 20 test requests shows nothing demo-related.

If any of F.1–F.5 fails, do not share the URL.

---

## Part G — Acceptance checklist

- [ ] `TASK-Config-D.md` Part A complete (checkpoint exists at `experiments/outputs/exp1/checkpoints/fold_N/best.pt`).
- [ ] `TASK-Config-D.md` Part B complete (backend boots locally).
- [ ] `TASK-Config-D.md` Part C complete (`Demo.js` calls real backend in local dev).
- [ ] Backend endpoints added: `/api/visualize`, `/api/selftest`, password gate on protected endpoints.
- [ ] `stage_breakdown` exists in `pipeline_v5.py` and returns labeled intermediates.
- [ ] Live Grad-CAM works on arbitrary uploads (not just walkthroughs).
- [ ] Live OD/Fovea overlay works on arbitrary uploads.
- [ ] V5 preview strip endpoint returns a composite PNG with all six stages.
- [ ] Frontend: five curated walkthroughs (one per DR grade) replace previous pool.
- [ ] Frontend: per-image visualization widget renders before Run is clicked.
- [ ] Frontend: status badge shows `real model` when backend is healthy.
- [ ] Frontend: provenance string visible in footer (version + SHA + checkpoint ID).
- [ ] Backend deployed on HF Space (public visibility, password-gated).
- [ ] Frontend deployed on Vercel/GH Pages with production env var pointing to the Space.
- [ ] Part F verification passed end-to-end.
- [ ] Distribution email drafted with URL + password + one-paragraph context.

---

## Part H — Explicitly out of scope for the beta

- Legal disclaimers beyond the one-line research-prototype banner.
- Privacy policy, terms of service, cookie banner.
- User accounts, individual login, OAuth.
- Rate limiting, CAPTCHA, DDoS protection.
- Analytics (Google, Plausible, custom).
- Per-user inference quotas.
- Multi-language beyond EN/RU (KZ translation lives in the thesis, not the demo, per `glossary/`).
- Internationalization of error messages from the backend (English only).
- Mobile-optimized layout (the React demo is already responsive enough; no native app, no PWA install).
- Public marketing (blog post, social share cards, OG images).
- Persistent feedback storage on backend (relabel buffer stays client-side, exported as JSONL by the user, kept as-is from current implementation).
- Real-time updates / streaming inference / WebSockets.
- Multi-model A/B (Config C vs D, ResNet vs EfficientNet) — single Config D only.

These move into scope only after the public release stage, which is a separate task document not authored yet.

---

## Part I — Risks specific to the academic beta

| Risk | Mitigation |
|---|---|
| Committee member uploads a low-quality phone photo of a paper printout — model returns nonsense | Acceptable failure mode. `analyzeFundus` heuristic already warns "does not look like a fundus" and inference still runs. The committee will understand. |
| Backend cold-start (~10–15 s on HF free tier) makes the first demo click look broken | Footer note: "First request after idle may take up to 15 seconds while the model loads." A spinner with progress copy reassures the user. |
| Space goes idle mid-defense | Schedule a `/api/health` ping every 30 minutes during defense day from a separate cron (UptimeRobot free tier or a GitHub Actions cron). |
| Curated walkthroughs accidentally include patient identifiers in EyePACS filenames | EyePACS images are already de-identified, but rename copies to `dr0N_left.png` / `dr0N_right.png` before committing to `demo/public/pipeline/demo_cases/`. |
| Grad-CAM library version drift produces different overlays than what the thesis text shows | Pin `grad-cam==1.5.0` (or whichever version was used for the figures in Chapter 4) in `server/requirements.txt`. Add a note in `server/README.md` explaining why this version is pinned. |
| Password leaks (academic forwards the email beyond the invited list) | Acceptable for beta — the audience is trusted, the demo has no clinical claims. Rotate password if leak is observed; bump `DEMO_PASSWORD` env var on Space and re-email. |
| Committee member asks "why this prediction?" and the live Grad-CAM hangs | Backend timeout 30 s + frontend fallback to pre-rendered overlay for the closest walkthrough case as visual stand-in, with a "live overlay unavailable, showing reference case" badge. |
| Checkpoint file too large for HF free tier git push | EfficientNet-B3 weights ~50 MB, well under HF's 100 MB threshold per file. If a future ensemble is added, use HF Hub's model repo separately and download at container startup. |

---

End of TASK-Demo.md.
