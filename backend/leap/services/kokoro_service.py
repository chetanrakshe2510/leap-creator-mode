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

def custom_get_duration(path: str) -> float:
    return mutagen.File(path).info.length

manim_voiceover.modify_audio.get_duration = custom_get_duration
manim_voiceover.tracker.get_duration = custom_get_duration

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
