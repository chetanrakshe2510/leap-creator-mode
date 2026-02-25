import sys
from pathlib import Path
# Add backend directory to sys.path BEFORE importing from leap
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from leap.services.kokoro_service import KokoroService

class ZunaScene3Voiceover(VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="am_michael", speed=1.0))

        # ---------------------------------------------------------
        # Subtopic 1: The Encoder (The Context Squeeze)
        # ---------------------------------------------------------
        title = Text("The Diffusion Sculptor").to_edge(UP)
        self.play(Write(title))

        # 3D Head representation (Top-down view)
        head_base = Ellipse(width=3, height=4, color=BLUE_A, fill_opacity=0.1)
        nose = Triangle(color=BLUE_A, fill_opacity=0.1).scale(0.2).move_to(head_base.get_top() + UP * 0.05)
        head_outline = VGroup(head_base, nose).shift(LEFT * 4)

        # Active healthy electrodes on the right side
        active_nodes = VGroup(*[
            Dot(color=BLUE, radius=0.1).move_to(
                head_outline.get_center() + np.array([np.random.uniform(0.2, 1.0), np.random.uniform(-1.0, 1.0), 0])
            ) for _ in range(12)
        ])
        
        # Missing patch on the left side
        missing_patch = Ellipse(width=1, height=2, color=RED, fill_opacity=0.2).move_to(head_outline.get_center() + LEFT*0.7)

        # Elements for the funnel
        funnel_pts = [[-1, 1.5, 0], [1, 1.5, 0], [0.3, -1, 0], [-0.3, -1, 0]]
        funnel = Polygon(*funnel_pts, color=PURPLE, fill_opacity=0.2).move_to(RIGHT * 1 + UP * 0.5)
        encoder_label = Text("Encoder", font_size=24).next_to(funnel, UP)

        tokens = VGroup(*[
            Rectangle(width=0.2, height=0.4, color=BLUE, fill_opacity=0.5).move_to(node.get_center())
            for node in active_nodes
        ])

        latent_sphere = Circle(radius=0.4, color=YELLOW, fill_opacity=1).move_to(funnel.get_bottom() + DOWN*0.8)
        latent_label = Text("Latent Bottleneck", font_size=20).next_to(latent_sphere, DOWN)

        with self.voiceover(text="Now that the data is organized, ZUNA has to fill in the blanks. It uses an Encoder-Decoder system. First, the Encoder gathers all the surviving, healthy signals.") as tracker:
            self.play(
                FadeIn(head_outline), FadeIn(active_nodes), FadeIn(missing_patch),
                run_time=tracker.duration * 0.4
            )
            self.play(
                Create(funnel), Write(encoder_label),
                run_time=tracker.duration * 0.6
            )

        with self.voiceover(text="It squeezes this massive amount of data into a dense, compressed summary of the brain's current state, capturing the deep correlations between different areas of the scalp.") as tracker:
            self.play(
                LaggedStart(
                    *[token.animate.move_to(funnel.get_top() + UP*0.5).set_opacity(0) for token in tokens],
                    lag_ratio=0.1,
                    run_time=tracker.duration * 0.5
                )
            )
            self.play(FadeIn(latent_sphere, scale=0.1), Write(latent_label), run_time=tracker.duration * 0.3)
            # Intense bright sphere compression effect
            self.play(latent_sphere.animate.set_color(WHITE).set_fill(color=YELLOW, opacity=1).scale(1.2), rate_func=there_and_back, run_time=tracker.duration * 0.2)
        
        # Fade out the funnel to clear the stage for the noise wave connection
        self.play(FadeOut(funnel), FadeOut(encoder_label))

        # ---------------------------------------------------------
        # Subtopic 2: The Blank Canvas (Gaussian Noise)
        # ---------------------------------------------------------
        subtitle2 = Text("The Blank Canvas: Gaussian Noise").to_edge(UP)

        # Placeholder electrode on the missing left side
        placeholder = Dot(color=RED, radius=0.15).move_to(missing_patch.get_center())
        
        # Pure random static generation
        noise_wave = always_redraw(lambda: FunctionGraph(
            lambda x: np.random.uniform(-1, 1),
            x_range=[-2, 2],
            color=RED
        ).move_to(RIGHT * 4 + UP * 0.5))

        noise_connection = DashedLine(placeholder.get_right(), noise_wave.get_left(), color=RED)

        with self.voiceover(text="Where channels are missing or completely broken, ZUNA doesn't just try to draw a line connecting the dots.") as tracker:
            self.play(Transform(title, subtitle2), run_time=tracker.duration * 0.3)
            self.play(FadeIn(placeholder, scale=5), run_time=tracker.duration * 0.7)

        with self.voiceover(text="Instead, it starts with a completely blank canvas: pure, random static, also known as Gaussian noise.") as tracker:
            self.play(Create(noise_connection), Create(noise_wave), run_time=tracker.duration)

        # ---------------------------------------------------------
        # Subtopic 3: The Decoder (The Sculptor)
        # ---------------------------------------------------------
        subtitle3 = Text("The Decoder: Sculpting the Signal").to_edge(UP)
        
        # The Decoder (crystalline filters / Transformer layers)
        decoder_layers = VGroup(*[
            Rectangle(width=0.2, height=2, color=TEAL, fill_opacity=0.3).move_to(RIGHT * (-2 + i*0.5) + UP * 0.5)
            for i in range(8) # Representing 16 layers visually
        ])
        decoder_label = Text("Transformer Layers", font_size=24).next_to(decoder_layers, UP, buff=0.5)
        
        # Adaptive conditioning beams
        beams = VGroup(*[
            Line(latent_sphere.get_right(), layer.get_left(), color=YELLOW, stroke_opacity=0.5)
            for layer in decoder_layers
        ])

        with self.voiceover(text="This is where the magic of Diffusion happens. The Decoder acts as a digital sculptor.") as tracker:
            self.play(Transform(title, subtitle3), run_time=tracker.duration * 0.2)
            # Clean up screen for split view
            self.play(
                FadeOut(head_outline), FadeOut(active_nodes), FadeOut(missing_patch),
                FadeOut(placeholder), FadeOut(noise_connection),
                run_time=tracker.duration * 0.4
            )
            # Spread layout for Decoder process
            self.play(
                VGroup(latent_sphere, latent_label).animate.move_to(LEFT * 5),
                run_time=tracker.duration * 0.4
            )

        with self.voiceover(text="Guided by the summary of the healthy channels and the exact 4D location of the missing sensor, it takes that pure static and iteratively chips away the noise.") as tracker:
            self.play(FadeIn(decoder_layers), Write(decoder_label), run_time=tracker.duration * 0.4)
            # Freeze the redrawable noise to manipulate it directly
            noise_wave.clear_updaters()
            self.play(LaggedStart(*[Create(beam) for beam in beams], lag_ratio=0.1), run_time=tracker.duration * 0.6)

        with self.voiceover(text="Step by step, it refines the chaos until a perfectly plausible brainwave emerges, perfectly in tune with the rest of the symphony.") as tracker:
            current_wave = noise_wave
            
            # Subdivide the remaining time by 8 layers
            step_time = tracker.duration / 8
            
            for i in range(8):
                progress = (i + 1) / 8
                new_wave = FunctionGraph(
                    lambda x: (1 - progress) * np.random.uniform(-1, 1) + progress * np.sin(3 * x),
                    x_range=[-2, 2],
                    color=interpolate_color(RED, BLUE, progress)
                ).move_to(RIGHT * 4 + UP * 0.5)
                
                self.play(
                    decoder_layers[i].animate.set_fill(opacity=0.8),
                    Transform(current_wave, new_wave),
                    run_time=step_time * 0.7
                )
                self.play(decoder_layers[i].animate.set_fill(opacity=0.3), run_time=step_time * 0.3)

        # ---------------------------------------------------------
        # The Mathematical Layer & Table
        # ---------------------------------------------------------
        math_title = Text("The Math of Diffusion").to_edge(UP)
        
        eq1 = MathTex("q(x_t | x_{t-1}) = \\mathcal{N}(x_t; \\sqrt{1 - \\beta_t} x_{t-1}, \\beta_t I)", font_size=36)
        eq1_label = Text("1. Forward Process (Adding Noise)", font_size=24, color=RED).next_to(eq1, UP, aligned_edge=LEFT)
        g1 = VGroup(eq1_label, eq1).move_to(UP)

        eq2 = MathTex("p_\\theta(x_{0:T}) = p(x_T) \\prod_{t=1}^T p_\\theta(x_{t-1} | x_t)", font_size=36)
        eq2_label = Text("2. Reverse Process (Sculpting/Generation)", font_size=24, color=TEAL).next_to(eq2, UP, aligned_edge=LEFT)
        g2 = VGroup(eq2_label, eq2).move_to(DOWN)

        with self.voiceover(text="To understand the sculptor's chiseling process, we look at the math of diffusion models. The AI is trained by first learning how to destroy data") as tracker:
            self.play(
                Transform(title, math_title),
                FadeOut(latent_sphere), FadeOut(latent_label), FadeOut(beams),
                FadeOut(decoder_layers), FadeOut(decoder_label), FadeOut(current_wave),
                run_time=tracker.duration * 0.5
            )
            self.play(Write(g1), run_time=tracker.duration * 0.5)

        with self.voiceover(text="and then learning how to reverse that exact process, predicting how to remove noise step-by-step to arrive back at the clean data.") as tracker:
            self.play(Write(g2), run_time=tracker.duration)

        # Pros and Cons table
        pros_cons_title = Text("Diffusion Autoencoders for EEG", font_size=36).to_edge(UP)
        
        table_data = [
            ["Iterative Denoising", "High-fidelity, realistic continuous data", "Computationally heavier and slower"],
            ["Latent Bottleneck", "Highly generalizable, deep rules", "Sparse data may lead to hallucinations"]
        ]
        table = Table(
            table_data,
            col_labels=[Text("Feature"), Text("Pros"), Text("Cons")],
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": GRAY}
        ).scale(0.35)

        with self.voiceover(text="This approach carries clear pros and cons. The iterative denoising leads to incredibly realistic data generation, but is computationally heavy.") as tracker:
            self.play(Transform(title, pros_cons_title), FadeOut(g1), FadeOut(g2), run_time=tracker.duration * 0.4)
            self.play(FadeIn(table, shift=UP), run_time=tracker.duration * 0.6)

        with self.voiceover(text="And while the latent bottleneck forces the AI to learn deep fundamental rules, if the input data is too sparse, it might hallucinate incorrect waves.") as tracker:
            self.wait(tracker.duration)
