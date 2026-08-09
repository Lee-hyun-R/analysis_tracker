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

No tests, linter, formatter, or CI exist.

## Architecture

- **`app.py`** -- Flask backend. REST API + serves `templates/index.html`.
- **`main.py`** -- PyInstaller entrypoint. Resolves paths for packaged exe, overrides `DATA_DIR`, auto-opens browser, runs Flask.
- **`templates/index.html`** -- Monolithic SPA (~1600 lines) with inline JS/CSS. Uses Tailwind CSS and Chart.js from CDNs.
- **`static/`** -- Empty directory; exists only because `build.spec` bundles it.
- **`data/`** -- Flat JSON files, one per exam module (`{module}_records.json`) plus `mock_records.json`. Gitignored except `.gitkeep`.

## 题解 (Solutions)

题解以 Markdown 内容存储，通过上传本地 `.md` 文件导入，关联到具体练习记录：
- 数据文件：`{module}_solutions.json` 和 `mock_solutions.json`，位于受 `DATA_DIR` 控制的数据目录。
- 每条题解：`{id, record_id, title, content, created_at, updated_at}`。`record_id` 关联模块记录的 `practice_number`（套题为 `mock_number`），与复盘（reviews）的关联方式一致。
- API：`/api/<module>/solutions` 支持 GET/POST/PUT/DELETE（`mock` 也可用，无需单独路由前缀）；`<module>` 非法时返回 404。
- 前端：模块页与套题页的记录表格都有"题解"列按钮（写题解/查看题解），点击打开 `#solutionModal`，支持导入本地 .md 文件（`importSolutionFile()` 用 FileReader 读入）、Markdown 预览（复用 `marked`、`==高亮==` 扩展和 `.markdown-preview` 样式）、保存/删除。
- **注意**：删除练习记录不会清理其关联题解（与复盘行为一致，单用户工具可接受）；记录 ID 重排时题解可能错配，暂未处理。

## Key Quirks

- **Dual DATA_DIR resolution**: `app.py` sets `DATA_DIR` at import time; `main.py` overrides it post-import via `app_module.DATA_DIR = data_path`. This is intentional for PyInstaller path handling.
- **`main.py` changes cwd** (`os.chdir(base_path)`) so Flask finds templates when frozen. Don't remove this.
- **Port 8080 is hardcoded** in `app.py`, `main.py`, and `run.sh` -- no config mechanism.
- **`pandas` in requirements.txt is unused** -- never imported anywhere. Dead dependency.
- **IDs are re-sequenced on delete** (not stable). Fine for single-user local tool.
- **No authentication** -- API is fully open. CORS is enabled for all routes.
- **`build.spec` hiddenimports** include `engineio.async_drivers.threading` -- required for Flask-SocketIO compat even though SocketIO isn't used. Don't trim.
- **`DATA_PATH` env var** can override the data directory location (checked by `get_data_dir()` in `app.py` after `sys.frozen`).
- **`==text==` highlight syntax** in reviews: custom Marked.js extension in `index.html` renders `==text==` as `<mark>` tags. Non-obvious if editing review rendering.
- **`.gitignore` has `*.spec`** but `build.spec` is tracked (force-added). Don't assume spec files are ignored.

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
