from manim import *
import numpy as np

class NormalizationIntuition(Scene):
    def construct(self):
        # Title
        title = Text("Why Normalize?", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 1. SETUP: UNNORMALIZED DATA
        # Define Unnormalized Axes
        # Feature 1 (X) is large scale: 0 to 1000
        # Feature 2 (Y) is small scale: 0 to 10
        axes = Axes(
            x_range=[0, 1000, 100],
            y_range=[0, 10, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True}
        ).shift(LEFT * 2)
        
        # Labels
        x_label = axes.get_x_axis_label("Salary (0-100k)").scale(0.6)
        y_label = axes.get_y_axis_label("Age (0-100)").scale(0.6)
        
        # Create unnormalized data points (stretched ellipse)
        np.random.seed(42)
        n_points = 100
        rhos = np.random.uniform(0, 1, n_points)
        thetas = np.random.uniform(0, 2*PI, n_points)
        
        # Ellipse parameters: center at (500, 5), radius x=400, radius y=1
        x_raw = 500 + 400 * np.sqrt(rhos) * np.cos(thetas)
        y_raw = 5 + 1 * np.sqrt(rhos) * np.sin(thetas)
        
        dots = VGroup()
        for x, y in zip(x_raw, y_raw):
            dot = Dot(axes.c2p(x, y), color=BLUE, radius=0.06)
            dots.add(dot)

        # Contour lines (Ellipses) to visualize cost function shape
        contours = VGroup()
        for i in range(1, 4):
            ellipse = Ellipse(width=axes.x_length * (i/3) * 0.8, height=axes.y_length * (i/3) * 0.2, color=RED, stroke_opacity=0.5)
            ellipse.move_to(axes.c2p(500, 5))
            contours.add(ellipse)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(FadeIn(dots), Create(contours))
        
        # Explanation text
        explanation = Text("Unnormalized: Skewed Cost Function", font_size=24, color=RED).next_to(axes, DOWN)
        self.play(Write(explanation))
        self.wait(2)
        
        # 2. TRANSFORMATION
        # Moving to normalized space
        
        # Target Axes: Standard Normal (centered at 0, unit variance)
        target_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": True}
        ).shift(RIGHT * 3)
        
        target_x_label = target_axes.get_x_axis_label("Norm. Salary").scale(0.6)
        target_y_label = target_axes.get_y_axis_label("Norm. Age").scale(0.6)
        
        # Normalized data points
        x_norm = (x_raw - 500) / 400 * 2 # mapping roughly to -2, 2 range visually
        y_norm = (y_raw - 5) / 1 * 2
        
        target_dots = VGroup()
        for x, y in zip(x_norm, y_norm):
            dot = Dot(target_axes.c2p(x/2, y/2), color=GREEN, radius=0.06) # /2 just to verify scale matches visual range
            target_dots.add(dot)
            
        # Target Contours (Circles)
        target_contours = VGroup()
        for i in range(1, 4):
            circle = Circle(radius=target_axes.x_length/2 * (i/3) * 0.7, color=GREEN, stroke_opacity=0.5)
            circle.move_to(target_axes.c2p(0, 0))
            target_contours.add(circle)
            
        # Formula
        formula = MathTex(r"x' = \frac{x - \mu}{\sigma}", color=YELLOW).move_to(UP * 2)
        
        self.play(
            Transform(explanation, Text("Normalized: Symmetric Cost Function", font_size=24, color=GREEN).next_to(target_axes, DOWN)),
            Write(formula)
        )
        
        self.play(
            Create(target_axes),
            Write(target_x_label),
            Write(target_y_label),
            Transform(dots, target_dots),
            Transform(contours, target_contours),
            run_time=3
        )
        
        self.wait(2)
        
        # Gradient Descent Arrow
        # On unnormalized (conceptual): zigzag
        # On normalized: straight to center
        
        arrow = Arrow(target_axes.c2p(2, 2), target_axes.c2p(0, 0), color=YELLOW, buff=0)
        grad_text = Text("Gradients point directly to minimum", font_size=20, color=YELLOW).next_to(arrow, RIGHT)
        
        self.play(GrowArrow(arrow), Write(grad_text))
        self.wait(2)
