from manim import *

class SquareSumFormula(Scene):
    def construct(self):
        # Configuration
        a = 2
        b = 1
        
        # Colors
        color_a2 = BLUE
        color_b2 = GREEN
        color_ab = ORANGE
        
        # Create shapes
        square_a = Square(side_length=a).set_fill(color_a2, opacity=0.5).set_stroke(color_a2)
        square_b = Square(side_length=b).set_fill(color_b2, opacity=0.5).set_stroke(color_b2)
        rect_ab1 = Rectangle(height=a, width=b).set_fill(color_ab, opacity=0.5).set_stroke(color_ab)
        rect_ab2 = Rectangle(height=b, width=a).set_fill(color_ab, opacity=0.5).set_stroke(color_ab)
        
        # Labels
        label_a2 = MathTex("a^2").move_to(square_a.get_center())
        label_b2 = MathTex("b^2").move_to(square_b.get_center())
        label_ab1 = MathTex("ab").move_to(rect_ab1.get_center())
        label_ab2 = MathTex("ab").move_to(rect_ab2.get_center())
        
        # Group them for easier manipulation
        part_a2 = VGroup(square_a, label_a2)
        part_b2 = VGroup(square_b, label_b2)
        part_ab1 = VGroup(rect_ab1, label_ab1)
        part_ab2 = VGroup(rect_ab2, label_ab2)
        
        # Arrange initially separated
        parts = VGroup(part_a2, part_ab1, part_ab2, part_b2).arrange(RIGHT, buff=0.5)
        
        # Title
        title = MathTex("(a+b)^2 = a^2 + 2ab + b^2").to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Introduce parts
        self.play(FadeIn(parts))
        self.wait(1)
        
        # Animate assembly into a big square
        # Target positions relative to a center point
        center = ORIGIN + DOWN * 0.5
        
        # Position logic:
        # Top-Left: a^2
        # Top-Right: ab (height a, width b)
        # Bottom-Left: ab (height b, width a)
        # Bottom-Right: b^2
        
        # Offset calculations to center the whole (a+b) square
        total_side = a + b
        offset = center - np.array([total_side/2, total_side/2, 0])
        
        # Manually move to forming positions
        # Top-Left corner of square_a is at (0, total_side) relative to bottom-left of big square
        # Let's align them relative to each other first
        
        self.play(
            part_a2.animate.move_to(center + np.array([-b/2, b/2, 0])),
            part_ab1.animate.move_to(center + np.array([a/2, b/2, 0])),
            part_ab2.animate.move_to(center + np.array([-b/2, -a/2, 0])),
            part_b2.animate.move_to(center + np.array([a/2, -a/2, 0])),
            run_time=2
        )
        self.wait(1)
        
        # Brace for side lengths
        brace_left = Brace(VGroup(square_a, rect_ab2), LEFT)
        brace_bottom = Brace(VGroup(rect_ab2, square_b), DOWN)
        
        label_left = brace_left.get_text("a+b")
        label_bottom = brace_bottom.get_text("a+b")
        
        self.play(
            GrowFromCenter(brace_left),
            Write(label_left),
            GrowFromCenter(brace_bottom),
            Write(label_bottom)
        )
        self.wait(2)
        
        # Emphasize the equation parts
        self.play(Indicate(part_a2[0]))
        self.play(Indicate(part_ab1[0]), Indicate(part_ab2[0]))
        self.play(Indicate(part_b2[0]))
        
        self.wait(2)
