# LEAP_VERTICAL
from manim import *

class VerticalDemo(Scene):
    def construct(self):
        # When running with -r 1080,1920 (triggered by # LEAP_VERTICAL),
        # The frame height remains 8.0 (default), but frame width becomes 4.5
        # (Aspect Ratio 9:16)
        
        # Title at the top
        title = Text("Vertical Mode", font_size=48)
        title.to_edge(UP, buff=1.0)
        
        # Center content
        circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.5)
        square = Square(side_length=3, color=RED, fill_opacity=0.5)
        
        # Footer
        footer = Text("9:16 Aspect Ratio", font_size=36, color=GRAY)
        footer.to_edge(DOWN, buff=1.0)
        
        # Animations
        self.play(Write(title))
        self.play(GrowFromCenter(circle))
        self.wait(0.5)
        
        self.play(Transform(circle, square))
        self.play(Rotate(square, PI/4))
        
        self.play(FadeIn(footer, shift=UP))
        self.wait(2)
