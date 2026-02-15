# LEAP_VERTICAL
from manim import *
import numpy as np

class ICAMathVertical(Scene):
    def construct(self):
        # 1. Setup Canvas (Vertical 9:16)
        # Effective width ~4.5, height ~8.0
        
        # Title
        title_group = VGroup(
            Text("ICA Math", font_size=40, weight=BOLD),
            Text("Cocktail Party Problem", font_size=24, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        title_group.to_edge(UP, buff=1.0)
        
        self.play(Write(title_group))
        
        # 2. Source Signals (Hidden Latent Variables)
        # Stack them vertically
        y_positions = [2.5, 0.5, -1.5, -3.5] # Approx vertical slots
        
        # Source 1: Sine
        def s1_func(t):
            return 0.5 * np.sin(3 * t)
            
        # Source 2: Sawtooth/Triangle
        def s2_func(t):
            return 0.5 * (2 * (t % 1) - 1) # simplified sawtooth-ish
            
        axes_sources = Axes(
            x_range=[0, 6, 1],
            y_range=[-1, 1, 1],
            x_length=3.5,
            y_length=1.2,
            axis_config={"include_ticks": False}
        ).move_to(UP * y_positions[0])
        
        source1 = axes_sources.plot(s1_func, color=BLUE)
        source2 = axes_sources.plot(s2_func, color=RED).next_to(source1, DOWN, buff=0.5)
        
        sources_label = Text("Original Sources (S)", font_size=24, color=YELLOW).next_to(axes_sources, UP, buff=0.1)
        
        self.play(FadeIn(sources_label))
        self.play(Create(source1), Create(source2))
        
        # 3. Mixing Matrix A (The Mathematics)
        # X = AS
        matrix_eq = MathTex(
            r"\begin{pmatrix} x_1 \\ x_2 \end{pmatrix}", # X
            r"=",
            r"\begin{pmatrix} 0.8 & 0.3 \\ 0.2 & 0.7 \end{pmatrix}", # A
            r"\begin{pmatrix} s_1 \\ s_2 \end{pmatrix}", # S
            font_size=32
        )
        matrix_eq.move_to(UP * y_positions[1])
        
        self.play(Write(matrix_eq))
        self.wait(1)
        
        # 4. Mixed Signals (Observed Data X)
        # x1 = 0.8*s1 + 0.3*s2
        # x2 = 0.2*s1 + 0.7*s2
        
        def x1_func(t):
            return 0.8 * s1_func(t) + 0.3 * s2_func(t)
            
        def x2_func(t):
            return 0.2 * s1_func(t) + 0.7 * s2_func(t)
            
        axes_mixed = axes_sources.copy().move_to(UP * y_positions[2] + UP * 0.5)
        
        mix1 = axes_mixed.plot(x1_func, color=PURPLE)
        mix2 = axes_mixed.plot(x2_func, color=ORANGE).next_to(mix1, DOWN, buff=0.5)
        
        mixed_label = Text("Mixed Signals (X)", font_size=24, color=PURPLE).next_to(axes_mixed, UP, buff=0.1)
        
        # Shift eq up a bit to make room
        self.play(
            matrix_eq.animate.scale(0.8).next_to(sources_label, DOWN, buff=2.7), # Move below sources
            FadeIn(mixed_label)
        )
        
        self.play(Create(mix1), Create(mix2))
        self.wait(1)
        
        # 5. Unmixing (ICA Goal)
        # S = WX (maximize non-Gaussianity)
        
        ica_arrow = Arrow(start=UP, end=DOWN, color=WHITE).next_to(mix2, DOWN)
        ica_text = Text("ICA: Maximize Non-Gaussianity", font_size=20).next_to(ica_arrow, RIGHT)
        
        formula_ica = MathTex(r"S \approx WX", font_size=32, color=GREEN).next_to(ica_arrow, DOWN)
        
        self.play(GrowArrow(ica_arrow), FadeIn(ica_text))
        self.play(Write(formula_ica))
        
        # 6. Recovered Signals
        # In ideal case, W is inverse of A
        # Recovers original shape (amplitude/sign might flip)
        
        axes_recovered = axes_sources.copy().move_to(DOWN * 2.5) # Bottom
        
        rec1 = axes_recovered.plot(s1_func, color=BLUE) # Ideally perfect recovery
        rec2 = axes_recovered.plot(s2_func, color=RED).next_to(rec1, DOWN, buff=0.5)
        
        rec_label = Text("Recovered Sources", font_size=24, color=GREEN).next_to(axes_recovered, UP, buff=0.1)
        
        self.play(FadeIn(rec_label))
        self.play(TransformFromCopy(mix1, rec1), TransformFromCopy(mix2, rec2))
        
        self.wait(2)
        
        # 7. Conclusion
        final_group = VGroup(
            Text("Blind Source Separation", font_size=32, color=YELLOW),
            Text("No knowledge of A needed!", font_size=24, color=WHITE)
        ).arrange(DOWN).to_edge(DOWN, buff=1.0)
        
        self.play(FadeIn(final_group))
        self.wait(3)