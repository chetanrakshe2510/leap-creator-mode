# Leap: Creator Mode (Antigravity Setup)

This project runs in "Creator Mode" where the Agent writes code and a local script instantly renders it.

## How to Run

### Terminal 1: The Render Engine
This watches for new files and renders them automatically.
```bash

docker compose up -d
cd 'e:\leap-main\leap-main'
docker compose exec leap python -u scripts/watch_and_render.py
```
*(Note: use `-u` for unbuffered output to see logs immediately)*

### Terminal 2: The Agent (Chat)
In your IDE Chat, use the "Manim Expert" system prompt.

SYSTEM PROMPT: MANIM EXPERT MODE

You are now an expert Manim Animation Engineer.

Your Workflow:

I will describe a concept (e.g., "Bubble Sort").

You will write a complete, runnable Scene class.

Action: Save the code to backend/leap/templates/examples/current_scene.py.

Coding Rules:

ALWAYS overwrite current_scene.py (this triggers my auto-renderer).

Use from manim import *.

Use Create() (not ShowCreation).

Use MathTex for equations.

Do not explain the code. Just write the file

1.  Ask the Agent to create a scene.
2.  Ensure it saves the code to: `backend/leap/templates/examples/current_scene.py`
3.  The video will appear at `frontend/public/videos/preview.mp4`.

## Saving Your Work

To save the current scene and video to a permanent folder:

```bash
docker compose exec leap python scripts/save_scene.py [YourSceneName]
```

Example:
```bash
docker compose exec leap python scripts/save_scene.py BubbleSort
```
This saves to `backend/leap/saved_scenes/BubbleSort/`.

## Reviewing & Correcting Scenes

After rendering, extract key frames for visual review before saving:

```bash
docker compose exec leap python scripts/extract_frames.py
```
*(Optional: set interval in seconds, e.g. `extract_frames.py 3` for every 3s)*

Frames are saved to `frontend/public/videos/frames/` (visible on host).

### Correction Workflow
1. **Extract** — Run `extract_frames.py` after rendering.
2. **Agent Reviews** — Agent views the frames and identifies issues.
3. **Improvement Plan** — Agent prepares a correction plan for your review.
4. **You Approve** — Review the plan and approve or request changes.
5. **Agent Fixes** — Agent updates `current_scene.py` and re-renders.
6. **Repeat** until satisfied, then **Save**.

## Troubleshooting
-   If "Service not running": Run `docker compose up -d`.
-   If video doesn't update: Check Terminal 1 for Python errors.
-   If watcher stops detecting: Restart it with the commands in Terminal 1 section.
