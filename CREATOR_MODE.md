# Leap: Creator Mode

This project runs in **Creator Mode** — the Agent writes Manim scene code and a local Docker pipeline renders, verifies, and saves it automatically.

---

## Quick Start

### Terminal 1: Start the Render Engine
```bash
docker compose up -d
cd 'e:\leap-main\leap-main'
docker compose exec leap python -u scripts/watch_and_render.py
```

> **Smart Watcher v2** — Debounces file changes (2s), auto-extracts review frames, and ignores `test_`/`temp_` files.

### Terminal 2: The Agent (IDE Chat)

Paste this system prompt into your IDE chat:

> **MANIM EXPERT MODE**
>
> You are an expert Manim Animation Engineer.
> - I describe a concept → you write a complete, runnable `Scene` class.
> - Save code to `backend/leap/templates/examples/current_scene.py` (triggers auto-render).
> - Use `from manim import *`, `Create()` (not `ShowCreation`), `MathTex` for equations.
> - Do not explain the code. Just write the file.

### Workflow
1. Ask the Agent to create a scene.
2. Code is saved to `backend/leap/templates/examples/current_scene.py`.
3. Smart Watcher renders it and extracts frames automatically.
4. Video appears at `frontend/public/videos/preview.mp4`.
5. Frames appear at `frontend/public/videos/frames/` for review.

---

## Tools Reference

### Save a Scene
Saves the scene code + rendered video to a permanent folder.

```bash
# From default current_scene.py
docker compose exec leap python scripts/save_scene.py <SceneName>

# From a custom source file
docker compose exec leap python scripts/save_scene.py <SceneName> <source_file>
```

**Example:**
```bash
docker compose exec leap python scripts/save_scene.py BubbleSort
docker compose exec leap python scripts/save_scene.py BeamEquilibrium beam_scene_final.py
```
Saves to → `backend/leap/saved_scenes/<SceneName>/`

---

### Render Large Scenes (Multi-Part Pipeline)
If a scene crashes with `ParseError` (too many objects for Docker), split it into multiple scene classes and use:

```bash
docker compose exec leap python scripts/render_chain.py <scene_file> [OutputName]
```

**Example:**
```bash
docker compose exec leap python scripts/render_chain.py beam_scene_final.py BeamEquilibrium
```

**How it works:**
1. Auto-detects all `Scene` classes in the file
2. Renders each sequentially (fresh process per scene — avoids resource limits)
3. Concatenates into a single `OutputName.mp4` via ffmpeg
4. Copies final video to `frontend/public/videos/preview.mp4`

---

### Extract Review Frames (Manual)
The Smart Watcher does this automatically, but you can also run it manually:

```bash
docker compose exec leap python scripts/extract_frames.py [video_path] [interval_seconds]
```

Defaults: `preview.mp4`, every `2s`. Frames saved to `frontend/public/videos/frames/`.

---

## Review & Correction Workflow

```
Write Scene → Render → Extract Frames → Agent Reviews → Fix → Repeat → Save
```

1. **Render** — Smart Watcher auto-renders on file save.
2. **Extract** — Frames are auto-extracted (or run `extract_frames.py` manually).
3. **Agent Reviews** — Agent views frames and identifies issues.
4. **You Approve** — Review the agent's correction plan.
5. **Agent Fixes** — Agent updates the scene and re-renders.
6. **Save** — When satisfied, run `save_scene.py`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Service not running" | `docker compose up -d` |
| Video doesn't update | Check Terminal 1 for Python errors |
| Watcher stops detecting | Restart with Terminal 1 commands |
| `ParseError: no element found` | Scene too large — split into parts, use `render_chain.py` |
| Frames not appearing | Run `extract_frames.py` manually |
