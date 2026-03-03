from manim import *
from manim_voiceover import VoiceoverScene
from leap.services.kokoro_service import KokoroService
import numpy as np

# Apply 9:16 vertical resolution constraints for YouTube Shorts
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8.0
config.frame_height = 14.22

class TheImmortalArrows(VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="am_michael", speed=1.15))
        
        BG = "#0b0c10"
        self.camera.background_color = BG

        # ==========================================
        # 0:00 - 0:05 | The Hook
        # ==========================================
        with self.voiceover(
            text="You’ve been taught that a matrix is just a boring grid of numbers to memorize. You were lied to."
        ) as tracker:
            mat_text = MathTex(
                r"\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}",
                font_size=150, color=WHITE
            )
            self.play(Write(mat_text), run_time=1.0)
            self.wait(1.5)
            
            # Shatter / dissolve into the void
            self.play(
                mat_text.animate.scale(1.5).set_opacity(0),
                run_time=0.8, rate_func=rush_into
            )
            r = tracker.duration - 3.3
            if r > 0: self.wait(r)

        # ==========================================
        # 0:05 - 0:15 | The Chaos
        # ==========================================
        grid = NumberPlane(
            x_range=[-10, 10, 1], y_range=[-15, 15, 1],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 2, "stroke_opacity": 0.4},
            axis_config={"stroke_color": GREY_B, "stroke_width": 2}
        )
        
        # Dandelion of random arrows
        arrows = VGroup()
        np.random.seed(42)
        for i in range(40):
            angle = i * TAU / 40
            length = np.random.uniform(1.5, 3.5)
            a = Arrow(ORIGIN, [np.cos(angle)*length, np.sin(angle)*length, 0], buff=0, color=GREY_A, stroke_width=4)
            arrows.add(a)

        with self.voiceover(
            text="A matrix is actually a physical warp of space. It stretches, squishes, and shears the "
                 "fabric of the universe. When this happens, almost every arrow gets knocked completely off its path."
        ) as tracker:
            self.play(FadeIn(grid), Create(arrows), run_time=1.5)
            
            warp_matrix = [[2, 1], [1, 2]]
            warp_3d = np.array([[2, 1, 0], [1, 2, 0], [0, 0, 1]])
            
            self.play(
                grid.animate.apply_matrix(warp_matrix),
                *[a.animate.put_start_and_end_on(ORIGIN, np.dot(warp_3d, a.get_end())) for a in arrows],
                run_time=3.5, rate_func=smooth
            )
            
            r = tracker.duration - 5.0
            if r > 0: self.wait(r)

        # ==========================================
        # 0:15 - 0:25 | The Revelation
        # ==========================================
        with self.voiceover(
            text="But if you look closely, there are a few rare, immortal arrows. They might stretch, "
                 "they might even flip backward, but they never change direction. These are the Eigenvectors."
        ) as tracker:
            # Target endpoints for eigenvectors of [[2,1],[1,2]]
            ev1_target = np.array([1, 1, 0]) * 2.5
            ev2_target = np.array([-1, 1, 0]) * 2.5
            
            ev1 = Arrow(ORIGIN, ev1_target, buff=0, color="#ffd43b", stroke_width=8)
            ev2 = Arrow(ORIGIN, ev2_target, buff=0, color="#ffd43b", stroke_width=8)
            
            # Undo the warp instantly in the background so we can show it again cleanly
            grid.apply_matrix(np.linalg.inv(warp_matrix))
            for a in arrows:
                a.put_start_and_end_on(ORIGIN, np.dot(np.linalg.inv(warp_3d), a.get_end()))
            
            self.play(
                arrows.animate.set_color("#495057").set_opacity(0.3),
                grid.animate.set_style(stroke_opacity=0.1),
                FadeIn(ev1), FadeIn(ev2),
                run_time=1.5
            )

            # Replay warp, showing ev1 and ev2 staying strictly on their lines
            # Eigenvector 1 (1,1) scales by 3.
            # Eigenvector 2 (-1,1) scales by 1 (doesn't move!).
            self.play(
                grid.animate.apply_matrix(warp_matrix).set_style(stroke_opacity=0.4),
                *[a.animate.put_start_and_end_on(ORIGIN, np.dot(warp_3d, a.get_end())) for a in arrows],
                ev1.animate.put_start_and_end_on(ORIGIN, np.dot(warp_3d, ev1_target)),
                ev2.animate.put_start_and_end_on(ORIGIN, np.dot(warp_3d, ev2_target)),
                run_time=3.5, rate_func=smooth
            )
            r = tracker.duration - 5.0
            if r > 0: self.wait(r)

        self.play(
            FadeOut(grid), FadeOut(arrows), 
            FadeOut(ev1), FadeOut(ev2), 
            run_time=0.8
        )

        # ==========================================
        # 0:25 - 0:40 | The Mind-Blower
        # ==========================================
        with self.voiceover(
            text="Why do we care? Because these stubborn arrows reveal the hidden skeleton of reality. "
                 "They are the exact mathematical secret to how machine learning compresses massive data,"
        ) as tracker:
            # Fast Cut 1: PCA Compression
            cloud = VGroup(*[
                Dot([np.random.normal(0, 1.5), np.random.normal(0, 0.5), 0], color="#63e6be") 
                for _ in range(70)
            ])
            cloud.rotate(PI/6)
            self.play(FadeIn(cloud), run_time=0.5)
            
            pca_line = Line(DOWN*3 + LEFT*1.73, UP*3 + RIGHT*1.73, color="#ffd43b", stroke_width=6)
            self.play(Create(pca_line), run_time=0.5)
            
            self.play(
                *[d.animate.move_to(pca_line.get_projection(d.get_center())) for d in cloud], 
                run_time=1.5, rate_func=rush_into
            )
            self.play(FadeOut(cloud), FadeOut(pca_line), run_time=0.3)
            
            r = tracker.duration - 2.8
            if r > 0: self.wait(r)
            
        with self.voiceover(
            text="how bridges vibrate, and how we isolate the fundamental rhythms of the human mind."
        ) as tracker:
            # Fast Cut 2: Bridge Sway
            bridge_deck = Line(LEFT*3.5, RIGHT*3.5, color="#74c0fc", stroke_width=8)
            pillars = VGroup(
                Line(LEFT*2+DOWN*2, LEFT*2+UP*1.5, color="#74c0fc", stroke_width=6),
                Line(RIGHT*2+DOWN*2, RIGHT*2+UP*1.5, color="#74c0fc", stroke_width=6)
            )
            cables = VGroup(
                Line(LEFT*2+UP*1.5, LEFT*3.5, color="#4dabf7"),
                Line(LEFT*2+UP*1.5, ORIGIN, color="#4dabf7"),
                Line(RIGHT*2+UP*1.5, ORIGIN, color="#4dabf7"),
                Line(RIGHT*2+UP*1.5, RIGHT*3.5, color="#4dabf7")
            )
            bridge = VGroup(bridge_deck, pillars, cables).shift(DOWN*0.5)
            
            self.play(FadeIn(bridge), run_time=0.3)
            # Wobble bridge with a shear
            self.play(
                bridge.animate.apply_matrix([[1, 0.3], [0, 1]]).set_color("#ffd43b"), 
                run_time=0.6, rate_func=there_and_back
            )
            self.play(
                bridge.animate.apply_matrix([[1, -0.3], [0, 1]]).set_color("#ffd43b"), 
                run_time=0.6, rate_func=there_and_back
            )
            self.play(FadeOut(bridge), run_time=0.3)
            
            # Fast Cut 3: Brain Pulse
            nodes = VGroup(*[
                Dot([np.random.uniform(-3, 3), np.random.uniform(-4, 4), 0], color=WHITE, radius=0.1) 
                for _ in range(25)
            ])
            edges = VGroup(*[
                Line(n1.get_center(), n2.get_center(), stroke_opacity=0.3, color="#4dabf7") 
                for n1 in nodes for n2 in nodes if np.random.random() > 0.85
            ])
            brain = VGroup(nodes, edges).shift(UP*0.5)
            self.play(FadeIn(brain), run_time=0.4)
            self.play(
                brain.animate.scale(1.2).set_color("#ffd43b"), 
                run_time=0.6, rate_func=there_and_back
            )
            self.play(FadeOut(brain), run_time=0.4)

            r = tracker.duration - 3.2
            if r > 0: self.wait(r)

        # ==========================================
        # 0:40 - 0:50 | The Call to Action
        # ==========================================
        with self.voiceover(
            text="Want to stop blindly calculating and actually see the math? "
                 "Tap the related video below to unlock the visual secrets of Linear Algebra."
        ) as tracker:
            
            # Split strings to target \vec{v} easily
            eq = MathTex("A", r"\vec{v}", "=", r"\lambda", r"\vec{v}", font_size=100)
            eq[1].set_color("#ffd43b") # \vec{v}
            eq[4].set_color("#ffd43b") # \vec{v}
            
            self.play(Write(eq), run_time=1.5)
            
            cta_txt1 = Text("Stop memorizing.", font="Outfit", font_size=60, weight=BOLD).next_to(eq, UP, buff=2)
            cta_txt2 = Text("Start seeing.", font="Outfit", font_size=60, weight=BOLD, color="#ffd43b").next_to(cta_txt1, DOWN, buff=0.5)
            
            cta_arrow = Arrow(DOWN*4, DOWN*6.5, color=WHITE, stroke_width=10, max_tip_length_to_length_ratio=0.15)
            cta_txt3 = Text("Watch the full video", font="Outfit", font_size=40).next_to(cta_arrow, UP, buff=0.5)
            
            self.play(FadeIn(cta_txt1, shift=UP*0.5), run_time=0.8)
            self.play(FadeIn(cta_txt2, shift=UP*0.5), run_time=0.8)
            self.wait(0.5)
            self.play(FadeIn(cta_txt3, shift=UP*0.5), GrowArrow(cta_arrow), run_time=1.0)
            
            r = tracker.duration - 4.6
            if r > 0: self.wait(r)
        
        self.wait(1.0)