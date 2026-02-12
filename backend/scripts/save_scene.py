import sys
import os
import shutil
from pathlib import Path

def save_scene(scene_name, source_file=None):
    # Configuration
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    BACKEND_DIR = PROJECT_ROOT / "backend"
    TEMPLATE_DIR = BACKEND_DIR / "leap" / "templates" / "examples"
    SCENES_DIR = BACKEND_DIR / "leap" / "scenes"
    SAVED_SCENES_DIR = BACKEND_DIR / "leap" / "saved_scenes"
    
    FRONTEND_VIDEOS_DIR = PROJECT_ROOT / "frontend" / "public" / "videos"
    
    # 1. Determine Source File
    current_scene_file = None
    
    if source_file:
         # Try to resolve provided path
        candidates = [
            Path(source_file),
            BACKEND_DIR / source_file,
            SCENES_DIR / source_file,
            TEMPLATE_DIR / source_file
        ]
        for c in candidates:
            if c.exists():
                current_scene_file = c
                break
    else:
        # Default behavior: check current_scene.py
        current_scene_file = TEMPLATE_DIR / "current_scene.py"
        
    if not current_scene_file or not current_scene_file.exists():
        print(f"Error: Source file not found. Checked: {source_file} and defaults.")
        sys.exit(1)

    print(f"Saving scene '{scene_name}' from {current_scene_file}...")

    # 2. Find Preview Video
    # We need to find where the video was rendered. 
    # Usually it's in media/videos/[module_name]/720p30/[SceneName].mp4
    # OR if it was the last rendered video, it might be at frontend/public/videos/preview.mp4
    
    # Check for specific video file first (more reliable)
    module_name = current_scene_file.stem
    video_path = BACKEND_DIR / "media" / "videos" / module_name / "720p30" / f"{scene_name}.mp4"
    
    # Fallback to preview.mp4 if specific file not found
    if not video_path.exists():
        video_path = FRONTEND_VIDEOS_DIR / "preview.mp4"
        
    if not video_path.exists():
        print(f"Warning: Video not found at {video_path}. Saving only code.")

    # 3. Create Destination
    dest_dir = SAVED_SCENES_DIR / scene_name
    if dest_dir.exists():
        print(f"Warning: Directory {dest_dir} already exists. Overwriting...")
    else:
        dest_dir.mkdir(parents=True, exist_ok=True)
        
    # 4. Copy Files
    # Copy code
    dest_code = dest_dir / f"{scene_name}.py"
    shutil.copy2(current_scene_file, dest_code)
    print(f"Saved code to: {dest_code}")
    
    # Copy video if exists
    if video_path.exists():
        dest_video = dest_dir / f"{scene_name}.mp4"
        shutil.copy2(video_path, dest_video)
        print(f"Saved video to: {dest_video}")
        
    # 5. Cleanup review frames
    FRAMES_DIR = FRONTEND_VIDEOS_DIR / "frames"
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
        print("Cleaned up review frames.")
        
    print(f"\nSuccess! Scene '{scene_name}' saved.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/save_scene.py <scene_name> [source_file]")
        print("Example: python scripts/save_scene.py MyScene")
        print("Example: python scripts/save_scene.py MyScene backend/experiments.py")
        sys.exit(1)
        
    scene_name = sys.argv[1]
    source_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    save_scene(scene_name, source_file)
