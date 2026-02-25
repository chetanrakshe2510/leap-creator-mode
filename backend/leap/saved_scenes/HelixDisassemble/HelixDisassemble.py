import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixDisassemble(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).set_color(BLUE).scale(2.5)
        self.play(DrawBorderThenFill(helix), run_time=2)
        self.wait(0.5)

        title = Text("Disassemble & Reassemble", font_size=32).to_edge(UP)
        self.play(Write(title))

        # Save original positions
        parts = VGroup(*helix.family_members_with_points())
        original_positions = [p.get_center() for p in parts]

        # Scatter randomly
        np.random.seed(42)
        scatter_anims = []
        for p in parts:
            target = np.array([np.random.uniform(-6, 6), np.random.uniform(-3.5, 3.5), 0])
            scatter_anims.append(p.animate.move_to(target).set_color(random_color()).rotate(np.random.uniform(-PI, PI)))

        self.play(LaggedStart(*scatter_anims, lag_ratio=0.02), run_time=2)
        self.wait(1)

        # Reassemble
        reassemble_anims = []
        for p, orig_pos in zip(parts, original_positions):
            reassemble_anims.append(p.animate.move_to(orig_pos).set_color(BLUE).rotate_about_origin(0))

        self.play(LaggedStart(*reassemble_anims, lag_ratio=0.02), run_time=2)
        self.wait(1)
