from manim import *
import numpy as np

class DistributionShapeProperty(Scene):
    def construct(self):
        # Title
        title = Text("Does Normalization Change Shape?", font_size=36).to_edge(UP)
        answer = Text("No! It only Shifts and Scales.", font_size=36, color=YELLOW).next_to(title, DOWN)
        
        self.play(Write(title))
        self.wait(1)
        self.play(Write(answer))
        self.wait(1)
        
        # --- 1. Original Distribution (e.g., Heights in cm) ---
        # Mean = 170, Std = 10
        # We need axes that can show this loc
        
        axes_orig = Axes(
            x_range=[130, 210, 10],
            y_range=[0, 0.05, 0.01],
            x_length=6,
            y_length=3,
            axis_config={"include_numbers": True, "font_size": 20}
        ).shift(UP * 0.5)
        
        x_label = axes_orig.get_x_axis_label("Height (cm)")
        
        # Gaussian Function
        def gaussian(x, mu, sigma):
            return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu)/sigma)**2)
        
        mu_orig = 170
        sigma_orig = 10
        
        curve_orig = axes_orig.plot(lambda x: gaussian(x, mu_orig, sigma_orig), color=BLUE)
        curve_label = Text("Original Bell Curve", font_size=24, color=BLUE).next_to(curve_orig, UP)
        
        self.play(Create(axes_orig), Write(x_label))
        self.play(Create(curve_orig), Write(curve_label))
        self.wait(1)
        
        # --- 2. Shift (Mean Centering) ---
        # Move entire graph to be centered at 0
        # Instead of moving curve on same axes, let's transform the AXES and CURVE together
        # to a new coordinate system below
        
        axes_centered = Axes(
            x_range=[-40, 40, 10], # 130-170=-40, 210-170=40
            y_range=[0, 0.05, 0.01],
            x_length=6,
            y_length=3,
            axis_config={"include_numbers": True, "font_size": 20}
        ).shift(DOWN * 2) # Position below
        
        # We will actally keep it in same position for visual continuity first?
        # User said "Just shifts and scales the axes".
        # Let's animate the AXES changing numbers while curve stays visually same?
        # No, "Shifting" usually implies value change. 
        # Let's show the curve physically moving to "0" on a shared number line concept?
        # Or better: Transform the axes linearly.
        
        step1 = Text("Step 1: Shift (x - 170)", font_size=24, color=YELLOW).to_edge(RIGHT).shift(UP)
        self.play(Write(step1))
        
        # Animate axis values sliding? Hard.
        # Let's simple create the new centered graph below.
        
        mu_centered = 0
        sigma_centered = 10 # Variance unchanged yet
        
        curve_centered = axes_centered.plot(lambda x: gaussian(x, mu_centered, sigma_centered), color=BLUE)
        # x_label_centered = axes_centered.get_x_axis_label("Centered")
        
        arrow_shift = Arrow(axes_orig.get_bottom(), axes_centered.get_top(), color=YELLOW)
        
        self.play(Create(axes_centered))
        self.play(GrowArrow(arrow_shift))
        self.play(TransformFromCopy(curve_orig, curve_centered))
        self.wait(1)
        
        # --- 3. Scale (Standard Deviation) ---
        # Now squish width, stretch height (to maintain probability mass = 1)
        
        step2 = Text("Step 2: Scale (/ 10)", font_size=24, color=GREEN).next_to(step1, DOWN)
        self.play(Write(step2))
        
        # Final Axes: Standard Normal
        axes_final = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1], # Height increases as width decreases
            x_length=6,
            y_length=3,
            axis_config={"include_numbers": True, "font_size": 20}
        ).move_to(axes_centered.get_center())
        
        mu_final = 0
        sigma_final = 1
        
        curve_final = axes_final.plot(lambda x: gaussian(x, mu_final, sigma_final), color=GREEN)
        
        self.play(
            ReplacementTransform(axes_centered, axes_final),
            ReplacementTransform(curve_centered, curve_final),
            FadeOut(arrow_shift),
            run_time=2
        )
        
        final_label = Text("Standard Normal (Z-Score)", font_size=24, color=GREEN).next_to(curve_final, UP)
        self.play(Transform(curve_label, final_label))
        self.wait(1)
        
        # --- 4. Shape Comparison ---
        # Show that if we stretched the Green curve back, it fits the Blue curve.
        # Or better: "Geometry is identical, just zoomed."
        
        geometry_text = Text("The Geometry is Identical!", color=WHITE, font_size=30).to_edge(DOWN)
        self.play(Write(geometry_text))
        
        # Overlay a copy of the original curve (scaled down to match visual frame of final)
        # Actually visually they look different now because the axes scales changed differently.
        # Normalization changes aspect ratio if X and Y scales aren't locked.
        # But the "Definition" of the shape (Gaussian) is preserved. It's an Affine transformation.
        
        # Let's show: "It's still a bell curve."
        # Verify Skewness and Kurtosis are preserved (visually).
        
        check1 = Text("Skewness: 0 -> 0", font_size=20).next_to(axes_final, RIGHT)
        check2 = Text("Kurtosis: 3 -> 3", font_size=20).next_to(check1, DOWN)
        
        self.play(FadeIn(check1), FadeIn(check2))
        self.wait(3)
