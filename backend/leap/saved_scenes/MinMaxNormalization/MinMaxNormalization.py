from manim import *
import numpy as np

class MinMaxNormalization(Scene):
    def construct(self):
        # Title
        title = Text("Min-Max Normalization", font_size=40).to_edge(UP)
        subtitle = Text("The 'Squish' Method", font_size=30, color=YELLOW).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        
        # --- PHASE 1: THE PROBLEM (Ages 20-80) ---
        
        # Number Line 0 to 100
        # We position it slightly left to leave room for text/equations
        number_line = NumberLine(
            x_range=[0, 100, 10], 
            length=10, 
            include_numbers=True,
            numbers_to_include=[0, 20, 50, 80, 100]
        ).shift(DOWN * 0.5)
        
        ax_label = number_line.get_label_constructor()("Age").next_to(number_line, RIGHT)
        
        # Data Points: 20(Min), 80(Max), 50(Middle), and some randoms
        ages = [20, 80, 50, 30, 65, 72, 25]
        dots = VGroup()
        for age in ages:
            color = RED if age in [20, 80] else BLUE
            # Use z_index to make dots appear on top of line
            dot = Dot(number_line.n2p(age), color=color, z_index=10)
            dots.add(dot)
            
        # Labels for Min and Max
        min_label = MathTex("Min = 20").next_to(dots[0], UP).add_background_rectangle()
        max_label = MathTex("Max = 80").next_to(dots[1], UP).add_background_rectangle()
        
        self.play(Create(number_line), Write(ax_label))
        self.play(FadeIn(dots, scale=0.5))
        self.play(Write(min_label), Write(max_label))
        self.wait(1)
        
        # --- PHASE 2: SHIFT (Subtract Min) ---
        
        step1_text = Text("Step 1: Shift (-20)", color=YELLOW, font_size=36).to_edge(UP).shift(DOWN)
        equation1 = MathTex("x' = x - 20").next_to(step1_text, DOWN)
        
        self.play(
            ReplacementTransform(subtitle, step1_text),
            FadeIn(equation1)
        )
        
        # Animate dots moving to the left
        # We physically move them to where they would be on the SAME number line
        # 20 -> 0, 80 -> 60
        
        shift_anim_group = []
        shifted_dots = VGroup()
        for dot, age in zip(dots, ages):
            new_age = age - 20
            new_pos = number_line.n2p(new_age)
            shift_anim_group.append(dot.animate.move_to(new_pos))
            # Create new dot object for the final state comparison if needed, 
            # but we can just use the moved dots.
        
        # Show arrow for the shift on the axis
        shift_arrow = Arrow(number_line.n2p(20), number_line.n2p(0), color=YELLOW, buff=0).shift(UP*0.4)
        
        self.play(GrowArrow(shift_arrow))
        self.play(*shift_anim_group, run_time=2)
        
        # Update Min/Max labels to 0 and 60
        new_min_label = MathTex("0").next_to(number_line.n2p(0), UP).add_background_rectangle()
        new_max_label = MathTex("60").next_to(number_line.n2p(60), UP).add_background_rectangle()
        
        self.play(
            FadeOut(min_label), FadeOut(max_label), FadeOut(shift_arrow),
            FadeIn(new_min_label), FadeIn(new_max_label)
        )
        self.wait(1)
        
        # --- PHASE 3: SQUISH (Divide by Range) ---
        
        step2_text = Text("Step 2: Squish (/ 60)", color=GREEN, font_size=36).to_edge(UP).shift(DOWN)
        equation2 = MathTex("x'' = x' / 60").next_to(step2_text, DOWN)
        
        self.play(
            ReplacementTransform(step1_text, step2_text),
            ReplacementTransform(equation1, equation2)
        )
        
        # Transforming the NumberLine itself to [0, 1]
        # We'll replace the old number line with a new unit interval line
        # visually stretching it out to fill the same space? 
        # OR "squishing" the dots into a small space?
        # The prompt says "Fitting perfectly into a 1x1 box", implying the container stays fixed
        # and data fits into it. 
        # Usually normalization makes data FIT standard bounds.
        # Let's show the dots moving into the [0, 1] range on the ORIGINAL line first (getting really packed),
        # AND THEN zoom in / rescale the axis.
        # actually, simply transforming the axis is clearer for "what the values become".
        
        unit_line = NumberLine(
            x_range=[0, 1, 0.1],
            length=10,
            include_numbers=True,
            numbers_to_include=[0, 0.5, 1],
            decimal_number_config={"num_decimal_places": 1}
        ).shift(DOWN * 0.5)
        
        # We need to map the CURRENT dot positions (which are at 0..60 on the old line)
        # to 0..1 on the NEW line.
        # Since the lines have same physical length and position, 
        # 0 on old line = 0 on new line.
        # 60 on old line (at x=~2) needs to go to 1 on new line (at x=~5).
        # Wait, NumberLine(length=10).
        # Old: 0..100. 0 is at left. 100 is at right.
        # Current dots: 0 to 60. They occupy leftmost 60% of the line.
        # New line: 0..1. 0 is at left. 1 is at right.
        # So 60 (currently at 60% mark) needs to move to 1 (100% mark).
        # So dots effectively spread out filling the line?
        # Or did we mean "Squish" in terms of values?
        # Value-wise: 60 becomes 1.
        # Visually: If we keep the axis static (fixed physical scale), the dots would shrink to a tiny point.
        # If we change the axis units (normalization), they fill the standardized range.
        # The user said "Squish: Now the oldest person is at 60... divide by 60... result is 1".
        # Let's show the axis transforming to match the new scale.
        
        # Correct visualization:
        # The "Range" 60 visually "squishes" to become "1".
        
        self.play(
            Transform(number_line, unit_line),
            # Dots are VGroup of Point objects. We need to move them to their new home on the unit_line
            # We can't just Transform(dots) because we need to calculate positions.
            # But we can animate them moving.
            *[
                dot.animate.move_to(unit_line.n2p((age-20)/60)) 
                for dot, age in zip(dots, ages)
            ],
            Transform(new_min_label, MathTex("0").next_to(unit_line.n2p(0), UP).add_background_rectangle()),
            Transform(new_max_label, MathTex("1").next_to(unit_line.n2p(1), UP).add_background_rectangle()),
            run_time=3
        )
        self.wait(1)
        
        # Highlight the 50 year old (now at 0.5)
        # 50 - 20 = 30. 30 / 60 = 0.5.
        # It's the 3rd dot in our list (index 2)
        mid_label = MathTex("Age 50 \\rightarrow 0.5").next_to(dots[2], UP).add_background_rectangle()
        self.play(Write(mid_label))
        self.wait(2)
        
        # --- PHASE 4: 1x1 BOX (The Goal) ---
        
        final_text = Text("Result: Fits in Unit Space", color=BLUE, font_size=36).to_edge(UP).shift(DOWN)
        self.play(
            ReplacementTransform(step2_text, final_text),
            ReplacementTransform(equation2, final_text), # Just merge them
            FadeOut(mid_label),
            FadeOut(new_min_label),
            FadeOut(new_max_label),
            FadeOut(ax_label)
        )

        
        # Transform 1D line to X-axis of a 2D plot
        # Create Y-axis
        axes_2d = Axes(
            x_range=[0, 1.2, 0.5], y_range=[0, 1.2, 0.5],
            x_length=5, y_length=5,
            axis_config={"include_numbers": True}
        ).move_to(ORIGIN)
        
        # Box [0,0] to [1,1]
        box = Square(side_length=axes_2d.x_length / 1.2, color=GREEN, fill_opacity=0.1).move_to(axes_2d.c2p(0.5, 0.5))
        # Wait, side_length scaling is tricky. P2C distance.
        # Let's just use Polygon
        box = Rectangle(
            width=axes_2d.c2p(1,0)[0] - axes_2d.c2p(0,0)[0],
            height=axes_2d.c2p(0,1)[1] - axes_2d.c2p(0,0)[1],
            color=GREEN,
            fill_opacity=0.1
        ).move_to(axes_2d.c2p(0.5, 0.5))


        self.play(
            ReplacementTransform(number_line, axes_2d.get_x_axis()), # Morph line to X axis
            Create(axes_2d.get_y_axis()),
            FadeOut(dots) # Fade out 1D dots, bring in 2D scatter
        )
        
        self.play(Create(box))
        
        # Generate random normalized 2D points inside the box
        points_2d = VGroup()
        for _ in range(40):
            x, y = np.random.random(), np.random.random()
            points_2d.add(Dot(axes_2d.c2p(x, y), radius=0.06, color=BLUE))
            
        self.play(FadeIn(points_2d))
        
        label_box = Text("1x1 Box", color=GREEN, font_size=24).next_to(box, UP)
        self.play(Write(label_box))
        
        self.wait(3)
