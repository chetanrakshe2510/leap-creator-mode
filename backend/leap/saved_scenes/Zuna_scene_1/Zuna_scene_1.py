from manim import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from leap.services.kokoro_service import KokoroService

class EEGSymphonyVoiceover(VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="am_michael", speed=1.0))

        # ---------------------------------------------------------
        # Subtopic 1: The Brain's Symphony (Normal EEG)
        # ---------------------------------------------------------
        title = Text("The Brain's Symphony").to_edge(UP)
        self.play(Write(title))

        # 3. Upgrading the Head Visual: Draw a top-down head outline
        # (Ellipse with nose & ears for orientation)
        head_base = Ellipse(width=5, height=6.5, color=BLUE_A, fill_opacity=0.1)
        nose = Triangle(color=BLUE_A, fill_opacity=0.1).scale(0.3).move_to(head_base.get_top() + UP * 0.1)
        left_ear = Circle(radius=0.4, color=BLUE_A, fill_opacity=0.1).move_to(head_base.get_left() + LEFT * 0.1)
        right_ear = Circle(radius=0.4, color=BLUE_A, fill_opacity=0.1).move_to(head_base.get_right() + RIGHT * 0.1)
        head_outline = VGroup(head_base, nose, left_ear, right_ear)
        
        # 10-20 Grid approximation
        node_positions = [
            [0, 2.5, 0],
            [-1.5, 1.5, 0], [1.5, 1.5, 0], [0, 1.0, 0],
            [-2.2, 0, 0], [-1.0, 0, 0], [0, -0.5, 0], [1.0, 0, 0], [2.2, 0, 0],
            [-1.5, -1.5, 0], [1.5, -1.5, 0], [0, -2.0, 0],
            [0, -3.0, 0]
        ]
        
        nodes = VGroup(*[Dot(pos, color=BLUE, radius=0.12) for pos in node_positions])
        
        # Living Plot Tracker for waves
        wave_offset = ValueTracker(0)
        
        waves = always_redraw(lambda: VGroup(*[
            FunctionGraph(
                lambda x: 0.3 * np.sin(3 * x - i*0.5 + wave_offset.get_value()), 
                x_range=[-3, 3], 
                color=BLUE_C
            ).shift(DOWN*2.5 + UP*(i*0.6))
            for i in range(3)
        ]))

        with self.voiceover(text="Your brain is like a massive, complex symphony orchestra, with billions of neurons firing in perfect harmony.") as tracker:
            self.play(FadeIn(head_outline), run_time=tracker.duration * 0.3)
            self.play(LaggedStart(*[FadeIn(node, shift=DOWN*0.5) for node in nodes], lag_ratio=0.05), run_time=tracker.duration * 0.7)

        # 2. Elevating the "Symphony" Metaphor
        # Note: Using SVGMobject or simple shapes instead of Text("🎵") as emoji fonts can be unreliable in Manim
        # We'll use a stylized sine wave and particle effects to represent music
        pulse_circle = Circle(radius=0.1, color=BLUE_B, stroke_opacity=0).move_to(DOWN*1.5)
        
        with self.voiceover(text="To listen to this music, scientists and doctors use Electroencephalography, or EEG.") as tracker:
            self.play(Create(waves), run_time=tracker.duration * 0.6)
            self.play(
                pulse_circle.animate(rate_func=there_and_back).scale(15).set_stroke(opacity=0.5), 
                run_time=tracker.duration * 0.4
            )

        with self.voiceover(text="They place tiny microphones—called electrodes or channels—across the scalp to record the electrical melodies of the mind.") as tracker:
            self.play(wave_offset.animate.increment_value(5), run_time=tracker.duration, rate_func=linear)

        # ---------------------------------------------------------
        # Subtopic 2: The Disconnect (When EEG Fails)
        # ---------------------------------------------------------
        subtitle = Text("The Disconnect: Noise & Missing Data").to_edge(UP)
        
        bad_idx = 4
        missing_idx = 8
        bad_node = nodes[bad_idx]
        missing_node = nodes[missing_idx]

        jagged_waves = always_redraw(lambda: VGroup(*[
            FunctionGraph(
                lambda x: 0.3 * np.sin(3 * x - i*0.5 + wave_offset.get_value()) + 0.2 * np.sin(25 * x + wave_offset.get_value()*5), 
                x_range=[-3, 3], 
                color=RED
            ).shift(DOWN*2.5 + UP*(i*0.6))
            for i in range(3)
        ]))

        with self.voiceover(text="But recording the brain is messy. In the real world, patients move, wires get bumped, and sensors lose connection.") as tracker:
            self.play(Transform(title, subtitle), run_time=tracker.duration * 0.4)
            self.play(
                bad_node.animate.set_color(RED).scale(1.5).shift(UP*0.2 + RIGHT*0.2),
                Transform(waves, jagged_waves),
                run_time=tracker.duration * 0.6
            )

        cross = Cross(stroke_color=RED, stroke_width=4, scale_factor=0.2).move_to(node_positions[missing_idx])
        
        with self.voiceover(text="Suddenly, our beautiful symphony is interrupted by harsh static, or worse—complete silence from missing channels.") as tracker:
            self.play(
                Circumscribe(bad_node, color=RED, time_width=2),
                FadeOut(missing_node, scale=0.2),
                Create(cross),
                wave_offset.animate.increment_value(5),
                run_time=tracker.duration,
                rate_func=linear
            )

        # ---------------------------------------------------------
        # Subtopic 3: The AI Bottleneck (Why Rigid Models Fail)
        # ---------------------------------------------------------
        subtitle3 = Text("The AI Bottleneck").to_edge(UP)
        
        # Move surviving nodes to the left
        left_shift = LEFT * 3.5
        
        # Rigid grid representing traditional AI
        grid_square = Square(side_length=4, color=GRAY, fill_opacity=0.2).shift(RIGHT*2.5)
        # Creating a 4x4 grid plane
        grid_lines = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            background_line_style={"stroke_color": GRAY, "stroke_width": 2}
        ).set_width(4).set_height(4).move_to(grid_square)

        model_label = Text("Rigid AI Model", font_size=28).next_to(grid_square, DOWN)
        model = VGroup(grid_square, grid_lines, model_label)
        
        with self.voiceover(text="We want to use artificial intelligence to decode these signals to help diagnose diseases or build brain-computer interfaces.") as tracker:
            self.play(Transform(title, subtitle3), run_time=tracker.duration * 0.2)
            self.play(
                FadeOut(head_outline), 
                FadeOut(waves),
                FadeOut(cross),
                run_time=tracker.duration * 0.3
            )
            self.play(nodes.animate.shift(left_shift), FadeIn(model, shift=UP), run_time=tracker.duration * 0.5)

        # 1. The "Fixed Seating Chart" Logic (Crucial Conceptual Fix)
        # 13 slots for the 13 nodes (arranged somewhat sequentially around the 4x4 grid)
        slots = [
            [-1.5, 1.5], [-0.5, 1.5], [0.5, 1.5], [1.5, 1.5],
            [-1.5, 0.5], [-0.5, 0.5], [0.5, 0.5], [1.5, 0.5],
            [-1.5, -0.5], [-0.5, -0.5], [0.5, -0.5], [1.5, -0.5],
            [-1.5, -1.5]
        ]
        
        animations = []
        
        # Zip nodes and slots together to enforce the 1-to-1 rigid mapping
        for i, (node, slot) in enumerate(zip(nodes, slots)):
            target = grid_lines.c2p(slot[0], slot[1])
            
            if i == missing_idx:
                # Highlight the missing data the rigid AI was expecting
                empty_highlight = Square(side_length=0.8, color=RED, stroke_width=4).move_to(target)
                animations.append(Create(empty_highlight))
                continue
            
            animations.append(node.animate.move_to(target))

        error_msg = Text("ERROR: Data Mismatch", color=RED, font_size=32, weight=BOLD)
        error_bg = BackgroundRectangle(error_msg, color=BLACK, fill_opacity=0.9, buff=0.2)
        error = VGroup(error_bg, error_msg).move_to(grid_square)

        with self.voiceover(text="But there is a major bottleneck. Traditional AI models are incredibly rigid.") as tracker:
            self.play(LaggedStart(*animations, lag_ratio=0.1), run_time=tracker.duration)

        # 4. Refining the Error State
        with self.voiceover(text="They require a fixed 'seating chart.' If you hand them a recording with missing channels or a different electrode layout, the model breaks.") as tracker:
            self.play(
                grid_square.animate.set_color(RED),
                grid_lines.animate.set_color(RED),
                # Turn all remaining healthy nodes gray to show systemic failure
                *[nodes[i].animate.set_color(GRAY) for i in range(len(nodes)) if i != missing_idx and i != bad_idx],
                FadeIn(error, scale=0.5),
                run_time=tracker.duration * 0.5
            )
            self.play(Wiggle(model), run_time=tracker.duration * 0.5)