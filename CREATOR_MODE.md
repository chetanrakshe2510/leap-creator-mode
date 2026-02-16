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
>
> ### 1. Analyze Request & Choose Mode
> - **Standard (16:9)**: Default. Best for lectures/YouTube.
> - **Vertical (9:16)**: Use if user asks for "Shorts", "TikTok", "Reels", or "Phone".
>
> ### 2. Write Code
> - Save to `backend/leap/templates/examples/current_scene.py`.
> - Use `from manim import *`, `Create()`, `MathTex`.
> - **Do not explain.** Just write the file.
>
> ### 3. Mode-Specific Rules
> **Option A: Standard Mode (16:9)**
> - Frame: 14.2 x 8.0
> - No special flags needed.
>
> **Option B: Vertical Mode (9:16)**
> - **REQUIRED:** Add `# LEAP_VERTICAL` as the very first line.
> - Frame: 4.5 x 8.0 (Narrow!)
> - **Golden Rules (Prevent Overlaps):**
>   1. **No Absolute Positioning:** NEVER use `move_to([0, 2.5, 0])`. Use `to_edge(UP, buff=0.5)` to pin to margins.
>   2. **Group & Arrange:** Use `VGroup(item1, item2).arrange(DOWN, buff=0.5)` for automatic layout.
>   3. **Explicit Buffs:** Always define `buff=0.2` or `0.3` when using `next_to()`.
>   4. **Wrap Content:** Break long equations/text into multiple lines. Width is only 4.5 units!
> - **Animation Flow (Space Management):**
>   - **The "Scroll" Technique:** `self.camera.frame.animate.shift(DOWN * 5)` to extend the canvas downward.
>   - **Aggressive Clearing:** Use `FadeOut()` or `Transform()` frequently to clear screen space.
>
> **Option C: Hybrid (Voiceover) Mode**
> - **REQUIRED:** Inherit from `VoiceoverScene`.
> - **REQUIRED:** Use `gTTS` service for placeholder audio.
> - **Logic:**
>   - NEVER use `self.wait(X)`.
>   - Use `with self.voiceover(text="...") as tracker:`
>   - **"Living Plots":** Visuals must NEVER freeze. Use `always_redraw()` + `ValueTracker` so graphs animate while waiting for audio.
>   - Use `tracker.duration` to pace animations: `self.play(..., run_time=tracker.duration)`.
>
> **Option D: Two-Stage Workflow (Recommended)**
> 1.  **Stage 1: Visual Sketch**
>     -   Write standard Manim code using `self.wait(2)`.
>     -   Focus on layout, colors, and animation flow.
>     -   **Goal:** Fast iteration, verify visuals.
> 2.  **Stage 2: Voice Sync**
>     -   Refactor to `VoiceoverScene` + `gTTS`.
>     -   Replace `wait()` with `voiceover()`.
>     -   Ensure animations loop ("Living Plots").
>     -   **Goal:** Perfect timing, ready for final audio.

### Workflow
1. Ask the Agent to create a scene (specify Stage 1 or 2).
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

---

## Video Modes

### 1. Standard Mode (16:9)
**Default.** Renders at 1280x720 (720p). Best for YouTube/Desktop.
- Just write your scene normally.
- Coordinate system: Frame Height = 8.0, Frame Width = 14.2.

### 2. Vertical Mode (9:16)
**TikTok/Reels/Shorts.** Renders at 1080x1920.

Add this comment to the VERY TOP of your Python file to trigger it:
```python
# LEAP_VERTICAL
from manim import *
...
```

- **Frame Height:** Remains `8.0`.
- **Frame Width:** Becomes `4.5` (narrower!).
- **Design Tips:**
  - Use `to_edge(UP)` / `to_edge(DOWN)`.
  - Keep content within `x_range=[-2.25, 2.25]`.
  - Use smaller font sizes (e.g., 32-40) for text to fit.



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
