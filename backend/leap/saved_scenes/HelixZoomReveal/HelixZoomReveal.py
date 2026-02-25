import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixZoomReveal(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).set_color(BLUE).scale(15)  # Start zoomed way in
        self.add(helix)
        self.wait(0.5)

        # Zoom out smoothly to reveal full structure
        self.play(helix.animate.scale(2.5 / 15), run_time=3, rate_func=smooth)
        self.wait(0.5)

        # Title card fades in
        title = Text("The Double Helix", font_size=48, color=WHITE).to_edge(UP)
        subtitle = Text("Blueprint of Life", font_size=28, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)

        # Gentle float
        self.play(helix.animate.shift(UP * 0.3), run_time=1.5)
        self.play(helix.animate.shift(DOWN * 0.3), run_time=1.5)
        self.wait()
