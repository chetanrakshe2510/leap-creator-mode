from manim import *
import numpy as np

class BeamEquilibriumPart2B_Table(Scene):
    def construct(self):
        title = Text("GATE Insights (2/2) - Table", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))

        deg_title = Text("Degree of Curves", font_size=22, color=YELLOW).shift(UP * 0.8)
        self.play(Write(deg_title))

        col_x = [-3.5, 0, 3.5]
        headers = VGroup(
            Text("Load w(x)", font_size=18, color=RED).move_to([col_x[0], 0.2, 0]),
            Text("SFD (V)", font_size=18, color=GREEN).move_to([col_x[1], 0.2, 0]),
            Text("BMD (M)", font_size=18, color=PURPLE).move_to([col_x[2], 0.2, 0]),
        )
        h_line = Line(LEFT * 5.5 + DOWN * 0.05, RIGHT * 5.5 + DOWN * 0.05, color=GRAY, stroke_width=1)

        row1 = VGroup(
            Text("Constant (0th)", font_size=16, color=RED).move_to([col_x[0], -0.5, 0]),
            Text("Linear (1st)", font_size=16, color=GREEN).move_to([col_x[1], -0.5, 0]),
            Text("Parabolic (2nd)", font_size=16, color=PURPLE).move_to([col_x[2], -0.5, 0]),
        )
        row2 = VGroup(
            Text("Triangular (1st)", font_size=16, color=RED).move_to([col_x[0], -1.1, 0]),
            Text("Parabolic (2nd)", font_size=16, color=GREEN).move_to([col_x[1], -1.1, 0]),
            Text("Cubic (3rd)", font_size=16, color=PURPLE).move_to([col_x[2], -1.1, 0]),
        )

        h_line2 = Line(LEFT * 5.5 + DOWN * 1.5, RIGHT * 5.5 + DOWN * 1.5, color=GRAY, stroke_width=1)

        arr1 = Arrow(LEFT * 0.3, RIGHT * 0.3, color=GRAY, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.4).move_to([-1.75, -0.5, 0])
        arr2 = Arrow(LEFT * 0.3, RIGHT * 0.3, color=GRAY, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.4).move_to([1.75, -0.5, 0])
        arr3 = Arrow(LEFT * 0.3, RIGHT * 0.3, color=GRAY, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.4).move_to([-1.75, -1.1, 0])
        arr4 = Arrow(LEFT * 0.3, RIGHT * 0.3, color=GRAY, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.4).move_to([1.75, -1.1, 0])

        self.play(FadeIn(headers), Create(h_line))
        self.play(FadeIn(row1), GrowArrow(arr1), GrowArrow(arr2))
        self.play(FadeIn(row2), GrowArrow(arr3), GrowArrow(arr4))
        self.play(Create(h_line2))
        self.wait(2)

class BeamEquilibriumPart2B_Plots(Scene):
    def construct(self):
        # title = Text("GATE Insights (2/2) - Plots", font_size=36, color=BLUE).to_edge(UP)
        # self.play(Write(title))

        col_x = [-3.5, 0, 3.5]
        
        # Mini plots only
        def make_small_ax(pos):
            return Axes(x_range=[0, 3, 1], y_range=[-1, 1, 0.5],
                       x_length=2.2, y_length=0.8,
                       axis_config={"include_numbers": False, "stroke_width": 0.8}).move_to(pos)

        ax1 = make_small_ax([col_x[0], -2, 0])
        c1 = ax1.plot(lambda x: 0.5, x_range=[0, 3, 0.02], color=RED, stroke_width=2)
        ax2 = make_small_ax([col_x[1], -2, 0])
        c2 = ax2.plot(lambda x: 0.8 - 0.5*x, x_range=[0, 3, 0.02], color=GREEN, stroke_width=2)
        ax3 = make_small_ax([col_x[2], -2, 0])
        c3 = ax3.plot(lambda x: -0.15*(x-1.5)**2 + 0.5, x_range=[0, 3, 0.02], color=PURPLE, stroke_width=2)

        self.play(FadeIn(VGroup(ax1, c1, ax2, c2, ax3, c3)))

        # summary = Text("Each integration raises the degree by 1", font_size=16, color=GRAY).to_edge(DOWN)
        # self.play(Write(summary))
        self.wait(3)
