import os
import json
import hashlib
import requests
import mutagen
import manim_voiceover.modify_audio
from pathlib import Path
from manim_voiceover.services.base import SpeechService

# Monkeypatch manim_voiceover to support non-MP3 durations (like WAV)
import manim_voiceover.tracker
import manim
from manim_voiceover.helper import remove_bookmarks

def custom_get_duration(path: str) -> float:
    return mutagen.File(path).info.length

manim_voiceover.modify_audio.get_duration = custom_get_duration
manim_voiceover.tracker.get_duration = custom_get_duration

# Monkeypatch to capture subtitles and generate SRT automatically
_original_tracker_init = manim_voiceover.tracker.VoiceoverTracker.__init__

def _patched_tracker_init(self, scene: manim.Scene, data: dict, cache_dir: str):
    _original_tracker_init(self, scene, data, cache_dir)
    if not hasattr(scene, "_kokoro_subtitles"):
        scene._kokoro_subtitles = []
    
    clean_text = remove_bookmarks(data.get("input_text", ""))
    scene._kokoro_subtitles.append((self.start_t, self.end_t, clean_text))

manim_voiceover.tracker.VoiceoverTracker.__init__ = _patched_tracker_init

_original_scene_tear_down = manim.Scene.tear_down

def _format_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def _patched_scene_tear_down(self):
    _original_scene_tear_down(self)
    if hasattr(self, "_kokoro_subtitles") and self._kokoro_subtitles:
        srt_content = ""
        for i, (start_t, end_t, text) in enumerate(self._kokoro_subtitles, 1):
            start_str = _format_srt_time(start_t)
            end_str = _format_srt_time(end_t)
            srt_content += f"{i}\n{start_str} --> {end_str}\n{text}\n\n"
        
        try:
            movie_path = getattr(self.renderer.file_writer, "movie_file_path", None)
            if movie_path:
                srt_path = Path(movie_path).with_suffix(".srt")
                with open(srt_path, "w", encoding="utf-8") as f:
                    f.write(srt_content)
                print(f"Saved exact subtitle transcript to {srt_path}")
        except Exception as e:
            print(f"Failed to generate SRT subtitles: {e}")

manim.Scene.tear_down = _patched_scene_tear_down

class KokoroService(SpeechService):
    """
    SpeechService for Manim that communicates with a local Kokoro API server.
    """
    def __init__(
        self,
        server_url: str = "http://host.docker.internal:5000/generate",
        voice: str = "am_michael",
        speed: float = 1.0,
        **kwargs
    ):
        """
        Args:
            server_url (str): The local URL of the Kokoro FastAPI server.
            voice (str): The Kokoro voice preset to use.
            speed (float): The speed of speech.
        """
        self.server_url = server_url
        self.voice = voice
        self.speed = speed
        super().__init__(**kwargs)

    def generate_from_text(self, text: str, cache_dir: str = None, path: str = None, **kwargs) -> dict:
        """
        Generates audio from text by calling the Kokoro API server.
        """
        if cache_dir is None:
            cache_dir = self.cache_dir

        # We construct a dictionary of the input parameters to hash it later
        input_data = {
            "text": text,
            "voice": kwargs.get("voice", self.voice),
            "speed": kwargs.get("speed", self.speed),
        }

        # Create a deterministic filename based on the input text and parameters
        input_hash = hashlib.sha256(json.dumps(input_data, sort_keys=True).encode("utf-8")).hexdigest()
        
        file_extension = ".wav"
        if path is None:
            audio_filename = input_hash + file_extension
            full_path = os.path.join(cache_dir, audio_filename)
            original_audio_return = audio_filename
        else:
            full_path = path
            original_audio_return = path

        # Check if the audio is already cached, return it directly if so
        if os.path.exists(full_path):
            return {"original_audio": original_audio_return, "json_dict": input_data}

        # Ensure cache directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Send request to local Kokoro API
        try:
            response = requests.post(self.server_url, json=input_data, timeout=300)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to Kokoro API Server at {self.server_url}. Is it running? Error: {e}")

        # Save downloaded audio to file
        with open(full_path, 'wb') as f:
            f.write(response.content)

        return {"original_audio": original_audio_return, "json_dict": input_data}
