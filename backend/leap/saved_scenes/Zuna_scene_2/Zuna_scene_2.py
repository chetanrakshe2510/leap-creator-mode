import sys
from pathlib import Path
# Add backend directory to sys.path BEFORE importing from leap
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from leap.services.kokoro_service import KokoroService

class ZunaScene2Voiceover(VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="am_michael", speed=1.0))

        # ---------------------------------------------------------
        # Subtopic 1: Shattering the Grid (The Intuition)
        # ---------------------------------------------------------
        title = Text("The 4D Map: Shattering the Grid").to_edge(UP)
        self.play(Write(title))

        # Recreate the rigid grid from Scene 1
        grid_square = Square(side_length=4, color=RED, fill_opacity=0.2)
        grid_lines = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            background_line_style={"stroke_color": RED, "stroke_width": 2}
        ).set_width(4).set_height(4).move_to(grid_square)
        grid = VGroup(grid_square, grid_lines)
        
        self.add(grid)

        # Shatter the grid: quickly scale down and fade out while a "dust" particle effect expands
        dust_particles = VGroup(*[
            Dot(color=GRAY, radius=np.random.uniform(0.02, 0.08)).move_to(
                grid.get_center() + np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0])
            ) for _ in range(50)
        ])

        with self.voiceover(text="To solve this bottleneck, the creators of ZUNA threw out the fixed seating chart.") as tracker:
            self.play(
                FadeOut(grid, scale=0.1, run_time=tracker.duration * 0.3),
                LaggedStart(
                    *[
                        dot.animate.move_to(dot.get_center() * 3 + np.array([np.random.uniform(-2, 2), np.random.uniform(-2, 2), 0])).set_opacity(0)
                        for dot in dust_particles
                    ],
                    lag_ratio=0.01,
                    run_time=tracker.duration * 0.7
                )
            )

        # Bring back the 3D head (SVG approximation) and freely floating nodes
        head_base = Ellipse(width=3, height=4, color=BLUE_A, fill_opacity=0.1)
        nose = Triangle(color=BLUE_A, fill_opacity=0.1).scale(0.2).move_to(head_base.get_top() + UP * 0.05)
        left_ear = Circle(radius=0.25, color=BLUE_A, fill_opacity=0.1).move_to(head_base.get_left() + LEFT * 0.05)
        right_ear = Circle(radius=0.25, color=BLUE_A, fill_opacity=0.1).move_to(head_base.get_right() + RIGHT * 0.05)
        head_outline = VGroup(head_base, nose, left_ear, right_ear).shift(LEFT * 3)

        # Nodes float in freely and land on the head
        free_nodes = VGroup(*[
            Dot(color=BLUE, radius=0.1).move_to(
                head_outline.get_center() + np.array([np.random.uniform(-1.2, 1.2), np.random.uniform(-1.5, 1.5), 0])
            ) for _ in range(20)
        ])

        # Spawn them from off-screen
        for node in free_nodes:
            node.save_state()
            node.move_to(RIGHT * 6 + UP * np.random.uniform(-3, 3))

        with self.voiceover(text="Instead of forcing the brain's symphony into a rigid grid, what if we just attached a precise GPS tracker to every single note?") as tracker:
            self.play(FadeIn(head_outline, shift=UP), run_time=tracker.duration * 0.2)
            self.play(
                LaggedStart(
                    *[node.animate.restore() for node in free_nodes],
                    lag_ratio=0.05,
                    run_time=tracker.duration * 0.8
                )
            )

        # ---------------------------------------------------------
        # Subtopic 2: The Chopping Block (Tokenization)
        # ---------------------------------------------------------
        subtitle2 = Text("Tokenization: The Chopping Block").to_edge(UP)

        wave_offset = ValueTracker(0)
        continuous_wave = always_redraw(lambda: FunctionGraph(
            lambda x: 1.5 * np.sin(2 * x + wave_offset.get_value()) + 0.5 * np.sin(5 * x + wave_offset.get_value() * 2),
            x_range=[-5, 5],
            color=BLUE_C
        ))

        with self.voiceover(text="First, ZUNA acts like a digital metronome.") as tracker:
            self.play(
                Transform(title, subtitle2),
                FadeOut(head_outline),
                FadeOut(free_nodes),
                run_time=tracker.duration * 0.5
            )
            self.play(Create(continuous_wave), run_time=tracker.duration * 0.5)

        # A precise, rhythmic laser slices the wave into tokens
        slice_lines = VGroup(*[
            DashedLine(start=UP*2, end=DOWN*2, color=RED).shift(RIGHT * x)
            for x in range(-4, 5, 2)
        ])
        
        with self.voiceover(text="It takes the continuous stream of electrical data from each channel and slices it into tiny, 0.125-second windows.") as tracker:
            self.play(wave_offset.animate.increment_value(5), run_time=tracker.duration * 0.3)
            self.play(LaggedStart(*[Create(line) for line in slice_lines], lag_ratio=0.2), wave_offset.animate.increment_value(5), run_time=tracker.duration * 0.7)

        # As each slice is cut, it solidifies into a small, glowing digital block ("token")
        tokens = VGroup()
        for i in range(len(slice_lines) - 1):
            x_start = slice_lines[i].get_x()
            x_end = slice_lines[i+1].get_x()
            token_rect = Rectangle(width=(x_end - x_start) * 0.9, height=3.5, color=BLUE_B, fill_opacity=0.2).move_to([ (x_start + x_end)/2, 0, 0 ])
            tokens.add(token_rect)

        # Counter on screen showing "0.125 seconds"
        time_label = Text("0.125 seconds", font_size=24, color=YELLOW).next_to(tokens[2], UP, buff=0.3)

        with self.voiceover(text="Each of these short snapshots is packaged into a mathematical block, or 'token'.") as tracker:
            self.play(
                FadeIn(tokens, scale=0.9), 
                Write(time_label), 
                wave_offset.animate.increment_value(3), 
                run_time=tracker.duration
            )

        # ---------------------------------------------------------
        # Subtopic 3: The 4D Tag (Rotary Positional Encoding)
        # ---------------------------------------------------------
        subtitle3 = Text("The 4D Tag: Rotary Positional Encoding").to_edge(UP)

        # The camera follows one of these glowing tokens. A digital holographic tag suddenly projects out
        target_token = tokens[2]
        
        with self.voiceover(text="Next comes the breakthrough. ZUNA stamps every single token with a 4D coordinate tag.") as tracker:
            self.play(Transform(title, subtitle3), run_time=tracker.duration * 0.2)
            self.play(
                FadeOut(continuous_wave),
                FadeOut(slice_lines),
                FadeOut(time_label),
                *[FadeOut(t) for t in tokens if t != target_token],
                run_time=tracker.duration * 0.4
            )
            self.play(target_token.animate.move_to(LEFT * 4.5).scale(0.8), run_time=tracker.duration * 0.4)

        # Tag projects out
        tag_bg = RoundedRectangle(width=4.0, height=2.5, corner_radius=0.2, color=TEAL, fill_opacity=0.1).next_to(target_token, RIGHT, buff=0.5)
        
        # 4 values: X, Y, Z, and T (or m)
        coord_text = MathTex("p_{i} = (x_c, y_c, z_c, m)").move_to(tag_bg.get_center())
        tag = VGroup(tag_bg, coord_text)
        
        # Connection line
        connection = Line(target_token.get_right(), tag_bg.get_left(), color=TEAL, stroke_width=2)

        # Lines shoot out back to the 3D head
        head_outline.move_to(RIGHT * 4).scale(0.4)
        
        spatial_lines = VGroup(*[
            DashedLine(tag_bg.get_right(), head_outline.get_center() + np.array([np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5), 0]), color=YELLOW)
            for _ in range(3)
        ])
        
        # A ticking clock icon for time index (T/m)
        clock = Circle(radius=0.4, color=WHITE).next_to(tag_bg, DOWN, buff=0.5).shift(LEFT*1)
        clock_hands = VGroup(
            Line(clock.get_center(), clock.get_center() + UP*0.25, color=WHITE),
            Line(clock.get_center(), clock.get_center() + RIGHT*0.2, color=WHITE)
        )
        time_icon = VGroup(clock, clock_hands)
        time_label_m = MathTex("m = \\text{Time Step}").next_to(clock, RIGHT, buff=0.3).scale(0.7)

        with self.voiceover(text="It records the exact 3D physical location of the sensor on the scalp—the X, Y, and Z axes—") as tracker:
            self.play(
                Create(connection),
                FadeIn(tag, shift=LEFT*0.5),
                run_time=tracker.duration * 0.4
            )
            self.play(FadeIn(head_outline), run_time=tracker.duration * 0.2)
            self.play(LaggedStart(*[Create(line) for line in spatial_lines], lag_ratio=0.1), run_time=tracker.duration * 0.4)
            
        with self.voiceover(text="along with its specific moment in time. This is called 4D Rotary Positional Encoding.") as tracker:
            self.play(
                FadeIn(time_icon, shift=UP),
                Write(time_label_m),
                Rotate(clock_hands[0], angle=-PI, about_point=clock.get_center(), rate_func=linear),
                run_time=tracker.duration
            )

        with self.voiceover(text="Because of this simple mathematical tag, ZUNA no longer cares if it is fed 16 channels, 64 channels, or 256 channels. It just reads the tags.") as tracker:
            # Pulsing the tracking connections to show the tag being "read"
            self.play(
                LaggedStart(*[Wiggle(line) for line in spatial_lines], lag_ratio=0.1),
                Rotate(clock_hands[0], angle=-PI, about_point=clock.get_center(), rate_func=linear),
                run_time=tracker.duration
            )