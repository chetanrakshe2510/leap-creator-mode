import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np

SVG_PATH = str(Path(__file__).resolve().parent / "double-helix-svgrepo-com.svg")

class HelixSpiralDraw(Scene):
    def construct(self):
        helix = SVGMobject(SVG_PATH).set_color(BLUE).scale(2.5)

        title = Text("Scanning DNA...", font_size=32, color=GREEN).to_edge(UP)
        self.play(Write(title))

        # Draw with ShowCreation (tracing effect)
        self.play(Create(helix), run_time=4, rate_func=linear)

        # Add a glowing tracer dot that moves along the helix contour
        tracer = Dot(color=YELLOW, radius=0.12).add_updater(
            lambda m, dt: m.set_opacity(0.5 + 0.5 * np.sin(self.renderer.time * 5))
        )
        
        # Flash effect along the helix
        for sub in helix.family_members_with_points()[:10]:
            flash = ShowPassingFlash(
                sub.copy().set_color(YELLOW).set_stroke(width=5),
                time_width=0.3,
                run_time=0.3
            )
            self.play(flash)

        # Final glow
        self.play(helix.animate.set_color(GREEN), run_time=1)
        
        done_text = Text("Scan Complete", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Transform(title, done_text))
        self.wait(1)
