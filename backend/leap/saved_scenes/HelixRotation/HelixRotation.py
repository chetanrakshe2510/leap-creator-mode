import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixRotation(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).set_color(BLUE).scale(2.5)
        self.play(FadeIn(helix))

        # Simulate 3D rotation by stretching X axis back and forth
        for _ in range(3):
            self.play(helix.animate.stretch(0.01, 0), run_time=0.5, rate_func=smooth)
            self.play(helix.animate.stretch(100, 0), run_time=0.5, rate_func=smooth)
            self.play(helix.animate.stretch(0.01, 0), run_time=0.5, rate_func=smooth)
            helix_flipped = helix.copy().flip(UP)
            self.play(Transform(helix, helix_flipped), run_time=0.01)
            self.play(helix.animate.stretch(100, 0), run_time=0.5, rate_func=smooth)

        self.wait()
