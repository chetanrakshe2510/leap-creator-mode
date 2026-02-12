from manim import *
import numpy as np

class Part1_Unscaled(Scene):
    """Without scaling — stretched graph, tilted decision boundary."""
    def construct(self):
        title = Text("Geometric Intuition: Decision Boundary", font_size=34, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        sub = Text("Without Scaling", font_size=24, color=RED).next_to(title, DOWN, buff=0.35)
        self.play(Write(sub), run_time=0.5)

        # Feature ranges
        ranges = VGroup(
            Text("Feature 1: 0 — 10", font_size=16, color=GREEN),
            Text("Feature 2: 0 — 10,000", font_size=16, color=RED),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(sub, DOWN, buff=0.3)
        self.play(FadeIn(ranges), run_time=0.5)

        # Stretched axes — Feature 2 axis is tall, Feature 1 is short
        ax = Axes(
            x_range=[0, 12, 2], y_range=[0, 11000, 2000],
            x_length=3, y_length=4.5,
            axis_config={"include_numbers": False, "stroke_width": 1.2},
        ).shift(DOWN * 0.2 + LEFT * 0.5)
        x_lbl = Text("Feature 1", font_size=12, color=GREEN).next_to(ax.x_axis, DOWN, buff=0.1)
        y_lbl = Text("Feature 2", font_size=12, color=RED).next_to(ax.y_axis, LEFT, buff=0.1).rotate(90 * DEGREES)

        # x-axis ticks
        x_ticks = VGroup(
            Text("0", font_size=10, color=GRAY).next_to(ax.c2p(0, 0), DOWN, buff=0.08),
            Text("5", font_size=10, color=GRAY).next_to(ax.c2p(5, 0), DOWN, buff=0.08),
            Text("10", font_size=10, color=GRAY).next_to(ax.c2p(10, 0), DOWN, buff=0.08),
        )
        y_ticks = VGroup(
            Text("0", font_size=10, color=GRAY).next_to(ax.c2p(0, 0), LEFT, buff=0.08),
            Text("5k", font_size=10, color=GRAY).next_to(ax.c2p(0, 5000), LEFT, buff=0.08),
            Text("10k", font_size=10, color=GRAY).next_to(ax.c2p(0, 10000), LEFT, buff=0.08),
        )

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(x_ticks), FadeIn(y_ticks), run_time=0.8)

        # Class A data — lower-left cluster
        np.random.seed(42)
        class_a_raw = [(np.random.uniform(1, 5), np.random.uniform(1000, 4000)) for _ in range(8)]
        class_b_raw = [(np.random.uniform(5, 9), np.random.uniform(6000, 9500)) for _ in range(8)]

        dots_a = VGroup(*[Dot(ax.c2p(x, y), color=TEAL, radius=0.05) for x, y in class_a_raw])
        dots_b = VGroup(*[Dot(ax.c2p(x, y), color=ORANGE, radius=0.05) for x, y in class_b_raw])

        self.play(FadeIn(dots_a), FadeIn(dots_b), run_time=0.6)

        lbl_a = Text("Class A", font_size=12, color=TEAL).next_to(ax.c2p(2.5, 2000), LEFT, buff=0.3)
        lbl_b = Text("Class B", font_size=12, color=ORANGE).next_to(ax.c2p(7.5, 8000), RIGHT, buff=0.3)
        self.play(FadeIn(lbl_a), FadeIn(lbl_b), run_time=0.3)

        # Tilted/unnatural decision boundary — nearly horizontal because y dominates
        boundary = ax.plot(
            lambda x: 4800 + 50 * (x - 5),  # nearly flat
            x_range=[0, 11], color=YELLOW, stroke_width=2
        )
        b_lbl = Text("Decision Boundary", font_size=11, color=YELLOW).next_to(ax.c2p(9, 5100), RIGHT, buff=0.1)

        self.play(Create(boundary), FadeIn(b_lbl), run_time=0.8)

        problem = VGroup(
            Text("Graph stretched → boundary tilts unnaturally", font_size=14, color=RED),
            Text("Feature 2 dominates all distance calculations", font_size=14, color=RED),
        ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.15)
        self.play(Write(problem[0]), run_time=0.5)
        self.play(Write(problem[1]), run_time=0.5)
        self.wait(2)


class Part2_Scaled(Scene):
    """After standardization — balanced axes, natural decision boundary."""
    def construct(self):
        title = Text("Geometric Intuition: Decision Boundary", font_size=34, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        sub = Text("After Standardization", font_size=24, color=GREEN).next_to(title, DOWN, buff=0.35)
        self.play(Write(sub), run_time=0.5)

        info = Text("Both axes scaled equally → variance = 1", font_size=16, color=GREEN_B)
        info.next_to(sub, DOWN, buff=0.25)
        self.play(Write(info), run_time=0.5)

        # Balanced axes
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5, y_length=5,
            axis_config={"include_numbers": True, "font_size": 12, "stroke_width": 1.2},
        ).shift(DOWN * 0.3)
        x_lbl = MathTex(r"Z_1", font_size=16, color=GREEN).next_to(ax.x_axis, DOWN, buff=0.15)
        y_lbl = MathTex(r"Z_2", font_size=16, color=RED).next_to(ax.y_axis, LEFT, buff=0.15)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)

        # Standardized data — roughly spherical clusters
        np.random.seed(42)
        class_a_z = [(np.random.uniform(-2, -0.2), np.random.uniform(-2, -0.2)) for _ in range(8)]
        class_b_z = [(np.random.uniform(0.2, 2), np.random.uniform(0.2, 2)) for _ in range(8)]

        dots_a = VGroup(*[Dot(ax.c2p(x, y), color=TEAL, radius=0.06) for x, y in class_a_z])
        dots_b = VGroup(*[Dot(ax.c2p(x, y), color=ORANGE, radius=0.06) for x, y in class_b_z])

        self.play(FadeIn(dots_a), FadeIn(dots_b), run_time=0.6)

        lbl_a = Text("Class A", font_size=12, color=TEAL).next_to(ax.c2p(-1.5, -2.5), DOWN, buff=0.1)
        lbl_b = Text("Class B", font_size=12, color=ORANGE).next_to(ax.c2p(1.5, 2.5), UP, buff=0.1)
        self.play(FadeIn(lbl_a), FadeIn(lbl_b), run_time=0.3)

        # Natural diagonal decision boundary
        boundary = ax.plot(
            lambda x: -x,  # clean diagonal
            x_range=[-2.8, 2.8], color=YELLOW, stroke_width=2
        )
        b_lbl = Text("Decision Boundary", font_size=11, color=YELLOW).next_to(ax.c2p(2.2, -1.8), RIGHT, buff=0.1)

        self.play(Create(boundary), FadeIn(b_lbl), run_time=0.8)

        # Data cloud circle to show spherical nature
        cloud = Circle(radius=1.8, color=WHITE, stroke_width=1, stroke_opacity=0.3).move_to(ax.c2p(0, 0))
        self.play(Create(cloud), run_time=0.5)

        result = VGroup(
            Text("✓ Data cloud is roughly spherical", font_size=14, color=GREEN),
            Text("✓ Boundary reflects true separation", font_size=14, color=GREEN),
            Text("✓ Both features contribute equally", font_size=14, color=GREEN),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).to_edge(DOWN, buff=0.1)

        for r in result:
            self.play(Write(r), run_time=0.3)
        self.wait(2)


class Part3_Comparison(Scene):
    """Side-by-side summary comparison."""
    def construct(self):
        title = Text("Geometric Intuition: Decision Boundary", font_size=34, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        comp = Text("Side-by-Side Comparison", font_size=22, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(comp), run_time=0.5)

        # Left: unscaled mini plot
        ax_l = Axes(
            x_range=[0, 12, 4], y_range=[0, 11000, 4000],
            x_length=2.8, y_length=3.5,
            axis_config={"include_numbers": False, "stroke_width": 0.8},
        ).shift(LEFT * 3.5 + DOWN * 0.5)
        left_title = Text("Unscaled", font_size=14, color=RED).next_to(ax_l, UP, buff=0.1)

        np.random.seed(42)
        ca_raw = [(np.random.uniform(1, 5), np.random.uniform(1000, 4000)) for _ in range(6)]
        cb_raw = [(np.random.uniform(5, 9), np.random.uniform(6000, 9500)) for _ in range(6)]
        dots_l_a = VGroup(*[Dot(ax_l.c2p(x, y), color=TEAL, radius=0.04) for x, y in ca_raw])
        dots_l_b = VGroup(*[Dot(ax_l.c2p(x, y), color=ORANGE, radius=0.04) for x, y in cb_raw])
        bnd_l = ax_l.plot(lambda x: 4800 + 50*(x-5), x_range=[0, 11], color=YELLOW, stroke_width=1.5)

        self.play(Create(ax_l), FadeIn(left_title), FadeIn(dots_l_a), FadeIn(dots_l_b), Create(bnd_l), run_time=1)

        # Right: scaled mini plot
        ax_r = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=3.5, y_length=3.5,
            axis_config={"include_numbers": False, "stroke_width": 0.8},
        ).shift(RIGHT * 3 + DOWN * 0.5)
        right_title = Text("Standardized", font_size=14, color=GREEN).next_to(ax_r, UP, buff=0.1)

        ca_z = [(np.random.uniform(-2, -0.2), np.random.uniform(-2, -0.2)) for _ in range(6)]
        cb_z = [(np.random.uniform(0.2, 2), np.random.uniform(0.2, 2)) for _ in range(6)]
        dots_r_a = VGroup(*[Dot(ax_r.c2p(x, y), color=TEAL, radius=0.04) for x, y in ca_z])
        dots_r_b = VGroup(*[Dot(ax_r.c2p(x, y), color=ORANGE, radius=0.04) for x, y in cb_z])
        bnd_r = ax_r.plot(lambda x: -x, x_range=[-2.8, 2.8], color=YELLOW, stroke_width=1.5)
        cloud = Circle(radius=1.5, color=WHITE, stroke_width=0.8, stroke_opacity=0.2).move_to(ax_r.c2p(0, 0))

        self.play(Create(ax_r), FadeIn(right_title), FadeIn(dots_r_a), FadeIn(dots_r_b), Create(bnd_r), Create(cloud), run_time=1)

        # Arrow
        arrow = Arrow(LEFT * 0.8, RIGHT * 0.8, color=WHITE, stroke_width=2).shift(DOWN * 0.5)
        arrow_lbl = Text("Standardize", font_size=12, color=WHITE).next_to(arrow, DOWN, buff=0.08)
        self.play(GrowArrow(arrow), FadeIn(arrow_lbl), run_time=0.5)

        # Key takeaways
        takeaway = VGroup(
            Text("Stretched graph → biased boundary", font_size=14, color=RED),
            Text("Balanced graph → true geometric structure", font_size=14, color=GREEN),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.15)
        self.play(Write(takeaway[0]), run_time=0.4)
        self.play(Write(takeaway[1]), run_time=0.4)
        self.wait(2)
