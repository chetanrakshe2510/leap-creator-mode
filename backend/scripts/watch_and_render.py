import sys
import time
import subprocess
import shutil
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
# Watch both templates and scene roots if needed, but for now stick to examples
TEMPLATE_DIR = BACKEND_DIR / "leap" / "templates" / "examples"
FRONTEND_PUBLIC_VIDEOS_DIR = PROJECT_ROOT / "frontend" / "public" / "videos"
OUTPUT_VIDEO_PATH = FRONTEND_PUBLIC_VIDEOS_DIR / "preview.mp4"

DEBOUNCE_SECONDS = 2.0

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
        
        try:
            # 1. Run Manim
            # manim -qm -v WARNING --disable_caching [file]
            cmd = ["manim", "-qm", "-v", "WARNING", "--disable_caching", str(filepath)]
            
            # Run from BACKEND_DIR so paths resolve correctly
            result = subprocess.run(cmd, cwd=BACKEND_DIR, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error rendering {filepath.name}:")
                # Print last 10 lines of stderr to avoid spam
                print("\n".join(result.stderr.splitlines()[-15:]))
                return

            print(f"Render success: {filepath.name}")

            # 2. Find Output Video
            # Manim structure: media/videos/[scene_name]/[resolution]/[scene_name].mp4
            # We assume the most recently modified mp4 in media/videos/module_name/720p30 is the one
            module_name = filepath.stem
            media_dir = BACKEND_DIR / "media" / "videos" / module_name / "720p30"
            
            latest_file = None
            if media_dir.exists():
                # Find newest mp4
                mp4s = list(media_dir.glob("*.mp4"))
                if mp4s:
                    latest_file = max(mp4s, key=lambda f: f.stat().st_mtime)

            if latest_file:
                print(f"Found output: {latest_file.name}")
                
                # Copy to preview
                FRONTEND_PUBLIC_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy2(latest_file, OUTPUT_VIDEO_PATH)
                print(f"Updated preview.mp4")
                
                # 3. Auto-Extract Frames (Optional)
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
                print(f"Warning: No output video found in {media_dir}")

        except Exception as e:
            print(f"Exception during render: {e}")

if __name__ == "__main__":
    print(f"Smart Watcher v2 Active.")
    print(f"Monitoring {TEMPLATE_DIR}")
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
