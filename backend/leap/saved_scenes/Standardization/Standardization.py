from manim import *
import numpy as np

class Part1_Problem(Scene):
    """What problem does standardization solve?"""
    def construct(self):
        title = Text("Standardization", font_size=40, color=BLUE)
        subtitle = Text("(Z-Score Scaling)", font_size=24, color=BLUE_B).next_to(title, DOWN, buff=0.15)
        VGroup(title, subtitle).to_edge(UP, buff=0.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1)

        q = Text("What problem does it solve?", font_size=24, color=YELLOW).next_to(subtitle, DOWN, buff=0.4)
        self.play(Write(q), run_time=0.7)

        # Two bell curves with different means and spreads
        ax = Axes(
            x_range=[-1, 12, 2], y_range=[0, 0.5, 0.1],
            x_length=9, y_length=2.5,
            axis_config={"include_numbers": False, "stroke_width": 1},
        ).shift(DOWN * 0.7)

        def gauss(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

        curve_a = ax.plot(lambda x: gauss(x, 3, 0.8), x_range=[0, 6], color=GREEN)
        curve_b = ax.plot(lambda x: gauss(x, 8, 2), x_range=[2, 12], color=RED)

        lbl_a = Text("Feature A", font_size=14, color=GREEN).next_to(ax.c2p(3, 0.5), UP, buff=0.1)
        lbl_b = Text("Feature B", font_size=14, color=RED).next_to(ax.c2p(8, 0.22), UP, buff=0.1)

        mean_a = DashedLine(ax.c2p(3, 0), ax.c2p(3, 0.5), color=GREEN, stroke_width=1.5)
        mean_b = DashedLine(ax.c2p(8, 0), ax.c2p(8, 0.22), color=RED, stroke_width=1.5)

        self.play(Create(ax), run_time=0.6)
        self.play(Create(curve_a), Create(mean_a), FadeIn(lbl_a), run_time=0.8)
        self.play(Create(curve_b), Create(mean_b), FadeIn(lbl_b), run_time=0.8)

        problems = VGroup(
            Text("✗ Different means (centers)", font_size=14, color=ORANGE),
            Text("✗ Different spreads (variance)", font_size=14, color=ORANGE),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).shift(DOWN * 2.8 + LEFT * 3)

        solution = VGroup(
            Text("✓ Mean → 0", font_size=14, color=GREEN),
            Text("✓ Std Dev → 1", font_size=14, color=GREEN),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).shift(DOWN * 2.8 + RIGHT * 3)

        self.play(FadeIn(problems), run_time=0.6)
        self.play(FadeIn(solution), run_time=0.6)
        self.wait(2)


class Part2_Formula(Scene):
    """The formula with step-by-step centering and scaling."""
    def construct(self):
        title = Text("Standardization", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        # The formula
        fl = Text("The Formula", font_size=24, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(fl), run_time=0.4)

        formula = MathTex(
            r"X_{\text{std}} = \frac{X - \mu}{\sigma}",
            font_size=44, color=WHITE
        ).next_to(fl, DOWN, buff=0.4)
        box = SurroundingRectangle(formula, color=BLUE, buff=0.2, corner_radius=0.1)

        where = VGroup(
            MathTex(r"\mu", font_size=22, color=TEAL),
            Text(" = mean (center)", font_size=16, color=GRAY),
            MathTex(r"\sigma", font_size=22, color=GOLD),
            Text(" = std deviation (spread)", font_size=16, color=GRAY),
        )
        row1 = VGroup(where[0], where[1]).arrange(RIGHT, buff=0.1)
        row2 = VGroup(where[2], where[3]).arrange(RIGHT, buff=0.1)
        where_grp = VGroup(row1, row2).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(formula, DOWN, buff=0.4)

        self.play(Write(formula), Create(box), run_time=1.2)
        self.play(FadeIn(where_grp), run_time=0.6)
        self.wait(1)
        self.play(FadeOut(fl), FadeOut(where_grp))

        # ---- Step 1: Centering ----
        step1 = Text("Step 1: Subtract the Mean (Centering)", font_size=20, color=TEAL)
        step1.next_to(title, DOWN, buff=0.35)
        self.play(Write(step1), run_time=0.6)

        ax1 = Axes(
            x_range=[20, 80, 10], y_range=[0, 0.06, 0.01],
            x_length=7, y_length=2, axis_config={"include_numbers": False, "stroke_width": 1},
        ).shift(DOWN * 1.8)

        def gauss(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

        curve1 = ax1.plot(lambda x: gauss(x, 50, 10), x_range=[20, 80], color=GREEN)
        mean_line1 = DashedLine(ax1.c2p(50, 0), ax1.c2p(50, 0.042), color=YELLOW, stroke_width=2)
        mu_lbl = MathTex(r"\mu=50", font_size=18, color=YELLOW).next_to(mean_line1, UP, buff=0.1)
        lbl_orig = Text("Original: centered at 50", font_size=14, color=GRAY).next_to(ax1, DOWN, buff=0.15)

        self.play(Create(ax1), Create(curve1), Create(mean_line1), FadeIn(mu_lbl), FadeIn(lbl_orig), run_time=1)
        self.wait(0.5)

        # Transform to centered at 0
        ax2 = Axes(
            x_range=[-30, 30, 10], y_range=[0, 0.06, 0.01],
            x_length=7, y_length=2, axis_config={"include_numbers": False, "stroke_width": 1},
        ).shift(DOWN * 1.8)
        curve2 = ax2.plot(lambda x: gauss(x, 0, 10), x_range=[-30, 30], color=TEAL)
        mean_line2 = DashedLine(ax2.c2p(0, 0), ax2.c2p(0, 0.042), color=YELLOW, stroke_width=2)
        mu_lbl2 = MathTex(r"\mu=0", font_size=18, color=YELLOW).next_to(mean_line2, UP, buff=0.1)
        lbl_center = Text("After centering: mean = 0", font_size=14, color=TEAL).next_to(ax2, DOWN, buff=0.15)

        eq1 = MathTex(r"X - \mu", font_size=22, color=TEAL).shift(DOWN * 0.3 + RIGHT * 4)
        self.play(Write(eq1), run_time=0.4)

        self.play(
            Transform(ax1, ax2), Transform(curve1, curve2),
            Transform(mean_line1, mean_line2), Transform(mu_lbl, mu_lbl2),
            Transform(lbl_orig, lbl_center),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(VGroup(step1, eq1)))

        # ---- Step 2: Divide by sigma (Scaling) ----
        step2 = Text("Step 2: Divide by Std Dev (Scaling)", font_size=20, color=GOLD)
        step2.next_to(title, DOWN, buff=0.35)
        self.play(Write(step2), run_time=0.6)

        # Transform to std=1 (narrower/wider doesn't matter visually, just show)
        ax3 = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1],
            x_length=7, y_length=2, axis_config={"include_numbers": False, "stroke_width": 1},
        ).shift(DOWN * 1.8)
        curve3 = ax3.plot(lambda x: gauss(x, 0, 1), x_range=[-4, 4], color=GOLD)
        mean_line3 = DashedLine(ax3.c2p(0, 0), ax3.c2p(0, 0.42), color=YELLOW, stroke_width=2)
        mu_lbl3 = MathTex(r"\mu=0, \sigma=1", font_size=16, color=YELLOW).next_to(mean_line3, UP, buff=0.1)
        lbl_std = Text("After scaling: std = 1", font_size=14, color=GOLD).next_to(ax3, DOWN, buff=0.15)

        # Sigma markers
        sig_m1 = DashedLine(ax3.c2p(-1, 0), ax3.c2p(-1, 0.25), color=GRAY, stroke_width=1)
        sig_p1 = DashedLine(ax3.c2p(1, 0), ax3.c2p(1, 0.25), color=GRAY, stroke_width=1)
        sig_m2 = DashedLine(ax3.c2p(-2, 0), ax3.c2p(-2, 0.06), color=GRAY, stroke_width=1)
        sig_p2 = DashedLine(ax3.c2p(2, 0), ax3.c2p(2, 0.06), color=GRAY, stroke_width=1)
        sig_labels = VGroup(
            MathTex(r"-2\sigma", font_size=12, color=GRAY).next_to(sig_m2, DOWN, buff=0.05),
            MathTex(r"-1\sigma", font_size=12, color=GRAY).next_to(sig_m1, DOWN, buff=0.05),
            MathTex(r"+1\sigma", font_size=12, color=GRAY).next_to(sig_p1, DOWN, buff=0.05),
            MathTex(r"+2\sigma", font_size=12, color=GRAY).next_to(sig_p2, DOWN, buff=0.05),
        )

        eq2 = MathTex(r"\frac{X - \mu}{\sigma}", font_size=22, color=GOLD).shift(DOWN * 0.3 + RIGHT * 4)
        self.play(Write(eq2), run_time=0.4)

        self.play(
            Transform(ax1, ax3), Transform(curve1, curve3),
            Transform(mean_line1, mean_line3), Transform(mu_lbl, mu_lbl3),
            Transform(lbl_orig, lbl_std),
            run_time=1.5
        )
        self.play(
            Create(sig_m1), Create(sig_p1), Create(sig_m2), Create(sig_p2),
            FadeIn(sig_labels),
            run_time=0.6
        )

        unit_txt = Text("Unit = 'number of standard deviations'", font_size=14, color=WHITE)
        unit_txt.to_edge(DOWN, buff=0.15)
        self.play(Write(unit_txt), run_time=0.6)
        self.wait(2)


class Part3_ZScore(Scene):
    """Z-score intuition, example, and classroom analogy."""
    def construct(self):
        title = Text("Standardization", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        # Z-Score: what it means
        zscore_title = Text("What is a Z-Score?", font_size=26, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(zscore_title), run_time=0.5)

        meaning = Text("How many standard deviations from the mean", font_size=18, color=WHITE)
        meaning.next_to(zscore_title, DOWN, buff=0.35)
        self.play(Write(meaning), run_time=0.6)

        # Numerical example
        setup = VGroup(
            MathTex(r"\mu = 50", font_size=22, color=TEAL),
            MathTex(r"\sigma = 10", font_size=22, color=GOLD),
            Text("Value = 70", font_size=18, color=WHITE),
        ).arrange(RIGHT, buff=0.5).next_to(meaning, DOWN, buff=0.4)
        self.play(FadeIn(setup), run_time=0.5)

        calc = VGroup(
            MathTex(r"Z = \frac{70 - 50}{10}", font_size=28, color=WHITE),
            MathTex(r"= \frac{20}{10}", font_size=28, color=WHITE),
            MathTex(r"= 2", font_size=32, color=GREEN),
        ).arrange(RIGHT, buff=0.3).next_to(setup, DOWN, buff=0.4)

        self.play(Write(calc[0]), run_time=0.6)
        self.play(Write(calc[1]), run_time=0.4)
        self.play(Write(calc[2]), run_time=0.4)

        interp = Text("→ 2 standard deviations above the mean", font_size=18, color=GREEN)
        interp.next_to(calc, DOWN, buff=0.3)
        self.play(Write(interp), run_time=0.6)

        # Show on a mini bell curve
        def gauss(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

        ax = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1],
            x_length=6, y_length=1.5, axis_config={"include_numbers": False, "stroke_width": 1},
        ).to_edge(DOWN, buff=0.3)
        curve = ax.plot(lambda x: gauss(x, 0, 1), x_range=[-4, 4], color=BLUE_B)
        mean_line = DashedLine(ax.c2p(0, 0), ax.c2p(0, 0.42), color=GRAY, stroke_width=1)
        dot_z = Dot(ax.c2p(2, gauss(2, 0, 1)), color=GREEN, radius=0.08)
        arrow_z = Arrow(ax.c2p(2, -0.05), ax.c2p(2, gauss(2, 0, 1) - 0.02), color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        z_lbl = MathTex(r"Z=2", font_size=16, color=GREEN).next_to(arrow_z, DOWN, buff=0.05)

        self.play(Create(ax), Create(curve), Create(mean_line), run_time=0.6)
        self.play(FadeIn(dot_z), GrowArrow(arrow_z), FadeIn(z_lbl), run_time=0.5)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # ---- Classroom Analogy ----
        title2 = Text("Standardization", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        analogy_title = Text("Real-World Analogy: Two Classrooms", font_size=24, color=YELLOW)
        analogy_title.next_to(title2, DOWN, buff=0.35)
        self.play(Write(title2), Write(analogy_title), run_time=0.7)

        class_a = VGroup(
            Text("Class A", font_size=20, color=GREEN),
            MathTex(r"\mu = 150\text{ cm}", font_size=18, color=GREEN_B),
            MathTex(r"\sigma = 5\text{ cm}", font_size=18, color=GREEN_B),
        ).arrange(DOWN, buff=0.1).shift(LEFT * 3.5 + DOWN * 0.3)

        class_b = VGroup(
            Text("Class B", font_size=20, color=RED),
            MathTex(r"\mu = 170\text{ cm}", font_size=18, color=RED_B),
            MathTex(r"\sigma = 10\text{ cm}", font_size=18, color=RED_B),
        ).arrange(DOWN, buff=0.1).shift(RIGHT * 3.5 + DOWN * 0.3)

        self.play(FadeIn(class_a), FadeIn(class_b), run_time=0.8)

        # Students
        student_a = VGroup(
            Text("Student: 160 cm", font_size=16, color=GREEN),
            MathTex(r"Z = \frac{160-150}{5} = +2\sigma", font_size=20, color=GREEN),
        ).arrange(DOWN, buff=0.1).shift(LEFT * 3.5 + DOWN * 1.8)

        student_b = VGroup(
            Text("Student: 190 cm", font_size=16, color=RED),
            MathTex(r"Z = \frac{190-170}{10} = +2\sigma", font_size=20, color=RED),
        ).arrange(DOWN, buff=0.1).shift(RIGHT * 3.5 + DOWN * 1.8)

        self.play(FadeIn(student_a), run_time=0.6)
        self.play(FadeIn(student_b), run_time=0.6)

        insight = Text("Both are equally exceptional — Z = +2σ in their group!", font_size=18, color=YELLOW)
        insight.to_edge(DOWN, buff=0.3)
        self.play(Write(insight), run_time=0.8)

        equal_box = SurroundingRectangle(
            VGroup(student_a[1], student_b[1]), color=YELLOW, buff=0.15, corner_radius=0.1
        )
        self.play(Create(equal_box), run_time=0.5)

        takeaway = Text("Standardization converts raw units → relative position", font_size=16, color=WHITE)
        takeaway.next_to(insight, DOWN, buff=0.15)
        self.play(Write(takeaway), run_time=0.6)
        self.wait(2)


class Part4_Comparison(Scene):
    """Why standardization handles outliers better + linear algebra view."""
    def construct(self):
        title = Text("Standardization", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        # Outlier comparison
        comp_title = Text("Standardization vs Min–Max: Outliers", font_size=22, color=YELLOW)
        comp_title.next_to(title, DOWN, buff=0.35)
        self.play(Write(comp_title), run_time=0.6)

        # Left: Min-Max with outlier
        left_lbl = Text("Min–Max", font_size=18, color=RED).shift(LEFT * 3.2 + UP * 0.8)
        nl_mm = NumberLine(x_range=[0, 1, 0.2], length=4, include_numbers=True,
                           font_size=12, color=RED).shift(LEFT * 3.2 + DOWN * 0.2)

        # Normal points clustered near 0 due to outlier pushing max
        dots_mm = VGroup(
            Dot(nl_mm.n2p(0.01), color=TEAL, radius=0.04),
            Dot(nl_mm.n2p(0.02), color=TEAL, radius=0.04),
            Dot(nl_mm.n2p(0.03), color=TEAL, radius=0.04),
            Dot(nl_mm.n2p(0.04), color=TEAL, radius=0.04),
            Dot(nl_mm.n2p(0.05), color=TEAL, radius=0.04),
            Dot(nl_mm.n2p(1.0), color=ORANGE, radius=0.06),  # outlier
        )
        outlier_lbl = Text("Outlier!", font_size=12, color=ORANGE).next_to(dots_mm[-1], UP, buff=0.1)
        squished = Text("All data squished to the left!", font_size=12, color=RED).next_to(nl_mm, DOWN, buff=0.2)

        self.play(FadeIn(left_lbl), Create(nl_mm), run_time=0.5)
        self.play(FadeIn(dots_mm), FadeIn(outlier_lbl), run_time=0.5)
        self.play(Write(squished), run_time=0.4)

        # Right: Standardization with outlier
        right_lbl = Text("Standardization", font_size=18, color=GREEN).shift(RIGHT * 3.2 + UP * 0.8)
        nl_std = NumberLine(x_range=[-2, 4, 1], length=4, include_numbers=True,
                            font_size=12, color=GREEN).shift(RIGHT * 3.2 + DOWN * 0.2)

        dots_std = VGroup(
            Dot(nl_std.n2p(-0.5), color=TEAL, radius=0.04),
            Dot(nl_std.n2p(-0.3), color=TEAL, radius=0.04),
            Dot(nl_std.n2p(0.0), color=TEAL, radius=0.04),
            Dot(nl_std.n2p(0.2), color=TEAL, radius=0.04),
            Dot(nl_std.n2p(0.5), color=TEAL, radius=0.04),
            Dot(nl_std.n2p(3.5), color=ORANGE, radius=0.06),  # outlier
        )
        outlier_lbl2 = Text("Outlier (Z=3.5)", font_size=12, color=ORANGE).next_to(dots_std[-1], UP, buff=0.1)
        spread = Text("Data spread preserved!", font_size=12, color=GREEN).next_to(nl_std, DOWN, buff=0.2)

        self.play(FadeIn(right_lbl), Create(nl_std), run_time=0.5)
        self.play(FadeIn(dots_std), FadeIn(outlier_lbl2), run_time=0.5)
        self.play(Write(spread), run_time=0.4)
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            left_lbl, nl_mm, dots_mm, outlier_lbl, squished,
            right_lbl, nl_std, dots_std, outlier_lbl2, spread, comp_title
        )))

        # Linear algebra view
        la_title = Text("Why It Works (Linear Algebra)", font_size=22, color=YELLOW)
        la_title.next_to(title, DOWN, buff=0.35)
        self.play(Write(la_title), run_time=0.5)

        linear = VGroup(
            Text("Standardization is a linear transform:", font_size=16, color=GRAY),
            MathTex(r"X_{\text{new}} = aX + b", font_size=30, color=WHITE),
        ).arrange(DOWN, buff=0.2).shift(UP * 0.2)

        params = VGroup(
            MathTex(r"a = \frac{1}{\sigma}", font_size=24, color=TEAL),
            MathTex(r"b = -\frac{\mu}{\sigma}", font_size=24, color=GOLD),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).shift(DOWN * 1)

        effects = VGroup(
            Text("→ Moves centroid to origin", font_size=14, color=GREEN),
            Text("→ Scales variance equally", font_size=14, color=GREEN),
            Text("→ Stabilizes covariance matrix (PCA)", font_size=14, color=GREEN),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).shift(DOWN * 2.3)

        self.play(FadeIn(linear), run_time=0.6)
        self.play(Write(params[0]), Write(params[1]), run_time=0.8)
        for e in effects:
            self.play(Write(e), run_time=0.4)
        self.wait(2)
