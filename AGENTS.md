# AGENTS.md

## Overview

Flask + single-page HTML app for tracking Chinese civil service exam (国考行测) practice scores. PyInstaller-packaged as a desktop app. All UI text is Chinese (Simplified).

## Commands

```bash
./run.sh              # create venv, install deps, run dev server on :8080
python app.py         # run Flask dev server directly (debug, 0.0.0.0:8080)
python main.py        # desktop launcher (auto-opens browser, 127.0.0.1:8080, no debug)
./build.sh            # build standalone executable via PyInstaller
```

No tests, linter, formatter, or CI exist. There is no `.git` directory.

## Architecture

- **`app.py`** -- Flask backend (257 lines). REST API + serves `templates/index.html`.
- **`main.py`** -- PyInstaller entrypoint. Resolves paths for packaged exe, overrides `DATA_DIR`, auto-opens browser, runs Flask.
- **`templates/index.html`** -- Monolithic SPA (1036 lines) with inline JS/CSS. Uses Tailwind CSS and Chart.js from CDNs.
- **`static/`** -- Empty directory; exists only because `build.spec` bundles it.
- **`data/`** -- Flat JSON files, one per exam module (`{module}_records.json`) plus `mock_records.json`.

## Key Quirks

- **Dual DATA_DIR resolution**: `app.py` sets `DATA_DIR` at import time; `main.py` overrides it post-import via `app_module.DATA_DIR = data_path`. This is intentional for PyInstaller path handling.
- **`main.py` changes cwd** (`os.chdir(base_path)`) so Flask finds templates when frozen. Don't remove this.
- **Port 8080 is hardcoded** in `app.py`, `main.py`, and `run.sh` -- no config mechanism.
- **`pandas` in requirements.txt is unused** -- never imported anywhere. Dead dependency.
- **IDs are re-sequenced on delete** (not stable). Fine for single-user local tool.
- **No authentication** -- API is fully open.
- **`build.spec` hiddenimports** include `engineio.async_drivers.threading` -- required for Flask-SocketIO compat even though SocketIO isn't used. Don't trim.

## Data Model

Each module record: `{id, practice_number, correct_count, total_count, time_minutes, date, notes}`. Mock records use `mock_number` instead. Append-only JSON arrays; IDs re-numbered on delete.

Reviews: `{id, content, date, practice_number/mock_number, created_at}` stored in `{module}_reviews.json` and `mock_reviews.json`. Markdown content supported.

## Exam Modules

| Key | Name | Questions |
|-----|------|-----------|
| `ziliao` | 资料分析 | 20 |
| `yanyu` | 言语理解 | 30 |
| `panduan` | 判断推理 | 35 |
| `shuliang` | 数量关系 | 15 |
| `changshi` | 常识判断 | 15 |
| `zhengzhi` | 政治理论 | 20 |
| `mock` | 套题记录 | 135 total |
