# LEAP_VERTICAL
from manim import *

class QuickVerticalTest(Scene):
    def construct(self):
        # Very simple scene to test 9:16 pipeline quickly
        title = Text("9:16 Test", font_size=48)
        title.to_edge(UP, buff=1.5)
        
        circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.6)
        
        label = Text("Vertical!", font_size=36, color=YELLOW)
        label.to_edge(DOWN, buff=1.5)
        
        self.play(Write(title), run_time=0.5)
        self.play(Create(circle), run_time=0.5)
        self.play(FadeIn(label), run_time=0.5)
        self.wait(1)
