import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixPulse(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).set_color(BLUE).scale(2.5)
        
        # Glow ring behind helix
        glow = Circle(radius=2.5, color=BLUE, fill_opacity=0.1, stroke_opacity=0.3)
        
        self.play(FadeIn(glow), DrawBorderThenFill(helix), run_time=2)

        title = Text("Heartbeat Pulse", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Pulsing heartbeat animation
        for _ in range(4):
            self.play(
                helix.animate.scale(1.15).set_color(TEAL),
                glow.animate.scale(1.3).set_fill(opacity=0.3),
                run_time=0.3, rate_func=rush_into
            )
            self.play(
                helix.animate.scale(1/1.15).set_color(BLUE),
                glow.animate.scale(1/1.3).set_fill(opacity=0.1),
                run_time=0.5, rate_func=rush_from
            )
            self.wait(0.3)

        self.wait()
