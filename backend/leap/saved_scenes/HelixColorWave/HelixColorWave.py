import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixColorWave(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).scale(2.5)
        helix.set_color(BLUE)
        self.play(FadeIn(helix))

        # Color sweep through rainbow
        colors = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK]
        for color in colors:
            self.play(helix.animate.set_color(color), run_time=0.4, rate_func=smooth)

        # Gradient sweep across submobjects
        subs = helix.submobjects if helix.submobjects else [helix]
        if len(subs) > 1:
            for i, sub in enumerate(subs):
                target_color = interpolate_color(BLUE, GREEN, i / max(len(subs) - 1, 1))
                sub.set_color(target_color)
            self.play(FadeIn(helix.copy().set_opacity(0)), run_time=0.01)  # force refresh
        
        self.wait()

        # Pulsing glow cycle
        for _ in range(2):
            self.play(helix.animate.set_opacity(0.3), run_time=0.5)
            self.play(helix.animate.set_opacity(1), run_time=0.5)

        self.wait()
