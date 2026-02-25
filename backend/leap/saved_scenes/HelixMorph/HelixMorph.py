import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixMorph(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).set_color(BLUE).scale(2.5)
        self.play(DrawBorderThenFill(helix), run_time=2)
        self.wait(0.5)

        # Morph into a Circle
        circle = Circle(radius=2, color=GREEN, fill_opacity=0.3)
        label1 = Text("DNA", font_size=28).next_to(helix, DOWN)
        self.play(Write(label1))
        self.wait(0.5)

        label2 = Text("Cell", font_size=28, color=GREEN).next_to(circle, DOWN)
        self.play(
            Transform(helix, circle),
            Transform(label1, label2),
            run_time=2
        )
        self.wait(0.5)

        # Morph into a Square (Protein)
        square = Square(side_length=3, color=ORANGE, fill_opacity=0.3)
        label3 = Text("Protein", font_size=28, color=ORANGE).next_to(square, DOWN)
        self.play(
            Transform(helix, square),
            Transform(label1, label3),
            run_time=2
        )
        self.wait(0.5)

        # Morph into Text
        final_text = Text("LIFE", font_size=72, color=YELLOW)
        self.play(
            Transform(helix, final_text),
            FadeOut(label1),
            run_time=2
        )
        self.wait(1)
