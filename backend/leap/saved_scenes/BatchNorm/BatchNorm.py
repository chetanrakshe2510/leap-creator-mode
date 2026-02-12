from manim import *
import numpy as np

class Part1_Problem(Scene):
    """Internal Covariate Shift — the problem."""
    def construct(self):
        title = Text("Batch Normalization", font_size=40, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1)

        prob = Text("The Problem: Internal Covariate Shift", font_size=24, color=RED)
        prob.next_to(title, DOWN, buff=0.4)
        self.play(Write(prob), run_time=0.8)

        # Neural network layers
        layers = VGroup()
        layer_labels = []
        colors = [GREEN, TEAL, BLUE, PURPLE]
        for i in range(4):
            rect = RoundedRectangle(
                width=1.2, height=2.0, corner_radius=0.15,
                color=colors[i], fill_opacity=0.15, stroke_width=2
            )
            lbl = Text(f"Layer {i+1}", font_size=12, color=colors[i]).move_to(rect.get_top() + DOWN * 0.2)
            layers.add(VGroup(rect, lbl))

        layers.arrange(RIGHT, buff=0.6).shift(DOWN * 0.5)

        # Arrows between layers
        arrows = VGroup()
        for i in range(3):
            a = Arrow(
                layers[i].get_right(), layers[i+1].get_left(),
                color=WHITE, stroke_width=2, buff=0.05,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(a)

        input_arrow = Arrow(LEFT * 0.8, ORIGIN, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        input_arrow.next_to(layers[0], LEFT, buff=0.05)
        input_lbl = Text("Input", font_size=12, color=GRAY).next_to(input_arrow, LEFT, buff=0.1)

        self.play(
            *[FadeIn(l) for l in layers],
            *[GrowArrow(a) for a in arrows],
            GrowArrow(input_arrow), FadeIn(input_lbl),
            run_time=1
        )
        self.wait(0.5)

        # Show distributions shifting inside each layer
        # Mini bell curves inside layers that shift
        def gauss(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

        # Epoch 1 distributions
        dist_texts = []
        for i, layer_group in enumerate(layers):
            rect = layer_group[0]
            ax = Axes(
                x_range=[-3, 3, 1], y_range=[0, 0.5, 0.1],
                x_length=0.9, y_length=1.0,
                axis_config={"stroke_width": 0.5, "include_ticks": False},
            ).move_to(rect.get_center() + DOWN * 0.15)
            curve = ax.plot(lambda x: gauss(x, 0, 1), x_range=[-3, 3], color=colors[i], stroke_width=1.5)
            dist_texts.append((ax, curve))

        epoch1_curves = VGroup()
        for ax, curve in dist_texts:
            epoch1_curves.add(VGroup(ax, curve))
        self.play(*[Create(g) for g in epoch1_curves], run_time=0.8)

        epoch_lbl = Text("Epoch 1", font_size=16, color=WHITE).to_edge(LEFT, buff=0.3).shift(DOWN * 2.5)
        self.play(FadeIn(epoch_lbl), run_time=0.3)
        self.wait(0.5)

        # Epoch 2 — distributions shift
        shifts = [0.5, -0.8, 1.0, -0.5]
        sigmas = [1.2, 0.7, 1.5, 0.8]
        epoch2_curves = VGroup()
        for i, layer_group in enumerate(layers):
            rect = layer_group[0]
            ax = Axes(
                x_range=[-3, 3, 1], y_range=[0, 0.7, 0.1],
                x_length=0.9, y_length=1.0,
                axis_config={"stroke_width": 0.5, "include_ticks": False},
            ).move_to(rect.get_center() + DOWN * 0.15)
            mu, sig = shifts[i], sigmas[i]
            curve = ax.plot(lambda x, m=mu, s=sig: gauss(x, m, s), x_range=[-3, 3], color=YELLOW, stroke_width=1.5)
            epoch2_curves.add(VGroup(ax, curve))

        epoch2_lbl = Text("Epoch 2", font_size=16, color=YELLOW).to_edge(LEFT, buff=0.3).shift(DOWN * 2.5)
        self.play(
            Transform(epoch1_curves, epoch2_curves),
            Transform(epoch_lbl, epoch2_lbl),
            run_time=1.2
        )
        self.wait(0.5)

        # Epoch 3 — shift again
        shifts2 = [-0.7, 1.2, -0.3, 0.9]
        sigmas2 = [0.6, 1.4, 0.9, 1.3]
        epoch3_curves = VGroup()
        for i, layer_group in enumerate(layers):
            rect = layer_group[0]
            ax = Axes(
                x_range=[-3, 3, 1], y_range=[0, 0.8, 0.1],
                x_length=0.9, y_length=1.0,
                axis_config={"stroke_width": 0.5, "include_ticks": False},
            ).move_to(rect.get_center() + DOWN * 0.15)
            mu, sig = shifts2[i], sigmas2[i]
            curve = ax.plot(lambda x, m=mu, s=sig: gauss(x, m, s), x_range=[-3, 3], color=ORANGE, stroke_width=1.5)
            epoch3_curves.add(VGroup(ax, curve))

        epoch3_lbl = Text("Epoch 3", font_size=16, color=ORANGE).to_edge(LEFT, buff=0.3).shift(DOWN * 2.5)
        self.play(
            Transform(epoch1_curves, epoch3_curves),
            Transform(epoch_lbl, epoch3_lbl),
            run_time=1.2
        )

        insight = Text("Distributions keep shifting → network must readjust every step!", font_size=16, color=RED)
        insight.to_edge(DOWN, buff=0.2)
        self.play(Write(insight), run_time=0.8)
        self.wait(2)


class Part2_Solution(Scene):
    """Batch Normalization — the solution, step by step."""
    def construct(self):
        title = Text("Batch Normalization", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        sol = Text("The Solution: Normalize Between Layers", font_size=22, color=GREEN)
        sol.next_to(title, DOWN, buff=0.35)
        self.play(Write(sol), run_time=0.7)

        # Show a simplified network with BN inserted
        layers = VGroup()
        bn_blocks = VGroup()
        colors = [GREEN, BLUE, PURPLE]
        for i in range(3):
            rect = RoundedRectangle(
                width=1.0, height=1.6, corner_radius=0.1,
                color=colors[i], fill_opacity=0.15, stroke_width=2
            )
            lbl = Text(f"Layer {i+1}", font_size=11, color=colors[i]).move_to(rect)
            layers.add(VGroup(rect, lbl))

        # BN blocks between layers
        for i in range(2):
            bn = RoundedRectangle(
                width=0.6, height=1.0, corner_radius=0.08,
                color=YELLOW, fill_opacity=0.25, stroke_width=2
            )
            bn_lbl = Text("BN", font_size=12, color=YELLOW).move_to(bn)
            bn_blocks.add(VGroup(bn, bn_lbl))

        # Arrange: Layer1 - BN - Layer2 - BN - Layer3
        network = VGroup(
            layers[0], bn_blocks[0], layers[1], bn_blocks[1], layers[2]
        ).arrange(RIGHT, buff=0.3).shift(DOWN * 0.2)

        arrows = VGroup()
        for i in range(4):
            a = Arrow(
                network[i].get_right(), network[i+1].get_left(),
                color=WHITE, stroke_width=1.5, buff=0.03,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(a)

        self.play(
            *[FadeIn(n) for n in network],
            *[GrowArrow(a) for a in arrows],
            run_time=1
        )

        idea = Text("Insert normalization after each layer!", font_size=16, color=YELLOW)
        idea.next_to(network, DOWN, buff=0.4)
        self.play(Write(idea), run_time=0.6)
        self.wait(1.5)

        self.play(FadeOut(VGroup(network, arrows, idea, sol)))

        # Step-by-step formula
        step_title = Text("Batch Norm: 3 Steps", font_size=24, color=YELLOW)
        step_title.next_to(title, DOWN, buff=0.35)
        self.play(Write(step_title), run_time=0.5)

        # Step 1: Compute mean & variance
        s1_label = Text("Step 1: Compute batch mean & variance", font_size=16, color=TEAL)
        s1_label.shift(UP * 0.8 + LEFT * 1)
        s1_eq = VGroup(
            MathTex(r"\mu_B = \frac{1}{m}\sum_{i=1}^{m} x_i", font_size=24, color=WHITE),
            MathTex(r"\sigma_B^2 = \frac{1}{m}\sum_{i=1}^{m}(x_i - \mu_B)^2", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(s1_label, DOWN, buff=0.2)

        self.play(Write(s1_label), run_time=0.5)
        self.play(Write(s1_eq), run_time=0.8)
        self.wait(0.5)

        # Step 2: Normalize
        s2_label = Text("Step 2: Normalize", font_size=16, color=GOLD)
        s2_label.next_to(s1_eq, DOWN, buff=0.3)
        s2_eq = MathTex(
            r"\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}",
            font_size=28, color=WHITE
        ).next_to(s2_label, DOWN, buff=0.15)

        self.play(Write(s2_label), run_time=0.4)
        self.play(Write(s2_eq), run_time=0.7)
        self.wait(0.5)

        # Step 3: Scale and shift
        s3_label = Text("Step 3: Scale & shift (learnable!)", font_size=16, color=GREEN)
        s3_label.next_to(s2_eq, DOWN, buff=0.3)
        s3_eq = MathTex(
            r"y_i = \gamma \hat{x}_i + \beta",
            font_size=30, color=WHITE
        ).next_to(s3_label, DOWN, buff=0.15)
        s3_box = SurroundingRectangle(s3_eq, color=GREEN, buff=0.12, corner_radius=0.08)

        self.play(Write(s3_label), run_time=0.4)
        self.play(Write(s3_eq), Create(s3_box), run_time=0.7)

        gamma_beta = VGroup(
            MathTex(r"\gamma", font_size=20, color=GREEN),
            Text(" = learned scale", font_size=13, color=GRAY),
            MathTex(r"\beta", font_size=20, color=GREEN),
            Text(" = learned shift", font_size=13, color=GRAY),
        )
        r1 = VGroup(gamma_beta[0], gamma_beta[1]).arrange(RIGHT, buff=0.05)
        r2 = VGroup(gamma_beta[2], gamma_beta[3]).arrange(RIGHT, buff=0.05)
        gb = VGroup(r1, r2).arrange(DOWN, buff=0.05, aligned_edge=LEFT).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(gb), run_time=0.5)
        self.wait(2)


class Part3_Effect(Scene):
    """Visual effect: before vs after Batch Norm on training."""
    def construct(self):
        title = Text("Batch Normalization", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        eff = Text("Effect on Training", font_size=24, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(eff), run_time=0.5)

        # Before: shifting distributions
        def gauss(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

        before_lbl = Text("Without Batch Norm", font_size=16, color=RED).shift(LEFT * 3.2 + UP * 0.7)
        ax_before = Axes(
            x_range=[-4, 6, 1], y_range=[0, 0.6, 0.1],
            x_length=4, y_length=2, axis_config={"stroke_width": 0.8, "include_ticks": False},
        ).shift(LEFT * 3.2 + DOWN * 0.8)

        c1 = ax_before.plot(lambda x: gauss(x, 0, 1), x_range=[-4, 4], color=GREEN, stroke_width=1.5)
        c2 = ax_before.plot(lambda x: gauss(x, 2, 1.5), x_range=[-2, 6], color=ORANGE, stroke_width=1.5)
        c3 = ax_before.plot(lambda x: gauss(x, -1, 0.7), x_range=[-4, 2], color=RED, stroke_width=1.5)

        e1 = Text("Epoch 1", font_size=10, color=GREEN).next_to(ax_before.c2p(0, 0.42), UP, buff=0.05)
        e2 = Text("Epoch 5", font_size=10, color=ORANGE).next_to(ax_before.c2p(2, 0.28), UP, buff=0.05)
        e3 = Text("Epoch 10", font_size=10, color=RED).next_to(ax_before.c2p(-1, 0.58), UP, buff=0.05)

        self.play(FadeIn(before_lbl), Create(ax_before), run_time=0.5)
        self.play(Create(c1), FadeIn(e1), run_time=0.5)
        self.play(Create(c2), FadeIn(e2), run_time=0.5)
        self.play(Create(c3), FadeIn(e3), run_time=0.5)

        shift_txt = Text("Distributions drift!", font_size=12, color=RED).next_to(ax_before, DOWN, buff=0.15)
        self.play(Write(shift_txt), run_time=0.3)

        # After: stable distributions
        after_lbl = Text("With Batch Norm", font_size=16, color=GREEN).shift(RIGHT * 3.2 + UP * 0.7)
        ax_after = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1],
            x_length=4, y_length=2, axis_config={"stroke_width": 0.8, "include_ticks": False},
        ).shift(RIGHT * 3.2 + DOWN * 0.8)

        ca1 = ax_after.plot(lambda x: gauss(x, 0, 1), x_range=[-4, 4], color=GREEN, stroke_width=1.5)
        ca2 = ax_after.plot(lambda x: gauss(x, 0.1, 1.05), x_range=[-4, 4], color=TEAL, stroke_width=1.5)
        ca3 = ax_after.plot(lambda x: gauss(x, -0.05, 0.95), x_range=[-4, 4], color=BLUE, stroke_width=1.5)

        ea1 = Text("Epoch 1", font_size=10, color=GREEN).next_to(ax_after.c2p(0, 0.42), UP, buff=0.05)
        ea2 = Text("Epoch 5", font_size=10, color=TEAL).next_to(ax_after.c2p(0.5, 0.39), UR, buff=0.05)
        ea3 = Text("Epoch 10", font_size=10, color=BLUE).next_to(ax_after.c2p(-0.5, 0.43), UL, buff=0.05)

        self.play(FadeIn(after_lbl), Create(ax_after), run_time=0.5)
        self.play(Create(ca1), FadeIn(ea1), run_time=0.5)
        self.play(Create(ca2), FadeIn(ea2), run_time=0.5)
        self.play(Create(ca3), FadeIn(ea3), run_time=0.5)

        stable_txt = Text("Distributions stable!", font_size=12, color=GREEN).next_to(ax_after, DOWN, buff=0.15)
        self.play(Write(stable_txt), run_time=0.3)
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            before_lbl, ax_before, c1, c2, c3, e1, e2, e3, shift_txt,
            after_lbl, ax_after, ca1, ca2, ca3, ea1, ea2, ea3, stable_txt, eff
        )))

        # Loss curve comparison
        loss_title = Text("Training Loss Comparison", font_size=22, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(loss_title), run_time=0.5)

        ax_loss = Axes(
            x_range=[0, 10, 2], y_range=[0, 1, 0.2],
            x_length=8, y_length=3,
            axis_config={"include_numbers": True, "font_size": 14, "stroke_width": 1},
            x_axis_config={"include_numbers": True},
        ).shift(DOWN * 0.8)
        x_lbl = Text("Epochs", font_size=14, color=GRAY).next_to(ax_loss.x_axis, DOWN, buff=0.15)
        y_lbl = Text("Loss", font_size=14, color=GRAY).next_to(ax_loss.y_axis, LEFT, buff=0.15).rotate(90 * DEGREES)

        # Without BN: slow, noisy descent
        no_bn = ax_loss.plot(
            lambda x: 0.9 * np.exp(-0.2 * x) + 0.05 * np.sin(3 * x) + 0.1,
            x_range=[0, 10], color=RED, stroke_width=2
        )
        # With BN: fast, smooth descent
        with_bn = ax_loss.plot(
            lambda x: 0.9 * np.exp(-0.5 * x) + 0.02,
            x_range=[0, 10], color=GREEN, stroke_width=2
        )

        lbl_no = Text("Without BN", font_size=13, color=RED).next_to(ax_loss.c2p(8, 0.35), RIGHT, buff=0.1)
        lbl_with = Text("With BN", font_size=13, color=GREEN).next_to(ax_loss.c2p(5, 0.05), RIGHT, buff=0.1)

        self.play(Create(ax_loss), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.6)
        self.play(Create(no_bn), FadeIn(lbl_no), run_time=1)
        self.play(Create(with_bn), FadeIn(lbl_with), run_time=1)

        takeaway = VGroup(
            Text("✓ Faster convergence", font_size=14, color=GREEN),
            Text("✓ Smoother loss landscape", font_size=14, color=GREEN),
            Text("✓ Allows higher learning rates", font_size=14, color=GREEN),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).to_edge(DOWN, buff=0.15)

        for t in takeaway:
            self.play(Write(t), run_time=0.3)
        self.wait(2)
