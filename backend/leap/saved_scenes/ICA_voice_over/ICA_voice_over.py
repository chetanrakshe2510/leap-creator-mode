# LEAP_VERTICAL
from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
# from manim_voiceover.services.recorder import RecorderService # Alternative

class CocktailPartyICA(VoiceoverScene, MovingCameraScene):
    def construct(self):
        # 1. Setup Voiceover Service
        # Use GTTSService for automatic placeholder audio
        speech_service = GTTSService(lang="en", tld="com")
        self.set_speech_service(speech_service)
        
        # 2. Time Tracker for "Living Plots"
        self.time_tracker = ValueTracker(0)
        
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
        def get_s1_plot():
            t = self.time_tracker.get_value()
            return axes_s1.plot(lambda x: 0.5 * np.sin(3 * (x - t)), color=BLUE)
        plot_s1 = always_redraw(get_s1_plot)
        label_s1 = Text("Person A (Singer)", font_size=24, color=BLUE).next_to(axes_s1, UP, buff=0.1)
        group_s1 = VGroup(label_s1, axes_s1, plot_s1)
        
        # Source 2: Sawtooth (Reader)
        axes_s2 = Axes(**axes_config)
        def get_s2_plot():
            t = self.time_tracker.get_value()
            return axes_s2.plot(lambda x: 0.5 * (2 * ((x - t) % 1) - 1), color=RED)
        plot_s2 = always_redraw(get_s2_plot)
        label_s2 = Text("Person B (Reader)", font_size=24, color=RED).next_to(axes_s2, UP, buff=0.1)
        group_s2 = VGroup(label_s2, axes_s2, plot_s2)
        
        step1_group = VGroup(title, group_s1, group_s2).arrange(DOWN, buff=0.4)
        step1_group.to_edge(UP, buff=1.0)
        
        # VOICE OVER SECTION 1
        with self.voiceover(text="Imagine being at a crowded cocktail party. You are trying to listen to two people talking at the same time.") as tracker:
            self.play(Write(step1_group), run_time=min(2, tracker.duration))
            # Continue animation if audio is longer
            remaining = max(0.1, tracker.duration - 2)
            self.play(self.time_tracker.animate.increment_value(remaining), run_time=remaining, rate_func=linear)
            
        with self.voiceover(text="Person A is singing a pure tone, while Person B is reading a book with a sharp, robotic voice.") as tracker:
             self.play(self.time_tracker.animate.increment_value(tracker.duration), run_time=tracker.duration, rate_func=linear)

        # --- Step 2: The Environment (Mixing Matrix A) ---
        matrix_A_tex = MathTex(r"X = A \cdot S", font_size=40)
        matrix_num_tex = MathTex(r"\begin{bmatrix} 0.8 & 0.3 \\ 0.2 & 0.7 \end{bmatrix}", font_size=32, color=YELLOW)
        matrix_label = Text("Mixing Matrix (Room Acoustics)", font_size=20, color=YELLOW)
        
        step2_group = VGroup(matrix_A_tex, matrix_num_tex, matrix_label).arrange(DOWN, buff=0.3)
        step2_group.next_to(step1_group, DOWN, buff=0.8)
        
        # VOICE OVER SECTION 2
        with self.voiceover(text="But you don't hear them separately. Their voices get mixed by the room's acoustics. We represent this mixing with a matrix, A.") as tracker:
             self.play(
                self.camera.frame.animate.move_to(step2_group.get_center()),
                Write(step2_group),
                self.time_tracker.animate.increment_value(tracker.duration), 
                run_time=tracker.duration, 
                rate_func=linear
            )

        # --- Step 3: What We Observe (Mixed Signals X) ---
        
        # Prepare mixed plots
        eq_top = MathTex(r"X = A \cdot S", font_size=36).to_edge(UP, buff=1.0)
        
        axes_x1 = Axes(**axes_config)
        def get_x1_plot():
            t = self.time_tracker.get_value()
            s1 = lambda x: 0.5 * np.sin(3 * (x - t))
            s2 = lambda x: 0.5 * (2 * ((x - t) % 1) - 1)
            return axes_x1.plot(lambda x: 0.8 * s1(x) + 0.3 * s2(x), color=PURPLE)
        plot_x1 = always_redraw(get_x1_plot)
        label_x1 = Text("Mic 1 (Mixed)", font_size=24, color=PURPLE).next_to(axes_x1, UP, buff=0.1)
        group_x1 = VGroup(label_x1, axes_x1, plot_x1)
        
        axes_x2 = Axes(**axes_config)
        def get_x2_plot():
            t = self.time_tracker.get_value()
            s1 = lambda x: 0.5 * np.sin(3 * (x - t))
            s2 = lambda x: 0.5 * (2 * ((x - t) % 1) - 1)
            return axes_x2.plot(lambda x: 0.2 * s1(x) + 0.7 * s2(x), color=ORANGE)
        plot_x2 = always_redraw(get_x2_plot)
        label_x2 = Text("Mic 2 (Mixed)", font_size=24, color=ORANGE).next_to(axes_x2, UP, buff=0.1)
        group_x2 = VGroup(label_x2, axes_x2, plot_x2)
        
        step3_group = VGroup(eq_top, group_x1, group_x2).arrange(DOWN, buff=0.4)
        step3_group.to_edge(UP, buff=1.0)
        
        # VOICE OVER SECTION 3
        with self.voiceover(text="This is what your microphones actually pick up. Two chaotic, mixed signals. It looks like a mess!") as tracker:
            self.play(
                FadeOut(step1_group),
                FadeOut(step2_group),
                self.camera.frame.animate.move_to(ORIGIN),
                self.time_tracker.animate.increment_value(tracker.duration/2), # Partial time
                run_time=tracker.duration/2,
                rate_func=linear
            )
            self.play(Write(step3_group), self.time_tracker.animate.increment_value(tracker.duration/2), run_time=tracker.duration/2, rate_func=linear)

        with self.voiceover(text="Our goal is to blindly separate them back to the original sources, using only these mixed observations.") as tracker:
             self.play(self.time_tracker.animate.increment_value(tracker.duration), run_time=tracker.duration, rate_func=linear)

        # --- Step 4: Core Logic ---
        
        # Prepare Dist plots
        axes_dist = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1, 0.5],
            x_length=3.0, y_length=1.5,
            axis_config={"include_ticks": False}
        ).next_to(eq_top, DOWN, buff=1.0)
        
        curve_gauss = axes_dist.plot(lambda x: np.exp(-x**2/2), color=GRAY)
        label_gauss = Text("Mixed = Gaussian", font_size=20, color=GRAY).next_to(axes_dist, UP)
        curve_nongauss = axes_dist.plot(lambda x: np.exp(-np.abs(x)), color=GREEN)
        label_nongauss = Text("Source = Spiky", font_size=20, color=GREEN).next_to(axes_dist, UP)
        group_dist = VGroup(label_gauss, axes_dist, curve_gauss)
        rule_text = Text("Maximize Non-Gaussianity", font_size=24, color=GREEN).next_to(axes_dist, DOWN, buff=0.5)

        # VOICE OVER SECTION 4
        with self.voiceover(text="The secret is in the statistics. Mixed signals tend to look like a Gaussian Bell Curve.") as tracker:
             self.play(
                FadeOut(group_x1), FadeOut(group_x2),
                Create(group_dist),
                self.time_tracker.animate.increment_value(tracker.duration),
                run_time=tracker.duration
             )

        with self.voiceover(text="But original sources are more unique, more spiky. ICA works by rotating the data until it finds the least Gaussian, most spiky distribution.") as tracker:
             self.play(
                Transform(curve_gauss, curve_nongauss),
                Transform(label_gauss, label_nongauss),
                Write(rule_text),
                self.time_tracker.animate.increment_value(tracker.duration),
                run_time=tracker.duration
             )
        
        # --- Step 5: Reveal ---
        
        top_reveal_group = VGroup(group_x1, group_x2).arrange(DOWN, buff=0.2).to_edge(UP, buff=1.0)
        arrow_w = Arrow(start=UP, end=DOWN, color=WHITE).next_to(top_reveal_group, DOWN, buff=0.3)
        w_label = MathTex(r"W \approx A^{-1}", font_size=28).next_to(arrow_w, RIGHT)
        
        axes_r1 = Axes(**axes_config)
        def get_r1_plot(): return axes_r1.plot(lambda x: 0.5 * np.sin(3 * (x - self.time_tracker.get_value())), color=BLUE)
        plot_r1 = always_redraw(get_r1_plot)
        label_r1 = Text("Recovered A", font_size=24, color=BLUE).next_to(axes_r1, UP, buff=0.1)
        group_r1 = VGroup(label_r1, axes_r1, plot_r1)
        
        axes_r2 = Axes(**axes_config)
        def get_r2_plot(): return axes_r2.plot(lambda x: 0.5 * (2 * ((x - self.time_tracker.get_value()) % 1) - 1), color=RED)
        plot_r2 = always_redraw(get_r2_plot)
        label_r2 = Text("Recovered B", font_size=24, color=RED).next_to(axes_r2, UP, buff=0.1)
        group_r2 = VGroup(label_r2, axes_r2, plot_r2)
        
        bottom_section = VGroup(group_r1, group_r2).arrange(DOWN, buff=0.3).next_to(arrow_w, DOWN, buff=0.3)

        # VOICE OVER SECTION 5
        with self.voiceover(text="By reversing the mixing process, we recover the original sounds perfectly. And that is how we solve the Cocktail Party Problem!") as tracker:
             self.play(
                FadeOut(axes_dist), FadeOut(curve_gauss), FadeOut(label_gauss), FadeOut(rule_text),
                FadeIn(top_reveal_group),
                self.time_tracker.animate.increment_value(1), run_time=1
             )
             remaining = max(0.1, tracker.duration - 1)
             self.play(
                self.camera.frame.animate.move_to(bottom_section.get_center()),
                GrowArrow(arrow_w), Write(w_label),
                FadeIn(bottom_section, shift=UP),
                self.time_tracker.animate.increment_value(remaining),
                run_time=remaining
             )
             
        # Final active wait
        self.play(self.time_tracker.animate.increment_value(3), run_time=3, rate_func=linear)