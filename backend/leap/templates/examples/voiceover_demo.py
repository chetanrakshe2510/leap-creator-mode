from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
# form manim_voiceover.services.gtts import GTTSService # If installed

# Option A: VoiceoverScene (Automatic Sync)
# This class automatically pauses the video to match the audio length.
# If the animation finishes early, it waits.
# If the audio finishes early, it proceeds.

class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        # 1. Setup the Service
        # RecorderService lets you record your own voice as the video plays.
        # You can also use OpenAI, ElevenLabs, or gTTS services here.
        self.set_speech_service(RecorderService(trim_silence=True))

        circle = Circle()
        square = Square()

        # 2. Sync Animation with Voice
        # The 'with' block ensures the scene waits for the audio to finish
        with self.voiceover(text="First, we draw a circle on the screen.") as tracker:
            self.play(Create(circle), run_time=tracker.duration) 
            # Note: tracker.duration is estimated or determined by the audio

        with self.voiceover(text="Now, we transform it into a square. Notice how the video waits for me to finish speaking.") as tracker:
            self.play(Transform(circle, square))

        with self.voiceover(text="Finally, we fade everything out. This method ensures your video is never too short for your story.") as tracker:
            self.play(FadeOut(circle))
