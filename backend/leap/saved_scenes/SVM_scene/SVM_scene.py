# LEAP_VERTICAL
from manim import *
import numpy as np

class SVMClassifier(Scene):
    def construct(self):
        # ─────────────────────────────────────────────
        # 1. Header Zone (Top 15%)
        # ─────────────────────────────────────────────
        title = Text("Support Vector Machine", font_size=42, weight=BOLD)
        subtitle = Text("How it finds the best line", font_size=30, color=BLUE_B)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        # Place roughly at y=3.2 (Frame top is 4.0)
        header.to_edge(UP, buff=0.5)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        
        # ─────────────────────────────────────────────
        # 2. Main Graph (Middle 70% - Massive Scale)
        # ─────────────────────────────────────────────
        plot_group = VGroup()
        
        # Scale: 1.5 because fitting 5.0 height in 8.0 frame with header/footer is tight.
        # X range [-2.25, 2.25].
        # Points at X=1.5 * S. 
        # If S=1.5 => X=2.25 (Edge of screen).
        # Let's go S=1.45 to be safe but maximize width.
        S = 1.45
        
        # Coordinates (Center-relative)
        blue_coords = [
            [-1.5*S, -2.0*S, 0], [-0.5*S, -1.0*S, 0], [-1.2*S, -0.5*S, 0], 
            [-0.8*S, -2.5*S, 0], [-0.5*S, -0.8*S, 0], [-1.2*S, -2.8*S, 0]
        ]
        red_coords = [
            [1.5*S, 2.0*S, 0], [0.5*S, 1.0*S, 0], [1.2*S, 0.5*S, 0],
            [0.8*S, 2.5*S, 0], [0.5*S, 0.8*S, 0], [1.2*S, 2.8*S, 0]
        ]
        
        blue_points = VGroup()
        red_points = VGroup()
        
        # Larger dots for visibility on mobile
        for p in blue_coords:
            dot = Dot(point=p, color=BLUE, radius=0.18)
            blue_points.add(dot)
            
        for p in red_coords:
            dot = Dot(point=p, color=RED, radius=0.18)
            red_points.add(dot)
            
        plot_group.add(blue_points, red_points)
        
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in blue_points], lag_ratio=0.1),
            LaggedStart(*[GrowFromCenter(d) for d in red_points], lag_ratio=0.1),
            run_time=1.5
        )
        self.wait(0.5)
        
        # ─────────────────────────────────────────────
        # 3. Separators
        # ─────────────────────────────────────────────
        
        # Optimal approximate: -45 deg (-1 slope)
        # Extends from roughly (-2.5, 2.5) to (2.5, -2.5) to cover screen width
        line1 = Line(start=[-3.0, 3.0, 0], end=[3.0, -3.0, 0], color=WHITE)
        
        # Footer Zone (Bottom 15%)
        # Bright yellow for contrast
        caption_style = {"font_size": 36, "color": YELLOW_B}
        
        problem_text = Text("Which line is best?", **caption_style)
        problem_text.to_edge(DOWN, buff=1.0)
        
        self.play(FadeIn(problem_text))
        
        # Bad lines
        line_bad1 = Line(start=[-2.5, 1.2, 0], end=[1.2, -2.5, 0], color=GRAY)
        line_bad2 = Line(start=[-1.2, 2.5, 0], end=[2.5, -1.2, 0], color=GRAY)
        
        self.play(Create(line_bad1)) 
        self.wait(0.5)
        self.play(Transform(line_bad1, line_bad2))
        self.wait(0.5)
        self.play(Transform(line_bad1, line1))
        self.wait(0.5)
        self.play(FadeOut(problem_text))
        
        # ─────────────────────────────────────────────
        # 4. Margin ("Street")
        # ─────────────────────────────────────────────
        
        # Neon Green for high contrast
        NEON_GREEN = "#39FF14"
        margin_text = Text("Maximize the Margin!", font_size=36, color=NEON_GREEN) 
        margin_text.to_edge(DOWN, buff=1.0)
        self.play(FadeIn(margin_text))
        
        street_width = ValueTracker(0.1)
        
        def get_street_lines():
            w = street_width.get_value()
            offset = w * np.array([1, 1, 0]) / np.sqrt(2)
            
            # Brighter Green Strokes
            l1 = Line(start=line1.get_start() - offset, end=line1.get_end() - offset, color=NEON_GREEN).set_stroke(opacity=0.8)
            l2 = Line(start=line1.get_start() + offset, end=line1.get_end() + offset, color=NEON_GREEN).set_stroke(opacity=0.8)
            
            # Brighter Fill
            area = Polygon(
                l1.get_start(), l1.get_end(), l2.get_end(), l2.get_start(),
                fill_color=NEON_GREEN, fill_opacity=0.2, stroke_width=0
            )
            return VGroup(l1, l2, area)
            
        street = always_redraw(get_street_lines)
        self.add(street)
        
        # Target width scaled
        target_width = 0.92 * S
        self.play(street_width.animate.set_value(target_width), run_time=2)
        self.wait(1)
        
        # ─────────────────────────────────────────────
        # 5. Support Vectors (Decoupled Labels)
        # ─────────────────────────────────────────────
        self.play(FadeOut(margin_text))
        
        sv_label = Text("Support Vectors", font_size=36, color=ORANGE)
        sv_label.to_edge(DOWN, buff=1.0)
        self.play(FadeIn(sv_label))
        
        # Target points (Indices 4 are the SVs in current list order)
        sv_blue_pt = blue_points[4]
        sv_red_pt = red_points[4]
        
        # Highlighting circles
        c1 = Circle(radius=0.3, color=ORANGE).move_to(sv_blue_pt)
        c2 = Circle(radius=0.3, color=ORANGE).move_to(sv_red_pt)
        
        # Animated indicators
        self.play(Create(c1), Create(c2))
        self.play(
            Indicate(sv_blue_pt, color=ORANGE, scale_factor=1.5), 
            Indicate(sv_red_pt, color=ORANGE, scale_factor=1.5)
        )
        self.wait(1)
        
        # ─────────────────────────────────────────────
        # 6. Conclusion
        # ─────────────────────────────────────────────
        # Use bright TEAL or BLUE_B
        final_text = Text("Safest Boundary Found!", font_size=40, color=BLUE_B)
        final_text.move_to(sv_label)
        
        self.play(
            FadeOut(sv_label),
            FadeOut(street),
            FadeIn(final_text)
        )
        self.wait(2)
