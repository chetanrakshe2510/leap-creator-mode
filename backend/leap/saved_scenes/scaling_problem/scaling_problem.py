from manim import *
import numpy as np

class UnscaledDataConfusion(Scene):
    def construct(self):
        # ============================================================
        # PART 1: THE PROBLEM — Two Features, Wildly Different Scales
        # ============================================================
        title = Text("Why Unscaled Data Confuses ML", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)

        # Show two features
        feat1_label = Text("Age", font_size=22, color=GREEN).shift(LEFT * 3 + UP * 1.5)
        feat1_range = Text("0 — 100", font_size=18, color=GREEN_B).next_to(feat1_label, DOWN, buff=0.2)
        feat1_bar = Rectangle(width=2, height=0.4, color=GREEN, fill_opacity=0.3).next_to(feat1_range, DOWN, buff=0.3)

        feat2_label = Text("Salary", font_size=22, color=RED).shift(RIGHT * 2 + UP * 1.5)
        feat2_range = Text("0 — 100,000", font_size=18, color=RED_B).next_to(feat2_label, DOWN, buff=0.2)
        feat2_bar = Rectangle(width=5, height=0.4, color=RED, fill_opacity=0.3).next_to(feat2_range, DOWN, buff=0.3)

        self.play(
            FadeIn(feat1_label), FadeIn(feat1_range), Create(feat1_bar),
            FadeIn(feat2_label), FadeIn(feat2_range), Create(feat2_bar),
            run_time=1.5
        )
        self.wait(1)

        # Insight text
        insight1 = Text("Salary is 1000x larger than Age!", font_size=20, color=YELLOW)
        insight1.shift(DOWN * 2)
        self.play(Write(insight1), run_time=1)
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            feat1_label, feat1_range, feat1_bar,
            feat2_label, feat2_range, feat2_bar, insight1
        )))

        # ============================================================
        # PART 2: DISTANCE IS HIJACKED
        # ============================================================
        sub2 = Text("Distance Calculation is Hijacked", font_size=28, color=YELLOW)
        sub2.next_to(title, DOWN, buff=0.4)
        self.play(Write(sub2), run_time=1)

        # Show two data points
        ax_dist = Axes(
            x_range=[0, 110, 20], y_range=[0, 110000, 20000],
            x_length=5, y_length=3.5,
            axis_config={"include_numbers": False, "stroke_width": 1.5},
        ).shift(DOWN * 0.8)

        x_lab = Text("Age", font_size=14, color=GREEN).next_to(ax_dist.x_axis, DOWN, buff=0.15)
        y_lab = Text("Salary", font_size=14, color=RED).next_to(ax_dist.y_axis, LEFT, buff=0.15).rotate(90 * DEGREES)

        p1_coords = ax_dist.c2p(25, 30000)
        p2_coords = ax_dist.c2p(30, 80000)

        dot1 = Dot(p1_coords, color=BLUE, radius=0.08)
        dot2 = Dot(p2_coords, color=PURPLE, radius=0.08)
        lbl1 = Text("Alice (25, 30k)", font_size=12, color=BLUE_B).next_to(dot1, DOWN + LEFT, buff=0.1)
        lbl2 = Text("Bob (30, 80k)", font_size=12, color=PURPLE_B).next_to(dot2, UP + RIGHT, buff=0.1)

        self.play(Create(ax_dist), FadeIn(x_lab), FadeIn(y_lab), run_time=1)
        self.play(FadeIn(dot1), FadeIn(lbl1), FadeIn(dot2), FadeIn(lbl2), run_time=0.8)

        # Draw distance line
        dist_line = DashedLine(p1_coords, p2_coords, color=ORANGE, stroke_width=2)
        self.play(Create(dist_line), run_time=0.8)

        # Show distance formula
        dist_formula = MathTex(
            r"d = \sqrt{(30-25)^2 + (80000-30000)^2}",
            font_size=24, color=ORANGE
        ).shift(DOWN * 3)
        self.play(Write(dist_formula), run_time=1)
        self.wait(0.5)

        # Highlight the domination
        dist_result = MathTex(
            r"= \sqrt{\underbrace{25}_{\text{Age}} + \underbrace{2{,}500{,}000{,}000}_{\text{Salary}}}",
            font_size=24, color=ORANGE
        ).shift(DOWN * 3)
        self.play(Transform(dist_formula, dist_result), run_time=1)
        self.wait(1)

        domination = Text("Salary completely dominates the distance!", font_size=18, color=RED)
        domination.next_to(dist_result, DOWN, buff=0.2)
        self.play(Write(domination), run_time=1)
        self.wait(2)

        self.play(FadeOut(VGroup(
            ax_dist, x_lab, y_lab, dot1, dot2, lbl1, lbl2,
            dist_line, dist_formula, domination, sub2
        )))

        # ============================================================
        # PART 3: GRADIENT DESCENT — Elongated vs Circular Contours
        # ============================================================
        sub3 = Text("Gradient Descent Struggles", font_size=28, color=YELLOW)
        sub3.next_to(title, DOWN, buff=0.4)
        self.play(Write(sub3), run_time=1)

        # LEFT: Unscaled (elongated ellipse)
        left_label = Text("Unscaled", font_size=18, color=RED).shift(LEFT * 3.2 + UP * 1.2)

        # Draw elongated contour ellipses
        ellipses_left = VGroup()
        for i, s in enumerate([0.3, 0.6, 0.9, 1.2]):
            e = Ellipse(width=s * 0.6, height=s * 3, color=RED, stroke_width=1.2, stroke_opacity=0.6 - i * 0.1)
            e.shift(LEFT * 3.2 + DOWN * 0.8)
            ellipses_left.add(e)

        # Zigzag gradient path (inefficient)
        zigzag_points = [
            LEFT * 3.2 + UP * 0.6,
            LEFT * 3.5 + DOWN * 0.2,
            LEFT * 2.9 + DOWN * 0.5,
            LEFT * 3.3 + DOWN * 0.7,
            LEFT * 3.1 + DOWN * 0.8,
            LEFT * 3.2 + DOWN * 0.85,
        ]
        zigzag = VMobject(color=YELLOW, stroke_width=2)
        zigzag.set_points_as_corners(zigzag_points)

        start_dot_l = Dot(zigzag_points[0], color=YELLOW, radius=0.06)
        end_dot_l = Dot(zigzag_points[-1], color=GREEN, radius=0.06)

        self.play(FadeIn(left_label), *[Create(e) for e in ellipses_left], run_time=1)
        self.play(FadeIn(start_dot_l), run_time=0.3)
        self.play(Create(zigzag), run_time=2)
        self.play(FadeIn(end_dot_l), run_time=0.3)

        slow_label = Text("Slow zigzag!", font_size=14, color=RED).next_to(ellipses_left, DOWN, buff=0.3)
        self.play(Write(slow_label), run_time=0.5)

        # RIGHT: Scaled (circular contours)
        right_label = Text("Scaled", font_size=18, color=GREEN).shift(RIGHT * 3.2 + UP * 1.2)

        circles_right = VGroup()
        for i, r in enumerate([0.3, 0.6, 0.9, 1.2]):
            c = Circle(radius=r, color=GREEN, stroke_width=1.2, stroke_opacity=0.6 - i * 0.1)
            c.shift(RIGHT * 3.2 + DOWN * 0.8)
            circles_right.add(c)

        # Smooth direct path (efficient)
        smooth_points = [
            RIGHT * 3.2 + UP * 0.4,
            RIGHT * 3.2 + DOWN * 0.1,
            RIGHT * 3.2 + DOWN * 0.5,
            RIGHT * 3.2 + DOWN * 0.8,
        ]
        smooth = VMobject(color=YELLOW, stroke_width=2)
        smooth.set_points_as_corners(smooth_points)

        start_dot_r = Dot(smooth_points[0], color=YELLOW, radius=0.06)
        end_dot_r = Dot(smooth_points[-1], color=GREEN, radius=0.06)

        self.play(FadeIn(right_label), *[Create(c) for c in circles_right], run_time=1)
        self.play(FadeIn(start_dot_r), run_time=0.3)
        self.play(Create(smooth), run_time=1)
        self.play(FadeIn(end_dot_r), run_time=0.3)

        fast_label = Text("Direct path!", font_size=14, color=GREEN).next_to(circles_right, DOWN, buff=0.3)
        self.play(Write(fast_label), run_time=0.5)
        self.wait(2)

        self.play(FadeOut(VGroup(
            left_label, ellipses_left, zigzag, start_dot_l, end_dot_l, slow_label,
            right_label, circles_right, smooth, start_dot_r, end_dot_r, fast_label, sub3
        )))

        # ============================================================
        # PART 4: THE FIX — Scale Your Features
        # ============================================================
        sub4 = Text("The Fix: Scale Your Features", font_size=28, color=GREEN)
        sub4.next_to(title, DOWN, buff=0.4)
        self.play(Write(sub4), run_time=1)

        methods = VGroup(
            Text("Min-Max Scaling", font_size=20, color=TEAL),
            MathTex(r"x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}", font_size=28, color=TEAL_B),
            Text("maps to [0, 1]", font_size=16, color=GRAY),
        ).arrange(DOWN, buff=0.15).shift(LEFT * 3 + DOWN * 0.5)

        methods2 = VGroup(
            Text("Standardization", font_size=20, color=GOLD),
            MathTex(r"x' = \frac{x - \mu}{\sigma}", font_size=28, color=GOLD_B),
            Text("maps to mean=0, std=1", font_size=16, color=GRAY),
        ).arrange(DOWN, buff=0.15).shift(RIGHT * 3 + DOWN * 0.5)

        div_line = DashedLine(UP * 0.5, DOWN * 2.5, color=GRAY, stroke_width=1).shift(DOWN * 0.2)

        self.play(Create(div_line), run_time=0.5)
        self.play(FadeIn(methods), run_time=1)
        self.play(FadeIn(methods2), run_time=1)
        self.wait(1)

        takeaway = Text("Every feature gets an equal voice!", font_size=22, color=YELLOW)
        takeaway.to_edge(DOWN, buff=0.4)
        self.play(Write(takeaway), run_time=1)
        self.wait(2)
