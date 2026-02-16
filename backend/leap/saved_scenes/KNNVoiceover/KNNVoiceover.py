# LEAP_VERTICAL
from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class KNNVoiceover(VoiceoverScene, MovingCameraScene):
    def construct(self):
        # 1. Setup Voiceover
        speech_service = GTTSService(lang="en", tld="com")
        self.set_speech_service(speech_service)
        
        # 2. Time Tracker for "Living Plots"
        self.time_tracker = ValueTracker(0)

        # --- Layout & Setup ---
        title = Text("K-Nearest Neighbors", font_size=42, weight=BOLD).to_edge(UP, buff=1.0)
        subtitle = Text("Classification (K=3)", font_size=28, color=GRAY).next_to(title, DOWN, buff=0.2)
        
        # Plot Area (Standard 9:16 safe width)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=4.0, y_length=4.0, 
            axis_config={"include_ticks": False, "include_tip": False}
        ).to_edge(LEFT, buff=0.25).shift(DOWN * 0.5)
        
        # --- Data Generation with "Living Plots" ---
        
        def get_pulse_scale():
            t = self.time_tracker.get_value()
            return 1 + 0.1 * np.sin(3 * t) # Gentle pulse
            
        # Class A: Red Triangles
        class_a_points = [[2, 6], [3, 7], [2.5, 8], [4, 6.5], [3, 5.5]]
        
        def get_group_a():
            group = VGroup()
            scale = get_pulse_scale()
            for p in class_a_points:
                # Add random phase shift based on x-coord so they don't pulse perfectly in sync
                local_scale = 1 + 0.1 * np.sin(3 * self.time_tracker.get_value() + p[0])
                dot = Triangle(color=RED, fill_opacity=1).scale(0.15 * local_scale).move_to(axes.c2p(*p))
                group.add(dot)
            return group
        group_a = always_redraw(get_group_a)
            
        # Class B: Blue Squares
        class_b_points = [[7, 3], [8, 2], [6, 4], [7.5, 3.5], [8, 4.5], [6.5, 2.5]]
        
        def get_group_b():
            group = VGroup()
            for p in class_b_points:
                local_scale = 1 + 0.1 * np.sin(3 * self.time_tracker.get_value() + p[1])
                dot = Square(color=BLUE, fill_opacity=1).scale(0.15 * local_scale).move_to(axes.c2p(*p))
                group.add(dot)
            return group
        group_b = always_redraw(get_group_b)
            
        # Query Point
        query_coords = [4.5, 5]
        def get_query_point():
            scale = 1 + 0.05 * np.sin(5 * self.time_tracker.get_value())
            return Dot(axes.c2p(*query_coords), color=GRAY, radius=0.15 * scale)
        query_point = always_redraw(get_query_point)
        
        query_label = always_redraw(lambda: Text("?", font_size=32).next_to(query_point, UP, buff=0.1 + 0.05 * np.sin(2 * self.time_tracker.get_value())))

        # --- Animation Sequence ---
        
        # 1. Intro
        with self.voiceover(text="This is K-Nearest Neighbors, a simple way to classify data.") as tracker:
            self.play(Write(title), FadeIn(subtitle), run_time=tracker.duration)
        
        # 2. Show Data
        with self.voiceover(text="We have two classes: Red Triangles and Blue Squares.") as tracker:
            self.play(FadeIn(group_a), FadeIn(group_b), run_time=tracker.duration)
            self.play(self.time_tracker.animate.increment_value(1), run_time=1, rate_func=linear)

        # 3. Enter Query Point
        with self.voiceover(text="A new, unknown point appears. How should we classify it?") as tracker:
            self.play(GrowFromCenter(query_point), Write(query_label), run_time=tracker.duration)

        # 4. Calculate Distance
        # Neighbors: [4, 6.5](A), [3, 5.5](A), [6, 4](B)
        # We need static references for the lines, so we get the current state of the points
        p_q = axes.c2p(*query_coords)
        p_n1 = axes.c2p(4, 6.5)
        p_n2 = axes.c2p(3, 5.5)
        p_n3 = axes.c2p(6, 4)
        
        lines = VGroup(
            DashedLine(p_q, p_n1, color=YELLOW),
            DashedLine(p_q, p_n2, color=YELLOW),
            DashedLine(p_q, p_n3, color=YELLOW)
        )
        
        radius = np.linalg.norm(axes.c2p(4.5, 5) - axes.c2p(6, 4))
        search_circle = Circle(radius=radius, color=YELLOW).move_to(p_q)

        with self.voiceover(text="We look at the 3 nearest neighbors within a certain distance.") as tracker:
            self.play(Create(search_circle), Create(lines), run_time=tracker.duration)
            self.play(self.time_tracker.animate.increment_value(1), run_time=1, rate_func=linear)
            
        # 5. Highlight Neighbors
        # Living plots make this tricky because they redraw. We'll add static highlighters on top.
        h1 = Circle(color=YELLOW, radius=0.3).move_to(p_n1)
        h2 = Circle(color=YELLOW, radius=0.3).move_to(p_n2)
        h3 = Circle(color=YELLOW, radius=0.3).move_to(p_n3)
        highlights = VGroup(h1, h2, h3)

        with self.voiceover(text="In this case, we have two Red Triangles and one Blue Square.") as tracker:
             self.play(Create(highlights), run_time=tracker.duration)

        # 6. Voting Tally
        tally_box = Rectangle(width=4, height=1.5, color=WHITE).to_edge(DOWN, buff=1.0)
        tally_title = Text("Votes (K=3)", font_size=24).next_to(tally_box, UP, buff=0.1)
        
        vote_a = Triangle(color=RED, fill_opacity=1).scale(0.15)
        vote_b = Square(color=BLUE, fill_opacity=1).scale(0.15)
        votes = VGroup(
            vote_a.copy(), vote_a.copy(), Text("vs", font_size=20), vote_b.copy()
        ).arrange(RIGHT, buff=0.3).move_to(tally_box)

        with self.voiceover(text="Since Red has the most votes, red wins!") as tracker:
            self.play(Create(tally_box), Write(tally_title), FadeIn(votes), run_time=tracker.duration)

        # 7. Classification
        final_shape = Triangle(color=RED, fill_opacity=1).scale(0.15).move_to(axes.c2p(*query_coords))
        
        with self.voiceover(text="We classify the new point as a Red Triangle.") as tracker:
            self.play(
                Transform(query_point, final_shape), 
                FadeOut(query_label, shift=UP),
                run_time=tracker.duration
            )
            
        self.play(self.time_tracker.animate.increment_value(3), run_time=3, rate_func=linear)