from manim import *
import numpy as np

class Part1_WhyGD(Scene):
    """Why gradient descent is needed — the loss function."""
    def construct(self):
        title = Text("Why Gradient Descent in ML?", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # Linear regression model
        model_lbl = Text("Linear Regression Model", font_size=22, color=YELLOW)
        model_lbl.next_to(title, DOWN, buff=0.4)
        self.play(Write(model_lbl), run_time=0.5)

        model_eq = MathTex(r"\hat{y} = wx + b", font_size=34, color=WHITE)
        model_eq.next_to(model_lbl, DOWN, buff=0.3)
        self.play(Write(model_eq), run_time=0.6)

        params = VGroup(
            VGroup(MathTex(r"w", font_size=22, color=GREEN), Text(" = weight (slope)", font_size=14, color=GRAY)).arrange(RIGHT, buff=0.1),
            VGroup(MathTex(r"b", font_size=22, color=GREEN), Text(" = bias (intercept)", font_size=14, color=GRAY)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(model_eq, DOWN, buff=0.25)
        self.play(FadeIn(params), run_time=0.5)
        self.wait(0.5)

        # Loss function
        self.play(FadeOut(VGroup(model_lbl, params)))
        loss_lbl = Text("Loss Function (Mean Squared Error)", font_size=20, color=RED)
        loss_lbl.next_to(title, DOWN, buff=0.4)
        self.play(Write(loss_lbl), run_time=0.5)

        loss_eq = MathTex(
            r"\mathcal{L} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2",
            font_size=34, color=WHITE
        ).next_to(model_eq, DOWN, buff=0.3)
        loss_box = SurroundingRectangle(loss_eq, color=RED, buff=0.12, corner_radius=0.08)
        self.play(Write(loss_eq), Create(loss_box), run_time=0.8)

        # Expand
        expand = MathTex(
            r"= \frac{1}{n}\sum_{i=1}^{n}(y_i - (wx_i + b))^2",
            font_size=28, color=GRAY
        ).next_to(loss_box, DOWN, buff=0.3)
        self.play(Write(expand), run_time=0.7)

        insight = Text("Loss depends on w and b — we need to find the best values!", font_size=16, color=YELLOW)
        insight.next_to(expand, DOWN, buff=0.3)
        self.play(Write(insight), run_time=0.7)
        self.wait(1)

        cant = Text("We cannot guess optimal w → we use Gradient Descent", font_size=18, color=GREEN)
        cant.to_edge(DOWN, buff=0.2)
        self.play(Write(cant), run_time=0.7)
        self.wait(2)


class Part2_Gradients(Scene):
    """Derive the gradients for linear regression."""
    def construct(self):
        title = Text("Computing the Gradients", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        # Start from loss
        loss = MathTex(
            r"\mathcal{L} = \frac{1}{n}\sum(y_i - wx_i - b)^2",
            font_size=28, color=WHITE
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(loss), run_time=0.6)

        # Gradient w.r.t w
        gw_label = Text("Gradient w.r.t. w:", font_size=18, color=GREEN)
        gw_label.next_to(loss, DOWN, buff=0.4).align_to(loss, LEFT)
        self.play(Write(gw_label), run_time=0.3)

        gw = MathTex(
            r"\frac{\partial \mathcal{L}}{\partial w} = \frac{-2}{n}\sum_{i=1}^{n} x_i(y_i - \hat{y}_i)",
            font_size=26, color=WHITE
        ).next_to(gw_label, DOWN, buff=0.15)
        self.play(Write(gw), run_time=0.8)

        # Gradient w.r.t b
        gb_label = Text("Gradient w.r.t. b:", font_size=18, color=TEAL)
        gb_label.next_to(gw, DOWN, buff=0.3).align_to(loss, LEFT)
        self.play(Write(gb_label), run_time=0.3)

        gb = MathTex(
            r"\frac{\partial \mathcal{L}}{\partial b} = \frac{-2}{n}\sum_{i=1}^{n} (y_i - \hat{y}_i)",
            font_size=26, color=WHITE
        ).next_to(gb_label, DOWN, buff=0.15)
        self.play(Write(gb), run_time=0.8)

        # Update rules
        update_lbl = Text("Update Rules:", font_size=18, color=GOLD)
        update_lbl.next_to(gb, DOWN, buff=0.4).align_to(loss, LEFT)
        self.play(Write(update_lbl), run_time=0.3)

        updates = VGroup(
            MathTex(r"w \leftarrow w - \alpha \frac{\partial \mathcal{L}}{\partial w}", font_size=26, color=WHITE),
            MathTex(r"b \leftarrow b - \alpha \frac{\partial \mathcal{L}}{\partial b}", font_size=26, color=WHITE),
        ).arrange(RIGHT, buff=1).next_to(update_lbl, DOWN, buff=0.15)
        updates_box = SurroundingRectangle(updates, color=GOLD, buff=0.12, corner_radius=0.08)

        self.play(Write(updates), Create(updates_box), run_time=0.8)
        self.wait(2)


class Part3_Visual(Scene):
    """Visual: animated line fitting with GD iterations."""
    def construct(self):
        title = Text("Gradient Descent in Action", font_size=36, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        # Data points
        np.random.seed(42)
        true_w, true_b = 2.0, 1.0
        xs = np.array([1, 2, 3, 4, 5], dtype=float)
        ys = true_w * xs + true_b + np.random.randn(5) * 0.5

        ax = Axes(
            x_range=[0, 6, 1], y_range=[0, 12, 2],
            x_length=6, y_length=4,
            axis_config={"include_numbers": True, "font_size": 12, "stroke_width": 1},
        ).shift(DOWN * 0.5 + LEFT * 0.5)
        x_lbl = MathTex(r"x", font_size=16, color=GRAY).next_to(ax.x_axis, DOWN, buff=0.15)
        y_lbl = MathTex(r"y", font_size=16, color=GRAY).next_to(ax.y_axis, LEFT, buff=0.15)

        dots = VGroup(*[Dot(ax.c2p(x, y), color=TEAL, radius=0.06) for x, y in zip(xs, ys)])

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(dots), run_time=0.8)

        # Start with a bad line
        w, b = 0.5, 0.0
        alpha = 0.01

        line = ax.plot(lambda x: w * x + b, x_range=[0, 6], color=YELLOW, stroke_width=2)
        param_text = MathTex(f"w = {w:.2f},\\; b = {b:.2f}", font_size=18, color=YELLOW)
        param_text.to_edge(RIGHT, buff=0.3).shift(UP * 0.5)
        self.play(Create(line), FadeIn(param_text), run_time=0.5)

        # Show error lines for iteration 0
        error_lines = VGroup()
        for x_val, y_val in zip(xs, ys):
            y_hat = w * x_val + b
            err_line = DashedLine(
                ax.c2p(x_val, y_val), ax.c2p(x_val, y_hat),
                color=RED, stroke_width=1
            )
            error_lines.add(err_line)
        self.play(Create(error_lines), run_time=0.5)

        loss_val = np.mean((ys - (w * xs + b))**2)
        loss_text = MathTex(f"\\mathcal{{L}} = {loss_val:.2f}", font_size=18, color=RED)
        loss_text.next_to(param_text, DOWN, buff=0.3)
        self.play(FadeIn(loss_text), run_time=0.3)
        self.wait(0.5)

        # GD iterations
        iter_lbl = Text("Iteration 0", font_size=14, color=GRAY).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)
        self.play(FadeIn(iter_lbl), run_time=0.2)

        for iteration in range(1, 13):
            # Compute gradients
            y_hat = w * xs + b
            residuals = ys - y_hat
            dw = (-2 / len(xs)) * np.sum(xs * residuals)
            db = (-2 / len(xs)) * np.sum(residuals)

            # Update
            w = w - alpha * dw
            b = b - alpha * db

            # New line
            new_line = ax.plot(lambda x, ww=w, bb=b: ww * x + bb, x_range=[0, 6], color=YELLOW, stroke_width=2)
            new_param = MathTex(f"w = {w:.2f},\\; b = {b:.2f}", font_size=18, color=YELLOW)
            new_param.to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

            loss_val = np.mean((ys - (w * xs + b))**2)
            new_loss = MathTex(f"\\mathcal{{L}} = {loss_val:.2f}", font_size=18, color=RED)
            new_loss.next_to(new_param, DOWN, buff=0.3)

            new_iter = Text(f"Iteration {iteration}", font_size=14, color=GRAY)
            new_iter.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)

            # New error lines
            new_errors = VGroup()
            for x_val, y_val in zip(xs, ys):
                yh = w * x_val + b
                err_line = DashedLine(
                    ax.c2p(x_val, y_val), ax.c2p(x_val, yh),
                    color=RED, stroke_width=1
                )
                new_errors.add(err_line)

            speed = 0.5 if iteration <= 4 else 0.25
            self.play(
                Transform(line, new_line),
                Transform(param_text, new_param),
                Transform(loss_text, new_loss),
                Transform(error_lines, new_errors),
                Transform(iter_lbl, new_iter),
                run_time=speed
            )
            if iteration <= 3:
                self.wait(0.2)

        # Final
        self.play(FadeOut(error_lines), run_time=0.3)

        final = VGroup(
            Text("Line converges to fit the data!", font_size=16, color=GREEN),
            MathTex(f"w \\approx {w:.2f} \\; (\\text{{true: }} {true_w})", font_size=18, color=GREEN),
            MathTex(f"b \\approx {b:.2f} \\; (\\text{{true: }} {true_b})", font_size=18, color=GREEN),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.15)
        self.play(Write(final[0]), run_time=0.4)
        self.play(FadeIn(final[1]), FadeIn(final[2]), run_time=0.5)

        # The 4-step cycle
        self.wait(1)
        self.play(FadeOut(VGroup(final, line, param_text, loss_text, iter_lbl, ax, dots, x_lbl, y_lbl)))

        cycle_title = Text("The Training Loop", font_size=26, color=YELLOW).next_to(title, DOWN, buff=0.35)
        self.play(Write(cycle_title), run_time=0.4)

        steps = VGroup(
            VGroup(
                Text("1", font_size=20, color=BLACK).set_z_index(1),
                Circle(radius=0.2, color=GREEN, fill_opacity=1),
            ).arrange(ORIGIN),
            VGroup(
                Text("2", font_size=20, color=BLACK).set_z_index(1),
                Circle(radius=0.2, color=TEAL, fill_opacity=1),
            ).arrange(ORIGIN),
            VGroup(
                Text("3", font_size=20, color=BLACK).set_z_index(1),
                Circle(radius=0.2, color=BLUE, fill_opacity=1),
            ).arrange(ORIGIN),
            VGroup(
                Text("4", font_size=20, color=BLACK).set_z_index(1),
                Circle(radius=0.2, color=PURPLE, fill_opacity=1),
            ).arrange(ORIGIN),
        )

        labels = VGroup(
            Text("Random w, b", font_size=14, color=GREEN),
            Text("Compute error", font_size=14, color=TEAL),
            Text("Compute gradient", font_size=14, color=BLUE),
            Text("Update weights", font_size=14, color=PURPLE),
        )

        # Arrange in a cycle
        positions = [UP * 0.5, RIGHT * 2.5 + DOWN * 0.8, DOWN * 2, LEFT * 2.5 + DOWN * 0.8]
        for step, lbl, pos in zip(steps, labels, positions):
            step.move_to(pos)
            lbl.next_to(step, DOWN, buff=0.15)

        arrows = VGroup()
        for i in range(4):
            j = (i + 1) % 4
            a = Arrow(
                steps[i].get_center(), steps[j].get_center(),
                color=WHITE, stroke_width=1.5, buff=0.3,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(a)

        for i in range(4):
            self.play(FadeIn(steps[i]), FadeIn(labels[i]), GrowArrow(arrows[i]), run_time=0.4)

        repeat = Text("Repeat until convergence!", font_size=18, color=YELLOW)
        repeat.to_edge(DOWN, buff=0.2)
        self.play(Write(repeat), run_time=0.5)
        self.wait(2)
