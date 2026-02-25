import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixInfoGraphic(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).set_color(BLUE_C).scale(3).shift(LEFT * 3)
        self.play(DrawBorderThenFill(helix), run_time=2)

        title = Text("DNA: Key Facts", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Data points positioned along the helix height
        facts = [
            ("3.2 billion", "base pairs in human genome"),
            ("99.9%", "identical between all humans"),
            ("6 feet", "of DNA in every cell"),
            ("2 nm", "width of the double helix"),
        ]

        labels = VGroup()
        for i, (stat, desc) in enumerate(facts):
            y_pos = 2.5 - i * 1.6
            stat_text = Text(stat, font_size=28, color=YELLOW).move_to(RIGHT * 1.5 + UP * y_pos)
            desc_text = Text(desc, font_size=18, color=GRAY).next_to(stat_text, DOWN, buff=0.15)
            connector = Line(
                helix.get_right() + UP * y_pos * 0.5,
                stat_text.get_left() + LEFT * 0.1,
                color=BLUE_C, stroke_width=2
            )
            group = VGroup(connector, stat_text, desc_text)
            labels.add(group)

        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.5) for l in labels], lag_ratio=0.4), run_time=3)
        self.wait(2)
