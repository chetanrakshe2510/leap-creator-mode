from manim import *
import numpy as np

class HikerInTheValley(Scene):
    def construct(self):
        # ============================================================
        # PART 1: THE INPUT SPACE
        # ============================================================
        part1_title = Text("Part 1: The Input Space", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(part1_title))

        # Small pixel grid (3x3)
        grid_vals = np.array([
            [10, 200, 30],
            [180, 255, 50],
            [20, 210, 90]
        ])

        grid = VGroup()
        pixel_squares = VGroup()
        pixel_labels = VGroup()
        side = 0.9

        for i in range(3):
            for j in range(3):
                v = grid_vals[i][j]
                brightness = v / 255.0
                c = interpolate_color(BLACK, WHITE, brightness)
                sq = Square(side_length=side).set_fill(c, opacity=1).set_stroke(GRAY, 1)
                sq.move_to(np.array([j - 1, 1 - i, 0]) * side)
                tc = BLACK if brightness > 0.5 else WHITE
                lb = Integer(v, color=tc, font_size=22).move_to(sq)
                pixel_squares.add(sq)
                pixel_labels.add(lb)

        grid.add(pixel_squares, pixel_labels)
        grid.scale(0.8).shift(LEFT * 4 + DOWN * 0.5)

        img_title = Text("Image Pixels", font_size=22).next_to(grid, UP, buff=0.2)
        self.play(FadeIn(grid), Write(img_title))
        self.wait(0.5)

        # Highlight pixel with value 255
        highlight = SurroundingRectangle(pixel_squares[4], color=RED, buff=0.05)
        val_label = MathTex("x_1 = 255", color=RED, font_size=28).next_to(highlight, DOWN, buff=0.3)
        self.play(Create(highlight), Write(val_label))

        # Show weight scale
        weight_box = VGroup(
            Text("Weights", font_size=22),
            MathTex("w \\sim [0, 1]", font_size=28, color=BLUE)
        ).arrange(DOWN, buff=0.1).shift(RIGHT * 0 + DOWN * 0.5)

        self.play(FadeIn(weight_box))

        # Problem statement
        problem = Text("Inputs and Weights on vastly different scales!", font_size=22, color=RED)
        problem.next_to(weight_box, RIGHT, buff=0.5)
        self.play(Write(problem))
        self.wait(2)

        self.play(FadeOut(VGroup(grid, img_title, highlight, val_label, weight_box, problem, part1_title)))

        # ============================================================
        # PART 2: THE OPTIMIZATION LANDSCAPE
        # ============================================================
        part2_title = Text("Part 2: The Optimization Landscape", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(part2_title))

        # --- Scenario A: Unnormalized (Left Side) ---
        label_a = Text("Unnormalized", font_size=24, color=RED).shift(LEFT * 3.5 + UP * 2.5)
        self.play(Write(label_a))

        # Elongated ellipse contours (narrow valley)
        contours_a = VGroup()
        center_a = LEFT * 3.5 + DOWN * 0.3
        for k in range(1, 5):
            e = Ellipse(width=k * 0.4, height=k * 1.5, color=RED, stroke_opacity=0.3 + 0.15 * k)
            e.move_to(center_a)
            contours_a.add(e)

        axes_a = VGroup(
            Arrow(center_a + LEFT * 1.5, center_a + RIGHT * 1.5, buff=0, stroke_width=2),
            Arrow(center_a + DOWN * 3.5, center_a + UP * 3.5, buff=0, stroke_width=2),
            MathTex("w_1", font_size=20).next_to(center_a + RIGHT * 1.5, DOWN, buff=0.1),
            MathTex("w_2", font_size=20).next_to(center_a + UP * 3.5, RIGHT, buff=0.1),
        )

        star_a = Star(n=5, outer_radius=0.12, color=YELLOW).move_to(center_a).set_fill(YELLOW, 1)

        self.play(Create(axes_a), Create(contours_a), FadeIn(star_a))

        # Zig-zag path (the nightmare)
        zigzag_points = [
            center_a + UP * 2.8 + RIGHT * 0.6,
            center_a + UP * 2.2 + LEFT * 0.5,
            center_a + UP * 1.6 + RIGHT * 0.4,
            center_a + UP * 1.0 + LEFT * 0.3,
            center_a + UP * 0.5 + RIGHT * 0.25,
            center_a + UP * 0.2 + LEFT * 0.15,
            center_a + UP * 0.05,
        ]

        hiker_a = Dot(zigzag_points[0], color=ORANGE, radius=0.12)
        hiker_a_label = Text("Hiker", font_size=16, color=ORANGE).next_to(hiker_a, RIGHT, buff=0.1)
        self.play(FadeIn(hiker_a), Write(hiker_a_label))

        path_a = VGroup()
        for i in range(len(zigzag_points) - 1):
            seg = Line(zigzag_points[i], zigzag_points[i + 1], color=ORANGE, stroke_width=2)
            path_a.add(seg)
            self.play(
                hiker_a.animate.move_to(zigzag_points[i + 1]),
                Create(seg),
                run_time=0.4
            )
            hiker_a_label.next_to(hiker_a, RIGHT, buff=0.1)

        zigzag_text = Text("Zig-Zag! Slow!", color=RED, font_size=20).next_to(contours_a, DOWN, buff=0.3)
        self.play(Write(zigzag_text), FadeOut(hiker_a_label))

        # --- Scenario B: Normalized (Right Side) ---
        label_b = Text("Normalized", font_size=24, color=GREEN).shift(RIGHT * 3.5 + UP * 2.5)
        self.play(Write(label_b))

        # Circular contours (bowl)
        contours_b = VGroup()
        center_b = RIGHT * 3.5 + DOWN * 0.3
        for k in range(1, 5):
            c = Circle(radius=k * 0.6, color=GREEN, stroke_opacity=0.3 + 0.15 * k)
            c.move_to(center_b)
            contours_b.add(c)

        axes_b = VGroup(
            Arrow(center_b + LEFT * 3, center_b + RIGHT * 3, buff=0, stroke_width=2),
            Arrow(center_b + DOWN * 3, center_b + UP * 3, buff=0, stroke_width=2),
            MathTex("w_1", font_size=20).next_to(center_b + RIGHT * 3, DOWN, buff=0.1),
            MathTex("w_2", font_size=20).next_to(center_b + UP * 3, RIGHT, buff=0.1),
        )

        star_b = Star(n=5, outer_radius=0.12, color=YELLOW).move_to(center_b).set_fill(YELLOW, 1)

        self.play(Create(axes_b), Create(contours_b), FadeIn(star_b))

        # Straight path (the dream)
        start_b = center_b + UP * 2 + LEFT * 1.5
        straight_points = [
            start_b,
            center_b + (start_b - center_b) * 0.6,
            center_b + (start_b - center_b) * 0.25,
            center_b + (start_b - center_b) * 0.05,
        ]

        hiker_b = Dot(straight_points[0], color=GREEN, radius=0.12)
        hiker_b_label = Text("Hiker", font_size=16, color=GREEN).next_to(hiker_b, RIGHT, buff=0.1)
        self.play(FadeIn(hiker_b), Write(hiker_b_label))

        path_b = VGroup()
        for i in range(len(straight_points) - 1):
            seg = Line(straight_points[i], straight_points[i + 1], color=GREEN, stroke_width=2)
            path_b.add(seg)
            self.play(
                hiker_b.animate.move_to(straight_points[i + 1]),
                Create(seg),
                run_time=0.4
            )
            hiker_b_label.next_to(hiker_b, RIGHT, buff=0.1)

        straight_text = Text("Straight Shot! Fast!", color=GREEN, font_size=20).next_to(contours_b, DOWN, buff=0.3)
        self.play(Write(straight_text), FadeOut(hiker_b_label))
        self.wait(2)

        # Clear Part 2
        self.play(FadeOut(VGroup(
            part2_title, label_a, label_b, contours_a, contours_b,
            axes_a, axes_b, star_a, star_b, hiker_a, hiker_b,
            path_a, path_b, zigzag_text, straight_text
        )))

        # ============================================================
        # PART 3: THE EXPLODING GRADIENT PROBLEM
        # ============================================================
        part3_title = Text("Part 3: Gradient Saturation", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(part3_title))

        # Neuron equation
        equation = MathTex("z = w \\cdot x + b", font_size=40).shift(UP * 2)
        self.play(Write(equation))

        # Sigmoid plot (shared)
        sig_axes = Axes(
            x_range=[-8, 8, 2],
            y_range=[0, 1.2, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_numbers": True, "font_size": 18}
        ).shift(DOWN * 1)

        sig_curve = sig_axes.plot(lambda x: 1 / (1 + np.exp(-x)), color=WHITE)
        sig_label = MathTex(r"\sigma(z)", font_size=24).next_to(sig_axes, LEFT)

        self.play(Create(sig_axes), Create(sig_curve), Write(sig_label))

        # Scenario A: Unnormalized x=255, w=0.5
        calc_a = MathTex(
            "x=255,\\;w=0.5", "\\Rightarrow", "z=127.5",
            font_size=28
        ).next_to(equation, DOWN, buff=0.3)
        calc_a[0].set_color(RED)
        calc_a[2].set_color(RED)

        self.play(Write(calc_a))

        # z=127.5 is WAY off chart. Show dot at saturation edge.
        dot_sat = Dot(sig_axes.c2p(7.5, 1), color=RED, radius=0.12)
        sat_label = Text("Saturated! Gradient ~ 0", font_size=18, color=RED).next_to(dot_sat, UP)
        arrow_sat = Arrow(sig_axes.c2p(7.5, 0.5), dot_sat.get_center(), color=RED, buff=0.1)

        self.play(GrowArrow(arrow_sat), FadeIn(dot_sat), Write(sat_label))
        self.wait(1)

        # Scenario B: Normalized x=1, w=0.5
        calc_b = MathTex(
            "x=1,\\;w=0.5", "\\Rightarrow", "z=0.5",
            font_size=28
        ).next_to(calc_a, DOWN, buff=0.2)
        calc_b[0].set_color(GREEN)
        calc_b[2].set_color(GREEN)

        self.play(Write(calc_b))

        sig_val = 1 / (1 + np.exp(-0.5))
        dot_active = Dot(sig_axes.c2p(0.5, sig_val), color=GREEN, radius=0.12)
        active_label = Text("Active! Learning!", font_size=18, color=GREEN).next_to(dot_active, DOWN)

        # Tangent line to show gradient
        tangent = sig_axes.get_secant_slope_group(
            x=0.5,
            graph=sig_curve,
            dx=0.01,
            secant_line_color=GREEN,
            secant_line_length=3
        )

        self.play(FadeIn(dot_active), Write(active_label), Create(tangent.secant_line))
        self.wait(3)
