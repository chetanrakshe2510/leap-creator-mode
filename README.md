# Leap: Creator Mode (Antigravity Setup)

This project runs in "Creator Mode" where the Agent writes code and a local script instantly renders it.

## How to Run

### Terminal 1: The Render Engine
This watches for new files and renders them automatically.
```bash
docker compose up -d
docker compose exec leap python -u backend/scripts/watch_and_render.py
```
*(Note: use `-u` for unbuffered output to see logs immediately)*

### Terminal 2: The Agent (Chat)
In your IDE Chat, use the "Manim Expert" system prompt.

1.  Ask the Agent to create a scene.
2.  Ensure it saves the code to: `backend/leap/templates/examples/current_scene.py`
3.  The video will appear at `frontend/public/videos/preview.mp4`.

## Troubleshooting
-   If "Service not running": Run `docker compose up -d`.
-   If video doesn't update: Check Terminal 1 for Python errors.
-   If watcher stops detecting: Restart it with the commands in Terminal 1 section.
