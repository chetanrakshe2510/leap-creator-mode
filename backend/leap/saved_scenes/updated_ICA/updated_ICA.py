# LEAP_VERTICAL
from manim import *
import numpy as np

class CocktailPartyICA(MovingCameraScene):
    def construct(self):
        # Golden Rules applied: Relative positioning, VGroup arrangement, Camera Scroll
        
        # --- Common Config ---
        axes_config = {
            "x_range": [0, 8, 1],
            "y_range": [-1.5, 1.5, 1],
            "x_length": 4.0,
            "y_length": 1.5,
            "axis_config": {"include_ticks": False, "tip_shape": StealthTip}
        }
        
        # --- Step 1: The Hidden Reality (Sources S) ---
        title = Text("Original Sources (Hidden)", font_size=32, weight=BOLD)
        
        # Source 1: Sine (Singer)
        axes_s1 = Axes(**axes_config)
        s1_func = lambda t: 0.5 * np.sin(3 * t)
        plot_s1 = axes_s1.plot(s1_func, color=BLUE)
        label_s1 = Text("Person A (Singer)", font_size=20, color=BLUE).next_to(axes_s1, LEFT, buff=0.1)
        group_s1 = VGroup(label_s1, axes_s1, plot_s1)
        
        # Source 2: Sawtooth (Reader)
        axes_s2 = Axes(**axes_config)
        s2_func = lambda t: 0.5 * (2 * (t % 1) - 1)
        plot_s2 = axes_s2.plot(s2_func, color=RED)
        label_s2 = Text("Person B (Reader)", font_size=20, color=RED).next_to(axes_s2, LEFT, buff=0.1)
        group_s2 = VGroup(label_s2, axes_s2, plot_s2)
        
        step1_group = VGroup(title, group_s1, group_s2).arrange(DOWN, buff=0.4)
        step1_group.to_edge(UP, buff=1.0)
        
        self.play(Write(step1_group))
        self.wait(2)
        
        # --- Step 2: The Environment (Mixing Matrix A) ---
        # Formula X = A * S
        matrix_A_tex = MathTex(
            r"X = A \cdot S",
            font_size=40
        )
        
        matrix_num_tex = MathTex(
            r"\begin{bmatrix} 0.8 & 0.3 \\ 0.2 & 0.7 \end{bmatrix}",
            font_size=32, color=YELLOW
        )
        
        matrix_label = Text("Mixing Matrix (Room Acoustics)", font_size=20, color=YELLOW)
        
        step2_group = VGroup(matrix_A_tex, matrix_num_tex, matrix_label).arrange(DOWN, buff=0.3)
        step2_group.next_to(step1_group, DOWN, buff=0.8)
        
        # Scroll to show Step 2
        self.play(
            self.camera.frame.animate.move_to(step2_group.get_center()),
            Write(step2_group)
        )
        self.wait(2)
        
        # --- Step 3: What We Observe (Mixed Signals X) ---
        # "Crucial 9:16 Move: Clear screen"
        
        self.play(
            FadeOut(step1_group),
            FadeOut(step2_group),
            run_time=1
        )
        # Reset camera for fresh start at top
        self.play(self.camera.frame.animate.move_to(ORIGIN), run_time=0.5)
        
        # New Header for Step 3
        eq_top = MathTex(r"X = A \cdot S", font_size=36).to_edge(UP, buff=1.0)
        
        # Mixed Signals
        # x1 = 0.8s1 + 0.3s2
        axes_x1 = Axes(**axes_config)
        x1_func = lambda t: 0.8 * s1_func(t) + 0.3 * s2_func(t)
        plot_x1 = axes_x1.plot(x1_func, color=PURPLE)
        label_x1 = Text("Mic 1 (Mixed)", font_size=20, color=PURPLE).next_to(axes_x1, LEFT, buff=0.1)
        group_x1 = VGroup(label_x1, axes_x1, plot_x1)
        
        # x2 = 0.2s1 + 0.7s2
        axes_x2 = Axes(**axes_config)
        x2_func = lambda t: 0.2 * s1_func(t) + 0.7 * s2_func(t)
        plot_x2 = axes_x2.plot(x2_func, color=ORANGE)
        label_x2 = Text("Mic 2 (Mixed)", font_size=20, color=ORANGE).next_to(axes_x2, LEFT, buff=0.1)
        group_x2 = VGroup(label_x2, axes_x2, plot_x2)
        
        step3_group = VGroup(eq_top, group_x1, group_x2).arrange(DOWN, buff=0.4)
        step3_group.to_edge(UP, buff=1.0)
        
        self.play(Write(step3_group))
        self.wait(2)
        
        # --- Step 4: The Core Logic (Non-Gaussianity) ---
        # Fade out mixed waves to make room
        self.play(
            FadeOut(group_x1),
            FadeOut(group_x2)
        )
        
        # Bell Curve vs Spiky
        axes_dist = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1, 0.5],
            x_length=3.0, y_length=1.5,
            axis_config={"include_ticks": False}
        ).next_to(eq_top, DOWN, buff=1.0)
        
        # Gaussian (Bell)
        curve_gauss = axes_dist.plot(lambda x: np.exp(-x**2/2), color=GRAY)
        label_gauss = Text("Mixed = Gaussian", font_size=20, color=GRAY).next_to(axes_dist, UP)
        
        # Non-Gaussian (Spiky/Super-Gaussian) - roughly
        curve_nongauss = axes_dist.plot(lambda x: np.exp(-np.abs(x)), color=GREEN)
        label_nongauss = Text("Source = Spiky", font_size=20, color=GREEN).next_to(axes_dist, UP)
        
        group_dist = VGroup(label_gauss, axes_dist, curve_gauss)
        
        self.play(Create(group_dist))
        self.wait(1)
        
        self.play(
            Transform(curve_gauss, curve_nongauss),
            Transform(label_gauss, label_nongauss)
        )
        
        rule_text = Text(
            "ICA rotates data to find\nthe least bell-shaped curve!",
            font_size=24, t2c={"ICA": GREEN}
        ).next_to(axes_dist, DOWN, buff=0.5)
        
        self.play(Write(rule_text))
        self.wait(2)
        
        # --- Step 5: The Grand Reveal ---
        self.play(
            FadeOut(group_dist),
            FadeOut(label_gauss), # In case transform left artifact
            FadeOut(rule_text),
            FadeIn(group_x1), # Bring back mixed top
            FadeIn(group_x2)
        )
        
        # Organize top section again
        top_section = VGroup(group_x1, group_x2).arrange(DOWN, buff=0.2).to_edge(UP, buff=1.5)
        group_x1.move_to(top_section[0])
        group_x2.move_to(top_section[1])
        
        # Arrow W
        arrow_w = Arrow(start=UP, end=DOWN, color=WHITE).next_to(top_section, DOWN, buff=0.3)
        w_label = MathTex(r"W \approx A^{-1}", font_size=28).next_to(arrow_w, RIGHT)
        
        # Recovered Sources (Bottom)
        # Rec 1 (Blue)
        axes_r1 = Axes(**axes_config)
        # Simulate slight scale diff or sign flip if desired, but let's keep it clean
        plot_r1 = axes_r1.plot(s1_func, color=BLUE)
        label_r1 = Text("Recovered A", font_size=20, color=BLUE).next_to(axes_r1, LEFT, buff=0.1)
        group_r1 = VGroup(label_r1, axes_r1, plot_r1)
        
        # Rec 2 (Red)
        axes_r2 = Axes(**axes_config)
        plot_r2 = axes_r2.plot(s2_func, color=RED) 
        label_r2 = Text("Recovered B", font_size=20, color=RED).next_to(axes_r2, LEFT, buff=0.1)
        group_r2 = VGroup(label_r2, axes_r2, plot_r2)
        
        bottom_section = VGroup(group_r1, group_r2).arrange(DOWN, buff=0.3)
        bottom_section.next_to(arrow_w, DOWN, buff=0.3)
        
        # Need space? Scroll down.
        self.play(
            self.camera.frame.animate.move_to(bottom_section.get_center()),
            GrowArrow(arrow_w), Write(w_label),
            FadeIn(bottom_section, shift=UP),
            run_time=2
        )
        
        self.wait(3)