import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixReplication(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).scale(2.5)
        
        # Split into two path groups (backbone vs rungs)
        parts = list(helix.submobjects) if helix.submobjects else [helix]
        
        if len(parts) >= 2:
            strand_a = parts[0].set_color(BLUE)
            strand_b = parts[1].set_color(TEAL)
            combined = VGroup(strand_a, strand_b)
        else:
            strand_a = helix.copy().set_color(BLUE)
            strand_b = helix.copy().set_color(TEAL)
            combined = VGroup(strand_a, strand_b)
        
        self.play(DrawBorderThenFill(combined), run_time=2)
        self.wait(0.5)

        # Title
        title = Text("DNA Replication", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # Split apart
        self.play(
            strand_a.animate.shift(LEFT * 2),
            strand_b.animate.shift(RIGHT * 2),
            run_time=2
        )
        self.wait(0.5)

        # Build complementary strands
        new_strand_a = strand_b.copy().set_color(YELLOW).set_opacity(0).move_to(strand_a.get_center() + RIGHT * 0.3)
        new_strand_b = strand_a.copy().set_color(GREEN).set_opacity(0).move_to(strand_b.get_center() + LEFT * 0.3)

        self.play(
            new_strand_a.animate.set_opacity(1),
            new_strand_b.animate.set_opacity(1),
            run_time=2
        )

        # Labels
        label_l = Text("Original", font_size=20, color=BLUE).next_to(strand_a, DOWN)
        label_r = Text("Copy", font_size=20, color=GREEN).next_to(strand_b, DOWN)
        self.play(Write(label_l), Write(label_r))
        self.wait(2)
