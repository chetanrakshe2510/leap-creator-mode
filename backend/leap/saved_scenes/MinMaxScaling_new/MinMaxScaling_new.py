from manim import *
import numpy as np

class Part1_Problem(Scene):
    """What problem are we solving?"""
    def construct(self):
        title = Text("Min–Max Scaling", font_size=40, color=BLUE)
        subtitle = Text("(Normalization)", font_size=24, color=BLUE_B).next_to(title, DOWN, buff=0.15)
        VGroup(title, subtitle).to_edge(UP, buff=0.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1)

        q = Text("What problem are we solving?", font_size=26, color=YELLOW).next_to(subtitle, DOWN, buff=0.5)
        self.play(Write(q), run_time=0.8)

        # Show three features with wildly different ranges
        features = VGroup(
            VGroup(
                Text("Age", font_size=18, color=GREEN),
                Text("18 — 60", font_size=14, color=GREEN_B),
                Rectangle(width=0.8, height=0.3, color=GREEN, fill_opacity=0.3),
            ).arrange(DOWN, buff=0.1),
            VGroup(
                Text("Salary", font_size=18, color=RED),
                Text("10k — 2,00,000", font_size=14, color=RED_B),
                Rectangle(width=4.0, height=0.3, color=RED, fill_opacity=0.3),
            ).arrange(DOWN, buff=0.1),
            VGroup(
                Text("Pixel Intensity", font_size=18, color=PURPLE),
                Text("0 — 255", font_size=14, color=PURPLE_B),
                Rectangle(width=1.5, height=0.3, color=PURPLE, fill_opacity=0.3),
            ).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.8).shift(DOWN * 0.3)

        for f in features:
            self.play(FadeIn(f), run_time=0.6)
        self.wait(0.5)

        # Problems
        problems = VGroup(
            Text("✗ Large features dominate", font_size=16, color=RED),
            Text("✗ KNN / SVM / Clustering get biased", font_size=16, color=RED),
            Text("✗ Gradient descent converges slowly", font_size=16, color=RED),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).shift(DOWN * 2.2)

        for p in problems:
            self.play(Write(p), run_time=0.5)

        self.wait(1)

        solution = Text("Solution: Rescale everything to [0, 1]", font_size=22, color=GREEN)
        solution.to_edge(DOWN, buff=0.3)
        self.play(Write(solution), run_time=0.8)
        self.wait(1.5)


class Part2_Formula(Scene):
    """The formula and step-by-step breakdown."""
    def construct(self):
        title = Text("Min–Max Scaling", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        # The formula
        formula_label = Text("The Formula", font_size=26, color=YELLOW).next_to(title, DOWN, buff=0.4)
        self.play(Write(formula_label), run_time=0.5)

        formula = MathTex(
            r"X_{\text{norm}} = \frac{X - X_{\min}}{X_{\max} - X_{\min}}",
            font_size=44, color=WHITE
        ).next_to(formula_label, DOWN, buff=0.5)
        box = SurroundingRectangle(formula, color=BLUE, buff=0.2, corner_radius=0.1)
        self.play(Write(formula), Create(box), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(formula_label))

        # Step 1: Subtract the minimum
        step1_title = Text("Step 1: Subtract the Minimum", font_size=22, color=TEAL)
        step1_title.next_to(title, DOWN, buff=0.35)
        self.play(Write(step1_title), run_time=0.6)

        # Show number line — original
        nl_orig = NumberLine(x_range=[10, 60, 10], length=8, include_numbers=True,
                            font_size=16, color=GRAY).shift(DOWN * 1.8)
        brace_orig = BraceBetweenPoints(nl_orig.n2p(10), nl_orig.n2p(60), UP, color=ORANGE)
        brace_lbl = MathTex(r"[X_{\min}, X_{\max}]", font_size=18, color=ORANGE).next_to(brace_orig, UP, buff=0.1)
        lbl_orig = Text("Original range", font_size=14, color=GRAY).next_to(nl_orig, DOWN, buff=0.2)

        self.play(Create(nl_orig), FadeIn(lbl_orig), run_time=0.8)
        self.play(GrowFromCenter(brace_orig), FadeIn(brace_lbl), run_time=0.6)

        step1_eq = MathTex(r"X - X_{\min}", font_size=24, color=TEAL).shift(DOWN * 0.5 + RIGHT * 3)
        arrow_shift = Text("Shift so min → 0", font_size=14, color=TEAL).next_to(step1_eq, RIGHT, buff=0.2)
        self.play(Write(step1_eq), Write(arrow_shift), run_time=0.8)

        # Animate shift: number line moves
        nl_shifted = NumberLine(x_range=[0, 50, 10], length=8, include_numbers=True,
                               font_size=16, color=GREEN).shift(DOWN * 1.8)
        brace_new = BraceBetweenPoints(nl_shifted.n2p(0), nl_shifted.n2p(50), UP, color=GREEN)
        brace_new_lbl = MathTex(r"[0, X_{\max}-X_{\min}]", font_size=18, color=GREEN).next_to(brace_new, UP, buff=0.1)
        lbl_shift = Text("After shifting", font_size=14, color=GREEN).next_to(nl_shifted, DOWN, buff=0.2)

        self.play(
            Transform(nl_orig, nl_shifted),
            Transform(brace_orig, brace_new),
            Transform(brace_lbl, brace_new_lbl),
            Transform(lbl_orig, lbl_shift),
            run_time=1.5
        )
        self.wait(1)

        self.play(FadeOut(VGroup(step1_eq, arrow_shift, step1_title)))

        # Step 2: Divide by the range
        step2_title = Text("Step 2: Divide by the Range", font_size=22, color=GOLD)
        step2_title.next_to(title, DOWN, buff=0.35)
        self.play(Write(step2_title), run_time=0.6)

        step2_eq = MathTex(
            r"\frac{X - X_{\min}}{X_{\max} - X_{\min}}",
            font_size=24, color=GOLD
        ).shift(DOWN * 0.5 + RIGHT * 3)
        arrow_scale = Text("Scale so max → 1", font_size=14, color=GOLD).next_to(step2_eq, RIGHT, buff=0.2)
        self.play(Write(step2_eq), Write(arrow_scale), run_time=0.8)

        # Animate: compress to [0,1]
        nl_final = NumberLine(x_range=[0, 1, 0.2], length=8, include_numbers=True,
                              font_size=16, color=YELLOW).shift(DOWN * 1.8)
        brace_final = BraceBetweenPoints(nl_final.n2p(0), nl_final.n2p(1), UP, color=YELLOW)
        brace_final_lbl = MathTex(r"[0, 1]", font_size=20, color=YELLOW).next_to(brace_final, UP, buff=0.1)
        lbl_final = Text("After scaling", font_size=14, color=YELLOW).next_to(nl_final, DOWN, buff=0.2)

        self.play(
            Transform(nl_orig, nl_final),
            Transform(brace_orig, brace_final),
            Transform(brace_lbl, brace_final_lbl),
            Transform(lbl_orig, lbl_final),
            run_time=1.5
        )

        summary = VGroup(
            Text("Step 1: Translation (shift min to 0)", font_size=14, color=TEAL),
            Text("Step 2: Scaling (compress max to 1)", font_size=14, color=GOLD),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(2)


class Part3_Example(Scene):
    """Concrete numerical example + geometric interpretation."""
    def construct(self):
        title = Text("Min–Max Scaling", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        # Numerical example
        ex_title = Text("Numerical Example", font_size=26, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(ex_title), run_time=0.5)

        setup = VGroup(
            Text("Marks range: 40 to 100", font_size=18, color=GRAY),
            Text("Student score: 70", font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.15).next_to(ex_title, DOWN, buff=0.4)
        self.play(FadeIn(setup), run_time=0.6)

        # Number line with the score highlighted
        nl = NumberLine(x_range=[40, 100, 10], length=8, include_numbers=True,
                        font_size=16, color=GRAY).shift(DOWN * 0.5)
        dot_score = Dot(nl.n2p(70), color=YELLOW, radius=0.1)
        dot_label = Text("70", font_size=16, color=YELLOW).next_to(dot_score, UP, buff=0.15)

        self.play(Create(nl), run_time=0.6)
        self.play(FadeIn(dot_score), FadeIn(dot_label), run_time=0.4)

        # Show calculation step by step
        calc = VGroup(
            MathTex(r"X_{\text{norm}} = \frac{70 - 40}{100 - 40}", font_size=28, color=WHITE),
            MathTex(r"= \frac{30}{60}", font_size=28, color=WHITE),
            MathTex(r"= 0.5", font_size=32, color=GREEN),
        ).arrange(RIGHT, buff=0.4).shift(DOWN * 1.8)

        self.play(Write(calc[0]), run_time=0.8)
        self.play(Write(calc[1]), run_time=0.6)
        self.play(Write(calc[2]), run_time=0.6)

        interp = Text("The student is exactly halfway between min and max!", font_size=18, color=GREEN)
        interp.shift(DOWN * 2.8)
        self.play(Write(interp), run_time=0.8)
        self.wait(1.5)

        # Animate the transformation
        self.play(FadeOut(VGroup(setup, calc, interp, ex_title)))

        geo_title = Text("Geometric View", font_size=26, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(geo_title), run_time=0.5)

        # Transform number line from [40,100] to [0,1]
        nl_new = NumberLine(x_range=[0, 1, 0.2], length=8, include_numbers=True,
                            font_size=16, color=YELLOW).shift(DOWN * 0.5)
        dot_new = Dot(nl_new.n2p(0.5), color=YELLOW, radius=0.1)
        dot_new_label = Text("0.5", font_size=16, color=YELLOW).next_to(dot_new, UP, buff=0.15)

        self.play(
            Transform(nl, nl_new),
            Transform(dot_score, dot_new),
            Transform(dot_label, dot_new_label),
            run_time=1.5
        )

        note = VGroup(
            Text("Shape of distribution preserved ✓", font_size=16, color=GREEN),
            Text("Only compressed/stretched linearly ✓", font_size=16, color=GREEN),
        ).arrange(DOWN, buff=0.1).shift(DOWN * 1.5)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.5)

        self.play(FadeOut(VGroup(nl, dot_score, dot_label, note, geo_title)))

        # Deep Insight: Linear Transformation
        deep_title = Text("Why It Works (Deep Insight)", font_size=26, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(deep_title), run_time=0.6)

        linear = VGroup(
            Text("Min–Max is a linear transformation:", font_size=18, color=GRAY),
            MathTex(r"X_{\text{new}} = aX + b", font_size=32, color=WHITE),
        ).arrange(DOWN, buff=0.3).shift(UP * 0.2)

        where = VGroup(
            MathTex(r"a = \frac{1}{X_{\max} - X_{\min}}", font_size=26, color=TEAL),
            MathTex(r"b = \frac{-X_{\min}}{X_{\max} - X_{\min}}", font_size=26, color=GOLD),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).shift(DOWN * 1.2)

        self.play(FadeIn(linear), run_time=0.8)
        self.play(Write(where[0]), run_time=0.6)
        self.play(Write(where[1]), run_time=0.6)

        key = VGroup(
            Text("Linear = preserves relative distances", font_size=16, color=GREEN),
            Text("No distortion of the data distribution", font_size=16, color=GREEN),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(key), run_time=0.6)
        self.wait(2)
