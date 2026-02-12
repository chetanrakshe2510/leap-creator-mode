from manim import *
import numpy as np

class Part1_Problem(Scene):
    """What problem does gradient descent solve?"""
    def construct(self):
        title = Text("Gradient Descent", font_size=40, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        q = Text("What problem does it solve?", font_size=24, color=YELLOW)
        q.next_to(title, DOWN, buff=0.4)
        self.play(Write(q), run_time=0.6)

        # Model with parameters
        points = VGroup(
            Text("We build models with parameters (weights)", font_size=18, color=GRAY),
            Text("We want parameters that minimize error", font_size=18, color=GRAY),
        ).arrange(DOWN, buff=0.15).next_to(q, DOWN, buff=0.4)
        self.play(FadeIn(points), run_time=0.6)
        self.wait(0.5)

        real_q = Text("How do we adjust parameters to reduce error?", font_size=20, color=WHITE)
        real_q.next_to(points, DOWN, buff=0.5)
        box = SurroundingRectangle(real_q, color=YELLOW, buff=0.15, corner_radius=0.1)
        self.play(Write(real_q), Create(box), run_time=0.8)
        self.wait(0.5)

        answer = Text("That process is Gradient Descent.", font_size=22, color=GREEN)
        answer.next_to(box, DOWN, buff=0.4)
        self.play(Write(answer), run_time=0.7)
        self.wait(1)

        # Core idea
        self.play(FadeOut(VGroup(points, real_q, box, answer, q)))

        core = Text("Core Idea", font_size=26, color=YELLOW).next_to(title, DOWN, buff=0.4)
        self.play(Write(core), run_time=0.4)

        idea = Text(
            "Repeatedly move in the direction\nthat reduces error the fastest.",
            font_size=22, color=WHITE, line_spacing=1.3
        ).next_to(core, DOWN, buff=0.4)
        idea_box = SurroundingRectangle(idea, color=GREEN, buff=0.2, corner_radius=0.1)
        self.play(Write(idea), Create(idea_box), run_time=1)

        # Show a simple parabola with an arrow pointing downhill
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[0, 9, 2],
            x_length=5, y_length=2.5,
            axis_config={"include_numbers": False, "stroke_width": 1},
        ).to_edge(DOWN, buff=0.3)

        curve = ax.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE_B, stroke_width=2)
        dot = Dot(ax.c2p(2, 4), color=YELLOW, radius=0.08)
        arrow = Arrow(
            ax.c2p(2, 4), ax.c2p(1, 1),
            color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.2
        )
        min_dot = Dot(ax.c2p(0, 0), color=GREEN, radius=0.08)
        min_lbl = Text("minimum", font_size=10, color=GREEN).next_to(min_dot, DOWN, buff=0.1)

        self.play(Create(ax), Create(curve), run_time=0.6)
        self.play(FadeIn(dot), FadeIn(min_dot), FadeIn(min_lbl), run_time=0.4)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.wait(2)


class Part2_Formula(Scene):
    """f(w) = w², gradient, and update rule."""
    def construct(self):
        title = Text("Gradient Descent", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        # Error function
        sub = Text("Simple Example", font_size=22, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(sub), run_time=0.4)

        func = MathTex(r"f(w) = w^2", font_size=36, color=WHITE)
        func_desc = Text("← our 'error' function", font_size=14, color=GRAY)
        VGroup(func, func_desc).arrange(RIGHT, buff=0.3).next_to(sub, DOWN, buff=0.4)
        self.play(Write(func), FadeIn(func_desc), run_time=0.6)

        goal = Text("Goal: Find w that minimizes f(w)", font_size=16, color=GREEN)
        goal.next_to(func, DOWN, buff=0.3)
        self.play(Write(goal), run_time=0.5)
        self.wait(0.5)

        self.play(FadeOut(VGroup(sub, func_desc, goal)))

        # Step 1: Gradient
        s1 = Text("Step 1: Compute the Gradient", font_size=20, color=TEAL)
        s1.next_to(title, DOWN, buff=0.35)
        self.play(Write(s1), run_time=0.4)

        grad = MathTex(r"\frac{df}{dw} = 2w", font_size=32, color=WHITE)
        grad.next_to(func, DOWN, buff=0.3)
        self.play(Write(grad), run_time=0.6)

        grad_meaning = VGroup(
            MathTex(r"w > 0 \Rightarrow", font_size=20, color=WHITE),
            Text("slope positive (go left)", font_size=14, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        grad_meaning2 = VGroup(
            MathTex(r"w < 0 \Rightarrow", font_size=20, color=WHITE),
            Text("slope negative (go right)", font_size=14, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        gm = VGroup(grad_meaning, grad_meaning2).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        gm.next_to(grad, DOWN, buff=0.3)
        self.play(FadeIn(gm), run_time=0.5)
        self.wait(0.5)

        self.play(FadeOut(VGroup(s1, grad, gm)))

        # Step 2: Update rule
        s2 = Text("Step 2: Update Rule", font_size=20, color=GOLD)
        s2.next_to(title, DOWN, buff=0.35)
        self.play(Write(s2), run_time=0.4)

        update = MathTex(
            r"w_{\text{new}} = w_{\text{old}} - \alpha \cdot \frac{df}{dw}",
            font_size=34, color=WHITE
        ).next_to(func, DOWN, buff=0.3)
        update_box = SurroundingRectangle(update, color=GOLD, buff=0.15, corner_radius=0.1)
        self.play(Write(update), Create(update_box), run_time=0.8)

        alpha_note = VGroup(
            MathTex(r"\alpha", font_size=22, color=GOLD),
            Text(" = learning rate (step size)", font_size=14, color=GRAY),
        ).arrange(RIGHT, buff=0.1).next_to(update_box, DOWN, buff=0.3)
        self.play(FadeIn(alpha_note), run_time=0.4)

        minus = Text("Minus sign → move opposite to slope!", font_size=16, color=GREEN)
        minus.next_to(alpha_note, DOWN, buff=0.2)
        self.play(Write(minus), run_time=0.5)
        self.wait(2)


class Part3_Animation(Scene):
    """Animated gradient descent on w² with numerical iterations."""
    def construct(self):
        title = Text("Gradient Descent", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        sub = Text("Watching It Work", font_size=22, color=YELLOW).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), Write(sub), run_time=0.8)

        # Setup
        setup = VGroup(
            MathTex(r"f(w) = w^2", font_size=20, color=GRAY),
            MathTex(r"\alpha = 0.1", font_size=20, color=GOLD),
            MathTex(r"w_0 = 4", font_size=20, color=WHITE),
        ).arrange(RIGHT, buff=0.6).next_to(sub, DOWN, buff=0.25)
        self.play(FadeIn(setup), run_time=0.4)

        # Axes with parabola
        ax = Axes(
            x_range=[-1, 5, 1], y_range=[0, 17, 4],
            x_length=7, y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 12, "stroke_width": 1},
        ).shift(DOWN * 1)
        x_lbl = MathTex(r"w", font_size=16, color=GRAY).next_to(ax.x_axis, DOWN, buff=0.15)
        y_lbl = MathTex(r"f(w)", font_size=16, color=GRAY).next_to(ax.y_axis, LEFT, buff=0.15)
        curve = ax.plot(lambda x: x**2, x_range=[-0.5, 4.2], color=BLUE_B, stroke_width=2)

        self.play(Create(ax), Create(curve), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)

        # Gradient descent iterations
        w = 4.0
        alpha = 0.1
        dot = Dot(ax.c2p(w, w**2), color=YELLOW, radius=0.1)
        w_text = MathTex(f"w = {w:.2f}", font_size=18, color=YELLOW)
        w_text.to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        self.play(FadeIn(dot), FadeIn(w_text), run_time=0.4)

        # Iteration tracker
        iter_texts = VGroup()

        for i in range(8):
            grad = 2 * w
            w_new = w - alpha * grad

            # Show calculation briefly
            calc = MathTex(
                f"w = {w:.2f} - 0.1 \\times {grad:.1f} = {w_new:.2f}",
                font_size=14, color=GRAY
            ).to_edge(DOWN, buff=0.15)

            new_dot = Dot(ax.c2p(w_new, w_new**2), color=YELLOW, radius=0.1)
            trail = DashedLine(
                ax.c2p(w, w**2), ax.c2p(w_new, w_new**2),
                color=GREEN, stroke_width=1
            )
            new_w_text = MathTex(f"w = {w_new:.2f}", font_size=18, color=YELLOW)
            new_w_text.to_edge(RIGHT, buff=0.5).shift(UP * 0.5)

            self.play(
                Create(trail),
                Transform(dot, new_dot),
                Transform(w_text, new_w_text),
                FadeIn(calc),
                run_time=0.6 if i < 4 else 0.3
            )
            if i < 4:
                self.wait(0.3)

            # Remove calc for next iteration
            if i < 7:
                self.play(FadeOut(calc), run_time=0.15)

            w = w_new

        # Show convergence
        conv = Text("→ Converges to w = 0 (the minimum!)", font_size=18, color=GREEN)
        conv.to_edge(DOWN, buff=0.4)
        self.play(Write(conv), run_time=0.6)

        min_dot = Dot(ax.c2p(0, 0), color=GREEN, radius=0.12)
        self.play(FadeIn(min_dot), run_time=0.3)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # What is the gradient?
        title2 = Text("Gradient Descent", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        grad_title = Text("What Is the Gradient?", font_size=26, color=YELLOW)
        grad_title.next_to(title2, DOWN, buff=0.35)
        self.play(Write(title2), Write(grad_title), run_time=0.6)

        meaning = VGroup(
            Text("Gradient = slope of the error function", font_size=18, color=WHITE),
            Text("It tells us:", font_size=16, color=GRAY),
            Text("  • Which direction increases error", font_size=16, color=RED),
            Text("  • How steep the slope is", font_size=16, color=RED),
            Text("To reduce error → move opposite the slope", font_size=18, color=GREEN),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(grad_title, DOWN, buff=0.4)

        for m in meaning:
            self.play(Write(m), run_time=0.4)

        # Visual: parabola with tangent arrows
        ax2 = Axes(
            x_range=[-3, 3, 1], y_range=[0, 9, 3],
            x_length=5, y_length=2,
            axis_config={"include_numbers": False, "stroke_width": 1},
        ).to_edge(DOWN, buff=0.2)
        curve2 = ax2.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE_B, stroke_width=2)

        # Positive gradient at w=2
        pt_r = Dot(ax2.c2p(2, 4), color=RED, radius=0.06)
        arr_r = Arrow(ax2.c2p(2, 4), ax2.c2p(1, 4), color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.3)
        lbl_r = Text("go left", font_size=10, color=GREEN).next_to(arr_r, UP, buff=0.05)

        # Negative gradient at w=-2
        pt_l = Dot(ax2.c2p(-2, 4), color=RED, radius=0.06)
        arr_l = Arrow(ax2.c2p(-2, 4), ax2.c2p(-1, 4), color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.3)
        lbl_l = Text("go right", font_size=10, color=GREEN).next_to(arr_l, UP, buff=0.05)

        self.play(Create(ax2), Create(curve2), run_time=0.5)
        self.play(FadeIn(pt_r), GrowArrow(arr_r), FadeIn(lbl_r), run_time=0.4)
        self.play(FadeIn(pt_l), GrowArrow(arr_l), FadeIn(lbl_l), run_time=0.4)
        self.wait(2)
