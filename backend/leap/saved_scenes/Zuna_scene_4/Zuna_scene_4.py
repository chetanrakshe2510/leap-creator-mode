import sys
from pathlib import Path
# Add backend directory to sys.path BEFORE importing from leap
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from leap.services.kokoro_service import KokoroService

class ZunaScene4Voiceover(VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="am_michael", speed=1.0))

        # ---------------------------------------------------------
        # Subtopic 1: The Limits of Geometry (The Baseline)
        # ---------------------------------------------------------
        title = Text("The Limits of Geometry").to_edge(UP)
        self.play(Write(title))

        head_base = Ellipse(width=3, height=4, color=BLUE_A, fill_opacity=0.1)
        nose = Triangle(color=BLUE_A, fill_opacity=0.1).scale(0.2).move_to(head_base.get_top() + UP * 0.05)
        head_outline = VGroup(head_base, nose).shift(LEFT * 4)

        # Dense cluster of electrodes
        np.random.seed(42)
        dense_pts = [np.array([np.random.uniform(-1.2, 1.2), np.random.uniform(-1.5, 1.5), 0]) for _ in range(40)]
        nodes = VGroup(*[Dot(head_outline.get_center() + pt, color=BLUE, radius=0.08) for pt in dense_pts])
        
        # One electrode disappears
        target_node = nodes[20]
        target_center = target_node.get_center()

        # Find closest neighbors
        distances = [np.linalg.norm(n.get_center() - target_center) for n in nodes]
        closest_indices = np.argsort(distances)[1:5] # skip 0 since it might be itself
        neighbors = [nodes[i] for i in closest_indices]
        
        web = VGroup(*[Line(n.get_center(), target_center, color=PURPLE, stroke_width=3, stroke_opacity=0.7) for n in neighbors])
        
        # Produces a clean wave on the right
        clean_wave = FunctionGraph(lambda x: 0.8 * np.sin(3 * x), x_range=[-2, 2], color=BLUE).move_to(RIGHT * 3)

        with self.voiceover(text="Traditionally, scientists use a mathematical trick called 'spherical-spline interpolation' to guess missing brainwaves. It simply averages the signals from nearby sensors.") as tracker:
            self.play(FadeIn(head_outline), FadeIn(nodes), run_time=tracker.duration * 0.5)
            self.play(target_node.animate.set_color(RED), run_time=tracker.duration * 0.2)
            self.play(FadeOut(target_node), run_time=tracker.duration * 0.3)

        with self.voiceover(text="If you only lose one or two sensors in a dense cluster, this geometric web works great.") as tracker:
            self.play(Create(web), Create(clean_wave), run_time=tracker.duration)

        # 90% of electrodes vanish
        survivor_indices = [0, 10, 30, 35]
        to_vanish = VGroup(*[n for i, n in enumerate(nodes) if i not in survivor_indices and i != 20])
        survivors = [nodes[i] for i in survivor_indices]
        massive_web = VGroup(*[Line(s.get_center(), target_center, color=PURPLE, stroke_width=2, stroke_opacity=0.5) for s in survivors])
        distorted_wave = FunctionGraph(lambda x: 0.1 * np.sin(x) + np.random.uniform(-0.1, 0.1), x_range=[-2, 2], color=RED).move_to(RIGHT * 3)

        with self.voiceover(text="But if you lose most of your sensors, the gaps are too wide, and the math completely breaks down.") as tracker:
            self.play(FadeOut(to_vanish), FadeOut(web), FadeOut(clean_wave), run_time=tracker.duration * 0.3)
            self.play(Create(massive_web), run_time=tracker.duration * 0.2)
            self.play(massive_web.animate.set_color(RED).set_stroke(width=1), run_time=tracker.duration * 0.2)
            self.play(Create(distorted_wave), run_time=tracker.duration * 0.3)

        # Clean up
        self.play(FadeOut(head_outline), LaggedStart(*[FadeOut(s) for s in survivors], lag_ratio=0.1), FadeOut(massive_web), FadeOut(distorted_wave))

        # ---------------------------------------------------------
        # Subtopic 2: The ZUNA Advantage (The Results)
        # ---------------------------------------------------------
        title2 = Text("The ZUNA Advantage").to_edge(UP)
        
        # Animated line graph (Dropout vs Error)
        axes = Axes(
            x_range=[20, 100, 10],
            y_range=[0, 1.2, 0.2],
            axis_config={"include_numbers": True},
            x_length=7,
            y_length=5
        ).scale(0.8).move_to(DOWN * 0.5)
        
        x_label = Text("Channel Dropout %", font_size=20).next_to(axes.x_axis, DOWN, buff=0.5)
        y_label = Text("Error (NMSE)", font_size=20).next_to(axes.y_axis, LEFT, buff=0.5).rotate(PI/2)
        
        spline_curve = axes.plot(lambda x: ((x - 20) / 80) ** 3 + 0.1, color=PURPLE, x_range=[25, 95])
        zuna_curve = axes.plot(lambda x: 0.15 + 0.05 * ((x - 20) / 80), color=GREEN, x_range=[25, 95])

        spline_label = Text("Spherical Spline", color=PURPLE, font_size=20).next_to(axes.c2p(90, 0.9), LEFT)
        zuna_label = Text("ZUNA", color=GREEN, font_size=20).next_to(axes.c2p(90, 0.2), RIGHT, buff=0.1)

        with self.voiceover(text="This is where ZUNA's training pays off. Researchers tested ZUNA by intentionally deleting up to 90 percent of the EEG channels.") as tracker:
            self.play(Transform(title, title2), run_time=tracker.duration * 0.3)
            self.play(Create(axes), Write(x_label), Write(y_label), run_time=tracker.duration * 0.7)

        with self.voiceover(text="As the data gets sparser, the traditional geometric method's error rate skyrockets.") as tracker:
            self.play(Create(spline_curve), Write(spline_label), run_time=tracker.duration)

        with self.voiceover(text="But ZUNA, relying on the deep patterns it learned from millions of hours of brainwaves, consistently outputs highly accurate reconstructions. The wider the gap, the bigger ZUNA's advantage.") as tracker:
            self.play(Create(zuna_curve), Write(zuna_label), run_time=tracker.duration)
        
        self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(spline_curve), FadeOut(zuna_curve), FadeOut(spline_label), FadeOut(zuna_label))

        # ---------------------------------------------------------
        # Subtopic 3: The Real-World Impact (Superresolution)
        # ---------------------------------------------------------
        title3 = Text("Real-World Impact: Superresolution").to_edge(UP)

        # Split screen
        # Left: Clinical Lab (256 Wires)
        left_head = Ellipse(width=3, height=4, color=WHITE, fill_opacity=0.1).shift(LEFT * 3.5)
        left_nose = Triangle(color=WHITE, fill_opacity=0.1).scale(0.2).move_to(left_head.get_top() + UP * 0.05)
        clinical_group = VGroup(left_head, left_nose)
        
        clinical_label = Text("Clinical Setup (256 Wires)", font_size=20).next_to(clinical_group, UP)
        dense_grid_pts = [np.array([np.random.uniform(-1.3, 1.3), np.random.uniform(-1.8, 1.8), 0]) for _ in range(256)]
        clinical_dots = VGroup(*[Dot(left_head.get_center() + pt, color=BLUE, radius=0.03) for pt in dense_grid_pts])

        # Right: Consumer Headband (4 Sensors)
        right_head = Ellipse(width=3, height=4, color=WHITE, fill_opacity=0.1).shift(RIGHT * 3.5)
        right_nose = Triangle(color=WHITE, fill_opacity=0.1).scale(0.2).move_to(right_head.get_top() + UP * 0.05)
        consumer_group = VGroup(right_head, right_nose)
        
        consumer_label = Text("Consumer (4 Sensors)", font_size=20).next_to(consumer_group, UP)
        sparse_pts = [UP*1.5, DOWN*1.5, LEFT*1.2, RIGHT*1.2]
        consumer_dots = VGroup(*[Dot(right_head.get_center() + pt, color=GREEN, radius=0.15) for pt in sparse_pts])

        with self.voiceover(text="What does this mean for the future? Because ZUNA doesn't just fix broken channels, it can 'imagine' channels that were never there. We call this superresolution.") as tracker:
            self.play(Transform(title, title3), run_time=tracker.duration * 0.2)
            self.play(FadeIn(clinical_group), FadeIn(clinical_label), FadeIn(clinical_dots), run_time=tracker.duration * 0.4)
            self.play(FadeIn(consumer_group), FadeIn(consumer_label), FadeIn(consumer_dots), run_time=tracker.duration * 0.4)

        # Glowing green ghost-electrodes appear to fill out the 256 channel grid digitally
        ghost_pts = [np.array([np.random.uniform(-1.3, 1.3), np.random.uniform(-1.8, 1.8), 0]) for _ in range(252)]
        ghost_dots = VGroup(*[Dot(right_head.get_center() + pt, color=GREEN, radius=0.03, fill_opacity=0.4) for pt in ghost_pts])
        
        with self.voiceover(text="By upsampling the data from cheap, comfortable, everyday consumer headsets, ZUNA could give researchers access to clinical-grade brain maps anywhere in the world.") as tracker:
            self.play(
                LaggedStart(
                    *[FadeIn(dot) for dot in ghost_dots],
                    lag_ratio=0.01,
                    run_time=tracker.duration
                )
            )

        # Clean up for table
        self.play(
            FadeOut(clinical_group), FadeOut(clinical_label), FadeOut(clinical_dots),
            FadeOut(consumer_group), FadeOut(consumer_label), FadeOut(consumer_dots), FadeOut(ghost_dots)
        )

        # ---------------------------------------------------------
        # The Data Layer: Caveats of Generative AI
        # ---------------------------------------------------------
        title4 = Text("The Data Layer: Caveats of Generative AI").to_edge(UP)

        table_data = [
            ["High-Dropout Perf", "Stable NMSE error with 90% missing channels", "N/A"],
            ["Superresolution", "Applies directly to novel hardware", "Imputed channels are estimates, not absolute ground-truth"]
        ]
        table = Table(
            table_data,
            col_labels=[Text("Feature"), Text("Pros"), Text("Cons / Cautions")],
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": GRAY}
        ).scale(0.35)

        with self.voiceover(text="While generative AI like ZUNA offers incredible advantages in handling massive dropout and enabling superresolution, we must remember the data layer caveats. These imputed channels are highly realistic estimates, not absolute ground-truth measurements for critical clinical diagnoses.") as tracker:
            self.play(Transform(title, title4), run_time=tracker.duration * 0.2)
            self.play(FadeIn(table, shift=UP), run_time=tracker.duration * 0.8)
