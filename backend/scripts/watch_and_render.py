import sys
import time
import subprocess
import shutil
import os
from pathlib import Path
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
TEMPLATE_DIR = BACKEND_DIR / "leap" / "templates" / "examples"
FRONTEND_PUBLIC_VIDEOS_DIR = PROJECT_ROOT / "frontend" / "public" / "videos"
OUTPUT_VIDEO_PATH = FRONTEND_PUBLIC_VIDEOS_DIR / "preview.mp4"

class ManimHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        if event.is_directory:
            return
        
        filename = Path(event.src_path)
        if filename.suffix != ".py":
            return

        print(f"Detected change in {filename.name}. Rendering...")

        # Run Manim command
        # command: manim -qm -v WARNING [filename]
        try:
            # We need to run manim from the directory where the file is, or handle paths correctly.
            # Manim usually outputs to media/ directory relative to execution.
            # Let's run from the file's directory to keep it simple, or from backend root.
            # If we run from backend root:
            
            # Construct command
            cmd = ["manim", "-qm", "-v", "WARNING", str(filename)]
            
            # Execute
            result = subprocess.run(cmd, cwd=BACKEND_DIR, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error rendering {filename.name}:")
                print(result.stderr)
                return

            print(f"Rendered {filename.name} successfully.")

            # Find the output video
            # Manim structure: media/videos/[scene_name]/[resolution]/[scene_name].mp4
            # OR media/videos/[filename_without_ext]/[resolution]/[scene_name].mp4
            # We need to find the most recently created mp4 file in media/videos
            
            media_dir = BACKEND_DIR / "media" / "videos"
            if not media_dir.exists():
                print(f"Media directory not found at {media_dir}")
                return

            # Find the latest mp4 file
            latest_file = None
            latest_time = 0

            for root, dirs, files in os.walk(media_dir):
                for file in files:
                    if file.endswith(".mp4"):
                        file_path = Path(root) / file
                        # Check modification time
                        mtime = file_path.stat().st_mtime
                        if mtime > latest_time:
                            latest_time = mtime
                            latest_file = file_path

            if latest_file:
                print(f"Found output video: {latest_file}")
                
                # Ensure destination directory exists
                FRONTEND_PUBLIC_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
                
                # Move/Copy the file
                shutil.copy2(latest_file, OUTPUT_VIDEO_PATH)
                print(f"Copied to {OUTPUT_VIDEO_PATH}")
            else:
                print("No output video found.")

        except Exception as e:
            print(f"Exception during processing: {e}")

if __name__ == "__main__":
    print(f"Monitoring {TEMPLATE_DIR} for changes...")
    
    # Ensure template directory exists
    if not TEMPLATE_DIR.exists():
        print(f"Error: Directory {TEMPLATE_DIR} does not exist.")
        sys.exit(1)

    event_handler = ManimHandler()
    observer = Observer()
    observer.schedule(event_handler, str(TEMPLATE_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
