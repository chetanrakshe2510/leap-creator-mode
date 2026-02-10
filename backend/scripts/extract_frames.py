import sys
import os
import subprocess
import shutil
from pathlib import Path

def extract_frames(video_path=None, interval=2):
    """Extract frames from a video at regular intervals.
    
    Args:
        video_path: Path to the video file. Defaults to preview.mp4.
        interval: Seconds between frames. Default 2.
    """
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    FRONTEND_VIDEOS_DIR = PROJECT_ROOT / "frontend" / "public" / "videos"
    FRAMES_DIR = FRONTEND_VIDEOS_DIR / "frames"
    
    if video_path is None:
        video_path = FRONTEND_VIDEOS_DIR / "preview.mp4"
    else:
        video_path = Path(video_path)
    
    if not video_path.exists():
        print(f"Error: Video not found at {video_path}")
        sys.exit(1)
    
    # Clean and recreate frames directory
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get video duration using ffprobe
    duration_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    
    try:
        result = subprocess.run(duration_cmd, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        print(f"Video duration: {duration:.1f}s")
    except Exception as e:
        print(f"Warning: Could not get duration: {e}")
        duration = 30  # fallback
    
    # Extract frames using ffmpeg
    # fps=1/interval means 1 frame every `interval` seconds
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",  # High quality JPEG
        str(FRAMES_DIR / "frame_%03d.png"),
        "-y"  # Overwrite
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error extracting frames:")
        print(result.stderr)
        sys.exit(1)
    
    # Count and list frames
    frames = sorted(FRAMES_DIR.glob("frame_*.png"))
    print(f"\nExtracted {len(frames)} frames (every {interval}s):")
    for i, f in enumerate(frames):
        timestamp = i * interval
        print(f"  [{timestamp:>4}s] {f.name}")
    
    print(f"\nFrames saved to: {FRAMES_DIR}")
    print(f"View on host at: frontend/public/videos/frames/")
    return frames

if __name__ == "__main__":
    interval = 2
    video = None
    
    if len(sys.argv) >= 2:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            video = sys.argv[1]
    
    if len(sys.argv) >= 3:
        interval = int(sys.argv[2])
    
    extract_frames(video_path=video, interval=interval)
