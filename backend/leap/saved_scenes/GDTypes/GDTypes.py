from manim import *
import numpy as np

class Part1_Types(Scene):
    """Three types of gradient descent with visual data usage."""
    def construct(self):
        title = Text("Types of Gradient Descent", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # Dataset representation — grid of dots
        def make_data_grid(rows=4, cols=5, color=WHITE, fill=0.4):
            dots = VGroup()
            for r in range(rows):
                for c in range(cols):
                    sq = Square(side_length=0.22, color=color, fill_opacity=fill, stroke_width=1)
                    sq.move_to(RIGHT * c * 0.28 + DOWN * r * 0.28)
                    dots.add(sq)
            dots.move_to(ORIGIN)
            return dots

        # ── TYPE 1: Batch GD ──
        t1 = Text("1. Batch Gradient Descent", font_size=22, color=GREEN)
        t1.next_to(title, DOWN, buff=0.4)
        self.play(Write(t1), run_time=0.5)

        batch_grid = make_data_grid(color=GREEN, fill=0.5)
        batch_grid.shift(LEFT * 3 + DOWN * 0.8)
        batch_lbl = Text("Full Dataset", font_size=12, color=GREEN).next_to(batch_grid, DOWN, buff=0.1)

        arrow1 = Arrow(LEFT * 1.5 + DOWN * 0.8, RIGHT * 0 + DOWN * 0.8, color=WHITE, stroke_width=1.5, max_tip_length_to_length_ratio=0.2)
        update1 = Text("1 update\nper epoch", font_size=12, color=GRAY).next_to(arrow1, RIGHT, buff=0.15)

        # All highlighted
        self.play(FadeIn(batch_grid), FadeIn(batch_lbl), run_time=0.4)
        self.play(GrowArrow(arrow1), FadeIn(update1), run_time=0.4)

        batch_props = VGroup(
            Text("✓ Stable gradients", font_size=12, color=GREEN),
            Text("✗ Slow on large data", font_size=12, color=RED),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT).next_to(update1, RIGHT, buff=0.3)
        self.play(FadeIn(batch_props), run_time=0.3)
        self.wait(0.8)

        type1_group = VGroup(t1, batch_grid, batch_lbl, arrow1, update1, batch_props)

        # ── TYPE 2: SGD ──
        self.play(FadeOut(type1_group))
        t2 = Text("2. Stochastic Gradient Descent (SGD)", font_size=22, color=GOLD)
        t2.next_to(title, DOWN, buff=0.4)
        self.play(Write(t2), run_time=0.5)

        sgd_grid = make_data_grid(color=GRAY, fill=0.15)
        sgd_grid.shift(LEFT * 3 + DOWN * 0.8)
        # Highlight just one sample
        sgd_grid[7].set_fill(GOLD, opacity=0.8)
        sgd_grid[7].set_stroke(GOLD, width=2)
        sgd_lbl = Text("1 Sample", font_size=12, color=GOLD).next_to(sgd_grid, DOWN, buff=0.1)

        arrow2 = Arrow(LEFT * 1.5 + DOWN * 0.8, RIGHT * 0 + DOWN * 0.8, color=WHITE, stroke_width=1.5, max_tip_length_to_length_ratio=0.2)
        update2 = Text("n updates\nper epoch", font_size=12, color=GRAY).next_to(arrow2, RIGHT, buff=0.15)

        self.play(FadeIn(sgd_grid), FadeIn(sgd_lbl), run_time=0.4)
        self.play(GrowArrow(arrow2), FadeIn(update2), run_time=0.4)

        sgd_props = VGroup(
            Text("✓ Fast updates", font_size=12, color=GREEN),
            Text("✗ Noisy gradients", font_size=12, color=RED),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT).next_to(update2, RIGHT, buff=0.3)
        self.play(FadeIn(sgd_props), run_time=0.3)

        # Animate highlighting different samples
        for idx in [3, 14, 9, 18]:
            new_grid = make_data_grid(color=GRAY, fill=0.15)
            new_grid.shift(LEFT * 3 + DOWN * 0.8)
            new_grid[idx].set_fill(GOLD, opacity=0.8)
            new_grid[idx].set_stroke(GOLD, width=2)
            self.play(Transform(sgd_grid, new_grid), run_time=0.25)

        self.wait(0.5)
        type2_group = VGroup(t2, sgd_grid, sgd_lbl, arrow2, update2, sgd_props)

        # ── TYPE 3: Mini-batch ──
        self.play(FadeOut(type2_group))
        t3 = Text("3. Mini-Batch Gradient Descent", font_size=22, color=TEAL)
        t3.next_to(title, DOWN, buff=0.4)
        self.play(Write(t3), run_time=0.5)

        mb_grid = make_data_grid(color=GRAY, fill=0.15)
        mb_grid.shift(LEFT * 3 + DOWN * 0.8)
        # Highlight a batch (row 1)
        for idx in [5, 6, 7, 8, 9]:
            mb_grid[idx].set_fill(TEAL, opacity=0.6)
            mb_grid[idx].set_stroke(TEAL, width=2)
        mb_lbl = Text("Mini-Batch", font_size=12, color=TEAL).next_to(mb_grid, DOWN, buff=0.1)

        arrow3 = Arrow(LEFT * 1.5 + DOWN * 0.8, RIGHT * 0 + DOWN * 0.8, color=WHITE, stroke_width=1.5, max_tip_length_to_length_ratio=0.2)
        update3 = Text("n/batch updates\nper epoch", font_size=12, color=GRAY).next_to(arrow3, RIGHT, buff=0.15)

        self.play(FadeIn(mb_grid), FadeIn(mb_lbl), run_time=0.4)
        self.play(GrowArrow(arrow3), FadeIn(update3), run_time=0.4)

        mb_props = VGroup(
            Text("✓ Balanced speed & stability", font_size=12, color=GREEN),
            Text("✓ GPU-friendly", font_size=12, color=GREEN),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT).next_to(update3, RIGHT, buff=0.3)
        self.play(FadeIn(mb_props), run_time=0.3)

        # Animate different mini-batches highlighted
        for batch_start in [0, 10, 15]:
            new_grid = make_data_grid(color=GRAY, fill=0.15)
            new_grid.shift(LEFT * 3 + DOWN * 0.8)
            for idx in range(batch_start, min(batch_start + 5, 20)):
                new_grid[idx].set_fill(TEAL, opacity=0.6)
                new_grid[idx].set_stroke(TEAL, width=2)
            self.play(Transform(mb_grid, new_grid), run_time=0.3)

        best = Text("→ Most common in practice!", font_size=16, color=YELLOW)
        best.to_edge(DOWN, buff=0.2)
        self.play(Write(best), run_time=0.5)
        self.wait(1.5)

        # Summary side by side
        self.play(*[FadeOut(m) for m in self.mobjects if m != title])

        summary_title = Text("Comparison", font_size=22, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(summary_title), run_time=0.3)

        # Table
        header = VGroup(
            Text("Type", font_size=12, color=GRAY),
            Text("Data Used", font_size=12, color=GRAY),
            Text("Speed", font_size=12, color=GRAY),
            Text("Stability", font_size=12, color=GRAY),
        ).arrange(RIGHT, buff=0.8)

        r1 = VGroup(
            Text("Batch", font_size=12, color=GREEN),
            Text("All", font_size=12, color=WHITE),
            Text("Slow", font_size=12, color=RED),
            Text("High", font_size=12, color=GREEN),
        ).arrange(RIGHT, buff=0.95)
        r2 = VGroup(
            Text("SGD", font_size=12, color=GOLD),
            Text("1", font_size=12, color=WHITE),
            Text("Fast", font_size=12, color=GREEN),
            Text("Low", font_size=12, color=RED),
        ).arrange(RIGHT, buff=1.1)
        r3 = VGroup(
            Text("Mini-batch", font_size=12, color=TEAL),
            Text("Subset", font_size=12, color=WHITE),
            Text("Medium", font_size=12, color=YELLOW),
            Text("Medium", font_size=12, color=YELLOW),
        ).arrange(RIGHT, buff=0.7)

        table = VGroup(header, r1, r2, r3).arrange(DOWN, buff=0.2)
        table.next_to(summary_title, DOWN, buff=0.3)
        sep = Line(header.get_left() + DOWN * 0.12, header.get_right() + DOWN * 0.12, color=GRAY, stroke_width=1)

        self.play(FadeIn(header), Create(sep), run_time=0.3)
        self.play(FadeIn(r1), run_time=0.25)
        self.play(FadeIn(r2), run_time=0.25)
        self.play(FadeIn(r3), run_time=0.25)

        # Visual: convergence paths on contour
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=3.5, y_length=3,
            axis_config={"include_numbers": False, "stroke_width": 0.5},
        ).to_edge(DOWN, buff=0.15)

        # Elliptical contours
        contours = VGroup()
        for r in [0.4, 0.8, 1.2, 1.6, 2.0]:
            e = Ellipse(width=r*2, height=r*1.5, color=BLUE_D, stroke_width=0.5, stroke_opacity=0.4)
            e.move_to(ax.c2p(0, 0))
            contours.add(e)

        self.play(Create(ax), Create(contours), run_time=0.5)

        # Batch: smooth direct path
        batch_path = VMobject(color=GREEN, stroke_width=1.5)
        batch_pts = [ax.c2p(-2, 2), ax.c2p(-1.2, 1.1), ax.c2p(-0.5, 0.4), ax.c2p(-0.1, 0.1), ax.c2p(0, 0)]
        batch_path.set_points_smoothly(batch_pts)
        bl = Text("Batch", font_size=9, color=GREEN).next_to(ax.c2p(-2, 2), LEFT, buff=0.05)

        # SGD: noisy path
        sgd_path = VMobject(color=GOLD, stroke_width=1.5)
        sgd_pts = [ax.c2p(2, 2), ax.c2p(1.5, 0.5), ax.c2p(2.2, 1.0), ax.c2p(0.8, -0.5), ax.c2p(1.0, 0.3), ax.c2p(-0.3, -0.2), ax.c2p(0.2, 0.1), ax.c2p(0, 0)]
        sgd_path.set_points_smoothly(sgd_pts)
        sl = Text("SGD", font_size=9, color=GOLD).next_to(ax.c2p(2, 2), RIGHT, buff=0.05)

        self.play(Create(batch_path), FadeIn(bl), run_time=0.6)
        self.play(Create(sgd_path), FadeIn(sl), run_time=0.6)
        self.wait(2)


class Part2_LearningRate(Scene):
    """Learning rate effects: too large, too small, just right."""
    def construct(self):
        title = Text("Learning Rate Importance", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        alpha_eq = MathTex(r"w_{\text{new}} = w_{\text{old}} - \alpha \cdot \nabla L", font_size=28, color=WHITE)
        alpha_eq.next_to(title, DOWN, buff=0.35)
        self.play(Write(alpha_eq), run_time=0.5)

        # Three side-by-side parabolas
        def gauss_like(x):
            return x**2

        # ── TOO LARGE ──
        ax1 = Axes(
            x_range=[-4, 4, 1], y_range=[0, 16, 4],
            x_length=3, y_length=2.5,
            axis_config={"include_numbers": False, "stroke_width": 0.8},
        ).shift(LEFT * 4 + DOWN * 1)
        c1 = ax1.plot(gauss_like, x_range=[-4, 4], color=BLUE_B, stroke_width=1.5)
        lbl1 = Text("α too large", font_size=14, color=RED).next_to(ax1, UP, buff=0.1)

        # Bouncing path — overshooting
        bounce_pts = [ax1.c2p(-3, 9), ax1.c2p(3.5, 12.25), ax1.c2p(-3.8, 14.44)]
        bounce = VMobject(color=RED, stroke_width=2)
        bounce.set_points_as_corners(bounce_pts)
        dots1 = VGroup(*[Dot(p, color=RED, radius=0.05) for p in bounce_pts])

        self.play(Create(ax1), Create(c1), FadeIn(lbl1), run_time=0.5)
        self.play(Create(bounce), FadeIn(dots1), run_time=0.8)
        diverge_txt = Text("Diverges!", font_size=11, color=RED).next_to(ax1, DOWN, buff=0.1)
        self.play(Write(diverge_txt), run_time=0.3)

        # ── TOO SMALL ──
        ax2 = Axes(
            x_range=[-4, 4, 1], y_range=[0, 16, 4],
            x_length=3, y_length=2.5,
            axis_config={"include_numbers": False, "stroke_width": 0.8},
        ).shift(DOWN * 1)
        c2 = ax2.plot(gauss_like, x_range=[-4, 4], color=BLUE_B, stroke_width=1.5)
        lbl2 = Text("α too small", font_size=14, color=YELLOW).next_to(ax2, UP, buff=0.1)

        # Tiny steps barely moving
        tiny_pts = [ax2.c2p(-3, 9)]
        w = -3.0
        for _ in range(8):
            w = w - 0.02 * (2 * w)  # very small alpha
            tiny_pts.append(ax2.c2p(w, w**2))
        tiny = VMobject(color=YELLOW, stroke_width=2)
        tiny.set_points_as_corners(tiny_pts)
        dots2 = VGroup(*[Dot(p, color=YELLOW, radius=0.04) for p in tiny_pts])

        self.play(Create(ax2), Create(c2), FadeIn(lbl2), run_time=0.5)
        self.play(Create(tiny), FadeIn(dots2), run_time=0.8)
        slow_txt = Text("Very slow!", font_size=11, color=YELLOW).next_to(ax2, DOWN, buff=0.1)
        self.play(Write(slow_txt), run_time=0.3)

        # ── JUST RIGHT ──
        ax3 = Axes(
            x_range=[-4, 4, 1], y_range=[0, 16, 4],
            x_length=3, y_length=2.5,
            axis_config={"include_numbers": False, "stroke_width": 0.8},
        ).shift(RIGHT * 4 + DOWN * 1)
        c3 = ax3.plot(gauss_like, x_range=[-4, 4], color=BLUE_B, stroke_width=1.5)
        lbl3 = Text("α just right", font_size=14, color=GREEN).next_to(ax3, UP, buff=0.1)

        # Smooth convergence
        good_pts = [ax3.c2p(-3, 9)]
        w = -3.0
        for _ in range(6):
            w = w - 0.3 * (2 * w)
            good_pts.append(ax3.c2p(w, w**2))
        good = VMobject(color=GREEN, stroke_width=2)
        good.set_points_as_corners(good_pts)
        dots3 = VGroup(*[Dot(p, color=GREEN, radius=0.05) for p in good_pts])

        self.play(Create(ax3), Create(c3), FadeIn(lbl3), run_time=0.5)
        self.play(Create(good), FadeIn(dots3), run_time=0.8)
        conv_txt = Text("Converges!", font_size=11, color=GREEN).next_to(ax3, DOWN, buff=0.1)
        self.play(Write(conv_txt), run_time=0.3)

        # Summary
        summary = VGroup(
            Text("Too large → overshoots & diverges", font_size=14, color=RED),
            Text("Too small → painfully slow", font_size=14, color=YELLOW),
            Text("Just right → efficient convergence", font_size=14, color=GREEN),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_edge(DOWN, buff=0.1)

        for s in summary:
            self.play(Write(s), run_time=0.3)
        self.wait(2)
