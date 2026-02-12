import sys
import os
import subprocess
import re
from pathlib import Path
import shutil

def render_chain(scene_file, output_name="FinalVideo"):
    """
    Renders all scenes in a file sequentially (to avoid resource limits)
    and concatenates them into a single video.
    """
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    BACKEND_DIR = PROJECT_ROOT / "backend"
    
    # In Docker, we are at /app (which is PROJECT_ROOT).
    # Inputs might be 'backend/beam_scene.py' or just 'beam_scene.py' if we are in backend dir.
    
    possible_paths = [
        Path(scene_file),                        # As provided
        Path("/app") / scene_file,               # Absolute Docker path
        BACKEND_DIR / scene_file,                # Relative to backend
        PROJECT_ROOT / scene_file                # Relative to root
    ]
    
    final_path = None
    for p in possible_paths:
        if p.exists():
            final_path = p
            break
            
    if not final_path:
        # Debugging aid
        print(f"Error: Scene file not found.")
        print(f"Current WD: {os.getcwd()}")
        print(f"Checked: {[str(p) for p in possible_paths]}")
        sys.exit(1)
        
    scene_path = final_path.resolve()
    print(f"Resolved scene file: {scene_path}")

    # 1. Detect Scene Classes
    with open(scene_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find classes inheriting from Scene
    # Matches: class SceneName(Scene): or class SceneName(ThreeDScene):
    scene_classes = re.findall(r'class\s+(\w+)\s*\(.*Scene.*\):', content)
    
    if not scene_classes:
        print("No Scene classes found in file.")
        sys.exit(1)
        
    print(f"Found {len(scene_classes)} scenes to render: {scene_classes}")

    # 2. Render Sequentially
    rendered_videos = []
    
    for scene_name in scene_classes:
        print(f"\n[render_chain] Rendering {scene_name}...")
        
        # Run manim in a subprocess to ensure fresh memory/resources for each scene
        cmd = [
            "manim", "-qm", 
            "--disable_caching", # Optional: ensure fresh render
            str(scene_path), 
            scene_name
        ]
        
        ret = subprocess.run(cmd, cwd=BACKEND_DIR)
        
        if ret.returncode != 0:
            print(f"Error rendering {scene_name}. Aborting chain.")
            sys.exit(1)
            
        # Find the output video
        # Manim default output: media/videos/{module_name}/720p30/{SceneName}.mp4
        module_name = scene_path.stem
        video_path = BACKEND_DIR / "media" / "videos" / module_name / "720p30" / f"{scene_name}.mp4"
        
        if video_path.exists():
            rendered_videos.append(video_path)
            print(f"Success: {video_path}")
        else:
            print(f"Error: Expected output video not found at {video_path}")
            sys.exit(1)

    # 3. Concatenate Videos
    if not rendered_videos:
        print("No videos rendered.")
        sys.exit(0)
        
    if len(rendered_videos) == 1:
        print("Only one scene rendered. No concatenation needed.")
        return

    print(f"\n[render_chain] Concatenating {len(rendered_videos)} videos...")
    
    # Create input file for ffmpeg concat demuxer
    concat_list_path = BACKEND_DIR / "temp_concat_list.txt"
    with open(concat_list_path, 'w') as f:
        for v in rendered_videos:
            # ffmpeg requires paths to be escaped - simple version for now
            # f.write(f"file '{v.absolute()}'\n")
            f.write(f"file '{str(v.absolute()).replace(os.sep, '/')}'\n")
            
    output_path = BACKEND_DIR / "media" / "videos" / scene_path.stem / "720p30" / f"{output_name}.mp4"
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # ffmpeg command
    # -f concat -safe 0 -i list.txt -c copy output.mp4
    cmd_concat = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy", "-y",
        str(output_path)
    ]
    
    ret = subprocess.run(cmd_concat, capture_output=True)
    
    # cleanup temp file
    if concat_list_path.exists():
        concat_list_path.unlink()
        
    if ret.returncode == 0:
        print(f"\nSuccessfully created final chain video:\n{output_path}")
        
        # Copy to frontend for preview if requested
        # PROJECT_ROOT is defined at start of function
        frontend_preview = PROJECT_ROOT / "frontend" / "public" / "videos" / "preview.mp4"
        try:
            shutil.copy2(output_path, frontend_preview)
            print(f"Copied to preview: {frontend_preview}")
        except Exception as e:
            print(f"Warning: Could not copy to preview: {e}")
    else:
        print("Error concatenating videos:")
        print(ret.stderr.decode())
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/render_chain.py <scene_file> [output_name]")
        sys.exit(1)
        
    scene_file = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else "FinalVideo"
    
    render_chain(scene_file, output_name)
