import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixExplosion(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).set_color(BLUE).scale(2.5)
        self.play(DrawBorderThenFill(helix), run_time=2)
        self.wait(0.5)

        # Get all submobject pieces
        parts = VGroup(*helix.family_members_with_points())
        original_positions = [p.get_center().copy() for p in parts]
        original_rotations = [0 for _ in parts]

        # Build up energy (quick pulse)
        self.play(helix.animate.scale(1.1).set_color(RED), run_time=0.3)
        self.play(helix.animate.scale(1/1.1).set_color(BLUE), run_time=0.2)
        self.play(helix.animate.scale(1.2).set_color(YELLOW), run_time=0.2)

        # EXPLODE outward
        np.random.seed(123)
        explode_anims = []
        for p in parts:
            direction = np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0])
            direction = direction / max(np.linalg.norm(direction), 0.001) * np.random.uniform(4, 8)
            explode_anims.append(
                p.animate.shift(direction).rotate(np.random.uniform(-2*PI, 2*PI)).set_opacity(0.3).set_color(random_color())
            )

        self.play(LaggedStart(*explode_anims, lag_ratio=0.01), run_time=1.5)
        self.wait(1)

        # REFORM — reverse the explosion
        reform_anims = []
        for p, orig_pos in zip(parts, original_positions):
            reform_anims.append(
                p.animate.move_to(orig_pos).rotate(0).set_opacity(1).set_color(BLUE)
            )

        self.play(LaggedStart(*reform_anims, lag_ratio=0.01), run_time=2, rate_func=smooth)
        
        # Final reveal
        self.play(helix.animate.set_color(GREEN), run_time=0.5)
        self.wait(1)
