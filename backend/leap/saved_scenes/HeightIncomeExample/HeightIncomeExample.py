from manim import *
import numpy as np

class Part1_Dataset(Scene):
    """Show the dataset and the problem setup."""
    def construct(self):
        title = Text("Standardization: A Concrete Example", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # Two features
        feat_info = VGroup(
            VGroup(
                Text("Height (cm)", font_size=18, color=GREEN),
                MathTex(r"\approx 170 \pm 10", font_size=20, color=GREEN_B),
            ).arrange(DOWN, buff=0.1),
            VGroup(
                Text("Income (₹)", font_size=18, color=RED),
                MathTex(r"\approx 50{,}000 \pm 20{,}000", font_size=20, color=RED_B),
            ).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=1.5).next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(feat_info), run_time=0.6)
        self.wait(0.5)

        # Dataset table
        table_title = Text("Dataset", font_size=20, color=YELLOW).shift(UP * 0.2 + LEFT * 4)

        # Header
        header = VGroup(
            Text("Height", font_size=14, color=GRAY),
            Text("Income", font_size=14, color=GRAY),
            Text("Class", font_size=14, color=GRAY),
        ).arrange(RIGHT, buff=0.8)

        # Rows
        rows_data = [
            ("160", "30,000", "A", TEAL),
            ("170", "40,000", "A", TEAL),
            ("180", "70,000", "B", ORANGE),
            ("175", "90,000", "B", ORANGE),
        ]
        rows = VGroup()
        for h, inc, cls, clr in rows_data:
            row = VGroup(
                Text(h, font_size=14, color=WHITE),
                Text(inc, font_size=14, color=WHITE),
                Text(cls, font_size=14, color=clr),
            ).arrange(RIGHT, buff=0.8)
            rows.add(row)

        table = VGroup(header, *rows).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        table.shift(DOWN * 1.2)

        # Separator line
        sep = Line(
            header.get_left() + DOWN * 0.12 + LEFT * 0.2,
            header.get_right() + DOWN * 0.12 + RIGHT * 0.2,
            color=GRAY, stroke_width=1
        )

        self.play(Write(table_title), run_time=0.3)
        self.play(FadeIn(header), Create(sep), run_time=0.4)
        for row in rows:
            self.play(FadeIn(row), run_time=0.3)

        # Plot the data
        ax = Axes(
            x_range=[155, 185, 5], y_range=[20000, 100000, 20000],
            x_length=4, y_length=3,
            axis_config={"include_numbers": False, "stroke_width": 1},
        ).shift(RIGHT * 3.5 + DOWN * 1)
        x_lbl = Text("Height", font_size=12, color=GREEN).next_to(ax.x_axis, DOWN, buff=0.1)
        y_lbl = Text("Income", font_size=12, color=RED).next_to(ax.y_axis, LEFT, buff=0.1).rotate(90 * DEGREES)

        dots = VGroup(
            Dot(ax.c2p(160, 30000), color=TEAL, radius=0.08),
            Dot(ax.c2p(170, 40000), color=TEAL, radius=0.08),
            Dot(ax.c2p(180, 70000), color=ORANGE, radius=0.08),
            Dot(ax.c2p(175, 90000), color=ORANGE, radius=0.08),
        )
        labels_plot = VGroup(
            Text("A", font_size=10, color=TEAL).next_to(dots[0], DL, buff=0.05),
            Text("A", font_size=10, color=TEAL).next_to(dots[1], DL, buff=0.05),
            Text("B", font_size=10, color=ORANGE).next_to(dots[2], UR, buff=0.05),
            Text("B", font_size=10, color=ORANGE).next_to(dots[3], UR, buff=0.05),
        )

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.6)
        self.play(FadeIn(dots), FadeIn(labels_plot), run_time=0.5)
        self.wait(2)


class Part2_Without(Scene):
    """Without standardization — income dominates distance."""
    def construct(self):
        title = Text("Standardization: A Concrete Example", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        warn = Text("⚠ Without Standardization", font_size=24, color=RED)
        warn.next_to(title, DOWN, buff=0.35)
        self.play(Write(warn), run_time=0.6)

        # Distance formula
        dist_eq = MathTex(
            r"d = \sqrt{(h_1 - h_2)^2 + (i_1 - i_2)^2}",
            font_size=28, color=WHITE
        ).next_to(warn, DOWN, buff=0.4)
        self.play(Write(dist_eq), run_time=0.8)

        # Example: distance between student 1 (160,30k) and student 3 (180,70k)
        example = Text("Distance: Student 1 → Student 3", font_size=16, color=GRAY)
        example.next_to(dist_eq, DOWN, buff=0.4)
        self.play(Write(example), run_time=0.4)

        calc = VGroup(
            MathTex(r"d = \sqrt{(160-180)^2 + (30000-70000)^2}", font_size=22, color=WHITE),
            MathTex(r"= \sqrt{(-20)^2 + (-40000)^2}", font_size=22, color=WHITE),
            MathTex(r"= \sqrt{400 + 1{,}600{,}000{,}000}", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(example, DOWN, buff=0.3)

        self.play(Write(calc[0]), run_time=0.7)
        self.play(Write(calc[1]), run_time=0.6)
        self.play(Write(calc[2]), run_time=0.6)

        # Highlight the disparity
        height_box = SurroundingRectangle(
            MathTex(r"400", font_size=22).move_to(calc[2][0][1:4]),
            color=GREEN, buff=0.05
        )

        compare = VGroup(
            VGroup(
                Text("Height²", font_size=16, color=GREEN),
                Text("= 400", font_size=16, color=GREEN),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("Income²", font_size=16, color=RED),
                Text("= 1,600,000,000", font_size=16, color=RED),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(calc, DOWN, buff=0.4)

        self.play(FadeIn(compare[0]), run_time=0.4)
        self.play(FadeIn(compare[1]), run_time=0.4)

        ratio = MathTex(
            r"\text{Income}^2 \text{ is } 4{,}000{,}000\times \text{ larger!}",
            font_size=22, color=YELLOW
        ).next_to(compare, DOWN, buff=0.25)
        self.play(Write(ratio), run_time=0.7)

        conclusion = Text("→ Model ignores height entirely!", font_size=18, color=RED)
        conclusion.to_edge(DOWN, buff=0.2)
        self.play(Write(conclusion), run_time=0.6)
        self.wait(2)


class Part3_After(Scene):
    """After standardization — both features contribute equally."""
    def construct(self):
        title = Text("Standardization: A Concrete Example", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.5)

        fix = Text("✅ After Standardization", font_size=24, color=GREEN)
        fix.next_to(title, DOWN, buff=0.35)
        self.play(Write(fix), run_time=0.6)

        # Show Z-score formula
        formula = MathTex(r"Z = \frac{X - \mu}{\sigma}", font_size=28, color=WHITE)
        formula.next_to(fix, DOWN, buff=0.3)
        self.play(Write(formula), run_time=0.5)

        # Compute stats
        stats = VGroup(
            VGroup(
                Text("Height:", font_size=16, color=GREEN),
                MathTex(r"\mu=171.25,\; \sigma=7.5", font_size=18, color=GREEN_B),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Text("Income:", font_size=16, color=RED),
                MathTex(r"\mu=57500,\; \sigma=22500", font_size=18, color=RED_B),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(formula, DOWN, buff=0.35)
        self.play(FadeIn(stats), run_time=0.6)
        self.wait(0.5)

        # Show standardized values
        self.play(FadeOut(VGroup(formula, stats)))

        # Standardized table
        table_title = Text("Standardized Values", font_size=18, color=YELLOW).next_to(fix, DOWN, buff=0.35)
        header = VGroup(
            Text("Z_height", font_size=13, color=GREEN),
            Text("Z_income", font_size=13, color=RED),
            Text("Class", font_size=13, color=GRAY),
        ).arrange(RIGHT, buff=0.6)

        # Heights: [160,170,180,175], mu=171.25, sigma~7.5
        # Incomes: [30k,40k,70k,90k], mu=57500, sigma~22500
        rows_data = [
            ("-1.50", "-1.22", "A", TEAL),
            ("-0.17", "-0.78", "A", TEAL),
            ("1.17", "0.56", "B", ORANGE),
            ("0.50", "1.44", "B", ORANGE),
        ]
        rows = VGroup()
        for zh, zi, cls, clr in rows_data:
            row = VGroup(
                Text(zh, font_size=13, color=WHITE),
                Text(zi, font_size=13, color=WHITE),
                Text(cls, font_size=13, color=clr),
            ).arrange(RIGHT, buff=0.7)
            rows.add(row)

        table = VGroup(header, *rows).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        table.next_to(table_title, DOWN, buff=0.25)
        sep = Line(
            header.get_left() + DOWN * 0.1 + LEFT * 0.1,
            header.get_right() + DOWN * 0.1 + RIGHT * 0.1,
            color=GRAY, stroke_width=1
        )

        self.play(Write(table_title), run_time=0.3)
        self.play(FadeIn(header), Create(sep), run_time=0.3)
        for r in rows:
            self.play(FadeIn(r), run_time=0.25)
        self.wait(0.5)

        # New distance
        new_dist = VGroup(
            Text("New distance formula:", font_size=16, color=GRAY),
            MathTex(r"d = \sqrt{Z_h^2 + Z_i^2}", font_size=24, color=WHITE),
            Text("Both features contribute equally!", font_size=16, color=GREEN),
        ).arrange(DOWN, buff=0.15).next_to(table, DOWN, buff=0.35)

        self.play(Write(new_dist[0]), run_time=0.3)
        self.play(Write(new_dist[1]), run_time=0.5)
        self.play(Write(new_dist[2]), run_time=0.5)
        self.wait(1)

        self.play(FadeOut(VGroup(table_title, header, sep, *rows, new_dist, fix)))

        # Side-by-side scatter comparison
        comp = Text("Before vs After: Geometric View", font_size=22, color=YELLOW)
        comp.next_to(title, DOWN, buff=0.35)
        self.play(Write(comp), run_time=0.5)

        # Before: elongated scatter
        ax_before = Axes(
            x_range=[155, 185, 10], y_range=[20000, 100000, 20000],
            x_length=3.5, y_length=2.5,
            axis_config={"include_numbers": False, "stroke_width": 0.8},
        ).shift(LEFT * 3.2 + DOWN * 1)
        lbl_bx = Text("Height", font_size=10, color=GREEN).next_to(ax_before.x_axis, DOWN, buff=0.08)
        lbl_by = Text("Income", font_size=10, color=RED).next_to(ax_before.y_axis, LEFT, buff=0.08).rotate(90*DEGREES)
        before_title = Text("Raw Data", font_size=14, color=RED).next_to(ax_before, UP, buff=0.15)

        dots_b = VGroup(
            Dot(ax_before.c2p(160, 30000), color=TEAL, radius=0.07),
            Dot(ax_before.c2p(170, 40000), color=TEAL, radius=0.07),
            Dot(ax_before.c2p(180, 70000), color=ORANGE, radius=0.07),
            Dot(ax_before.c2p(175, 90000), color=ORANGE, radius=0.07),
        )

        self.play(
            Create(ax_before), FadeIn(lbl_bx), FadeIn(lbl_by),
            FadeIn(before_title), FadeIn(dots_b),
            run_time=0.8
        )

        # After: balanced scatter
        ax_after = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=3.5, y_length=2.5,
            axis_config={"include_numbers": False, "stroke_width": 0.8},
        ).shift(RIGHT * 3.2 + DOWN * 1)
        lbl_ax = MathTex(r"Z_h", font_size=14, color=GREEN).next_to(ax_after.x_axis, DOWN, buff=0.08)
        lbl_ay = MathTex(r"Z_i", font_size=14, color=RED).next_to(ax_after.y_axis, LEFT, buff=0.08)
        after_title = Text("Standardized", font_size=14, color=GREEN).next_to(ax_after, UP, buff=0.15)

        dots_a = VGroup(
            Dot(ax_after.c2p(-1.5, -1.22), color=TEAL, radius=0.07),
            Dot(ax_after.c2p(-0.17, -0.78), color=TEAL, radius=0.07),
            Dot(ax_after.c2p(1.17, 0.56), color=ORANGE, radius=0.07),
            Dot(ax_after.c2p(0.5, 1.44), color=ORANGE, radius=0.07),
        )

        self.play(
            Create(ax_after), FadeIn(lbl_ax), FadeIn(lbl_ay),
            FadeIn(after_title), FadeIn(dots_a),
            run_time=0.8
        )

        # Insight
        insight = Text("Classifier sees true geometric structure, not scale bias!", font_size=16, color=YELLOW)
        insight.to_edge(DOWN, buff=0.2)
        self.play(Write(insight), run_time=0.8)
        self.wait(2)
