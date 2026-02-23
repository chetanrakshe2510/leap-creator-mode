import sys
import time
import subprocess
import shutil
import json
import os
from pathlib import Path
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
# Watch both templates and scene roots if needed, but for now stick to examples
TEMPLATE_DIR = BACKEND_DIR / "leap" / "templates" / "examples"
FRONTEND_PUBLIC_VIDEOS_DIR = PROJECT_ROOT / "frontend" / "public" / "videos"
OUTPUT_VIDEO_PATH = FRONTEND_PUBLIC_VIDEOS_DIR / "preview.mp4"
RENDER_STATUS_PATH = FRONTEND_PUBLIC_VIDEOS_DIR / "render_status.json"

DEBOUNCE_SECONDS = 2.0


def write_render_status(status, message="", scene_name=""):
    """Write render_status.json to the frontend public directory."""
    FRONTEND_PUBLIC_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": status,
        "message": message,
        "scene": scene_name,
        "timestamp": time.time()
    }
    try:
        with open(RENDER_STATUS_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except Exception as e:
        print(f"[StatusWriter] Failed to write render_status.json: {e}")


class SmartHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = {}  # path -> timestamp
        self.pending_files = set()

    def on_modified(self, event):
        if event.is_directory:
            return
        self.handle_event(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self.handle_event(event.src_path)

    def handle_event(self, src_path):
        filename = Path(src_path).name
        
        # Ignored files
        if not filename.endswith(".py"):
            return
        if filename.startswith(("test_", "temp_", ".")):
            return

        # Mark for processing
        self.pending_files.add(src_path)
        self.last_modified[src_path] = time.time()
        print(f"Change detected in {filename}. Waiting for debounce...")

    def check_pending(self):
        """Called periodically to check if any pending files are ready to render"""
        now = time.time()
        to_process = []
        
        for path in list(self.pending_files):
            # If idle for DEBOUNCE_SECONDS
            if now - self.last_modified[path] >= DEBOUNCE_SECONDS:
                to_process.append(path)
                self.pending_files.remove(path)
                
        for path in to_process:
            self.render(Path(path))

    def render(self, filepath):
        print(f"\n[SmartWatcher] Starting render for {filepath.name}...")
        write_render_status("rendering", f"Compiling {filepath.name}...", filepath.stem)
        
        try:
            # 1. Check for Vertical Mode
            is_vertical = False
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "# LEAP_VERTICAL" in content:
                        is_vertical = True
            except Exception as e:
                print(f"Error reading file {filepath.name}: {e}")

            # 2. Run Manim
            if is_vertical:
                print("Vertical mode detected (9:16). Rendering at 1080x1920...")
                cmd = ["manim", "-v", "WARNING", "--disable_caching", "-r", "1080,1920", str(filepath)]
            else:
                # Default 720p30 (Manim -qm defaults to 720p, 16:9)
                cmd = ["manim", "-qm", "-v", "WARNING", "--disable_caching", str(filepath)]
            
            # Run from BACKEND_DIR so paths resolve correctly
            result = subprocess.run(cmd, cwd=BACKEND_DIR, capture_output=True, text=True)
            
            if result.returncode != 0:
                # --- ERROR: Write status JSON with traceback ---
                stderr_lines = result.stderr.splitlines()
                # Grab last 20 lines for a clean traceback
                error_text = "\n".join(stderr_lines[-20:])
                print(f"Error rendering {filepath.name}:")
                print(error_text)
                write_render_status("error", error_text, filepath.stem)
                return

            print(f"Render success: {filepath.name}")

            # 3. Find Output Video (ROBUST: scan entire media tree for newest mp4)
            # Manim structure: media/videos/[module_name]/[resolution]/[scene_name].mp4
            # We search the ENTIRE media/videos directory for the newest mp4
            # modified AFTER we started the render, to handle any resolution folder.
            module_name = filepath.stem
            media_module_dir = BACKEND_DIR / "media" / "videos" / module_name
            
            latest_file = None
            if media_module_dir.exists():
                # Find newest mp4 recursively, excluding partial_movie_files
                mp4s = [
                    f for f in media_module_dir.rglob("*.mp4")
                    if "partial_movie_files" not in str(f)
                ]
                if mp4s:
                    latest_file = max(mp4s, key=lambda f: f.stat().st_mtime)

            if latest_file:
                print(f"Found output: {latest_file}")
                
                # Copy to preview
                FRONTEND_PUBLIC_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy2(latest_file, OUTPUT_VIDEO_PATH)
                print(f"Updated preview.mp4")
                
                # --- SUCCESS: Write status JSON ---
                write_render_status("success", f"Rendered {latest_file.name}", filepath.stem)
                
                # 4. Auto-Extract Frames (Optional)
                print("Auto-extracting frames for review...")
                extract_script = BACKEND_DIR / "scripts" / "extract_frames.py"
                if extract_script.exists():
                    subprocess.run(
                        ["python", str(extract_script), str(latest_file)], 
                        cwd=BACKEND_DIR
                    )
                else: 
                    print("Warning: extract_frames.py not found.")
            else:
                error_msg = f"No output video found in {media_module_dir}"
                print(f"Warning: {error_msg}")
                write_render_status("error", error_msg, filepath.stem)

        except Exception as e:
            error_msg = f"Exception during render: {e}"
            print(error_msg)
            write_render_status("error", error_msg, filepath.stem)

if __name__ == "__main__":
    print(f"Smart Watcher v3 Active.")
    print(f"Monitoring {TEMPLATE_DIR}")
    print(f"Status file: {RENDER_STATUS_PATH}")
    print(f"Debounce: {DEBOUNCE_SECONDS}s")

    event_handler = SmartHandler()
    observer = Observer()
    observer.schedule(event_handler, str(TEMPLATE_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.5)
            event_handler.check_pending()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
