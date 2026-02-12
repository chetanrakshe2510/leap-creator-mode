from manim import *

class Part1_Intro(Scene):
    """Part 1: Simple title card"""
    def construct(self):
        title = Text("Workflow Test", font_size=48, color=BLUE)
        subtitle = Text("Part 1: Introduction", font_size=24, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

class Part2_Animation(Scene):
    """Part 2: A simple animation"""
    def construct(self):
        circle = Circle(radius=1, color=GREEN)
        square = Square(side_length=2, color=RED)
        
        self.play(Create(circle), run_time=1)
        self.play(Transform(circle, square), run_time=1)
        self.wait(0.5)
        
        label = Text("Transform!", font_size=28, color=YELLOW).next_to(square, DOWN)
        self.play(Write(label), run_time=0.5)
        self.wait(1)
