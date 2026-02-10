import sys
import os
import shutil
from pathlib import Path

def save_scene(scene_name):
    # Configuration
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    BACKEND_DIR = PROJECT_ROOT / "backend"
    TEMPLATE_DIR = BACKEND_DIR / "leap" / "templates" / "examples"
    SAVED_SCENES_DIR = BACKEND_DIR / "leap" / "saved_scenes"
    
    # Source paths
    CURRENT_SCENE_FILE = TEMPLATE_DIR / "current_scene.py"
    # Preview video is in frontend public folder for the user to see, 
    # but inside the container (where this script runs), it might be mapped differently 
    # depending on volumes. 
    # However, standard practice in this repo seems to be:
    # Dockerfile: COPY --from=frontend-builder /app/frontend/dist/ /app/frontend/dist/
    # docker-compose: ./frontend/public/videos:/app/frontend/public/videos
    # So /app/frontend/public/videos/preview.mp4 should be accessible if volumes are correct.
    
    FRONTEND_VIDEOS_DIR = PROJECT_ROOT / "frontend" / "public" / "videos"
    CURRENT_VIDEO_FILE = FRONTEND_VIDEOS_DIR / "preview.mp4"

    # 1. Validation
    if not CURRENT_SCENE_FILE.exists():
        print(f"Error: Current scene file not found at {CURRENT_SCENE_FILE}")
        sys.exit(1)
        
    if not CURRENT_VIDEO_FILE.exists():
        print(f"Warning: Preview video not found at {CURRENT_VIDEO_FILE}. Saving only code.")
    
    # 2. Create Destination
    dest_dir = SAVED_SCENES_DIR / scene_name
    if dest_dir.exists():
        print(f"Warning: Directory {dest_dir} already exists. Overwriting...")
    else:
        dest_dir.mkdir(parents=True, exist_ok=True)
        
    # 3. Copy Files
    # Copy code
    dest_code = dest_dir / f"{scene_name}.py"
    shutil.copy2(CURRENT_SCENE_FILE, dest_code)
    print(f"Saved code to: {dest_code}")
    
    # Copy video if exists
    if CURRENT_VIDEO_FILE.exists():
        dest_video = dest_dir / f"{scene_name}.mp4"
        shutil.copy2(CURRENT_VIDEO_FILE, dest_video)
        print(f"Saved video to: {dest_video}")
        
    # 4. Cleanup review frames
    FRAMES_DIR = FRONTEND_VIDEOS_DIR / "frames"
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
        print("Cleaned up review frames.")
        
    print(f"\nSuccess! Scene '{scene_name}' saved.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/save_scene.py [scene_name]")
        print("Example: python scripts/save_scene.py MyAwesomeScene")
        sys.exit(1)
        
    scene_name = sys.argv[1]
    # Sanitize name usually good practice, but for dev tool let's keep it simple
    save_scene(scene_name)
