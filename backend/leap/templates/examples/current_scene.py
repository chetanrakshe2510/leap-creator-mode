from manim import *
import numpy as np

class ReverseNormalization(Scene):
    def construct(self):
        # ============================================================
        # PART 1: THE CURRENCY EXCHANGE ANALOGY
        # ============================================================
        title = Text("Reverse Normalization", font_size=42, color=YELLOW).to_edge(UP)
        subtitle = Text("The Currency Exchange", font_size=28, color=GRAY).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(subtitle))

        # --- Stage 1: Departure (Normalization) ---
        stage1 = Text("Departure: Normalization", font_size=28, color=BLUE).shift(UP * 2)
        self.play(ReplacementTransform(subtitle, stage1))

        # Show $100 bill
        dollar_box = VGroup(
            RoundedRectangle(width=3, height=1.5, corner_radius=0.15, color=GREEN, fill_opacity=0.2),
            Text("$100", font_size=36, color=GREEN)
        ).shift(LEFT * 4)
        raw_label = Text("Raw Data", font_size=18, color=GRAY).next_to(dollar_box, DOWN, buff=0.2)

        self.play(FadeIn(dollar_box), Write(raw_label))

        # Exchange counter
        counter = VGroup(
            RoundedRectangle(width=2.5, height=1.8, corner_radius=0.15, color=YELLOW, fill_opacity=0.15),
            Text("Exchange", font_size=18, color=YELLOW),
            Text("$100 = 1 Token", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.1).move_to(ORIGIN)

        self.play(FadeIn(counter))

        # Arrow: Dollar -> Counter
        arr1 = Arrow(dollar_box.get_right(), counter.get_left(), color=BLUE, buff=0.2)
        self.play(GrowArrow(arr1))

        # Token result
        token_box = VGroup(
            RoundedRectangle(width=2.5, height=1.5, corner_radius=0.15, color=BLUE, fill_opacity=0.2),
            Text("1.0 Token", font_size=30, color=BLUE)
        ).shift(RIGHT * 4)
        norm_label = Text("Normalized", font_size=18, color=GRAY).next_to(token_box, DOWN, buff=0.2)

        arr2 = Arrow(counter.get_right(), token_box.get_left(), color=BLUE, buff=0.2)
        self.play(GrowArrow(arr2), FadeIn(token_box), Write(norm_label))
        self.wait(1)

        # --- Stage 2: The Prediction (Transaction) ---
        self.play(FadeOut(VGroup(dollar_box, raw_label, counter, arr1, arr2)))

        stage2 = Text("Transaction: Model Predicts", font_size=28, color=PURPLE).shift(UP * 2)
        self.play(ReplacementTransform(stage1, stage2))

        # Model box
        model_box = VGroup(
            RoundedRectangle(width=3, height=2, corner_radius=0.2, color=PURPLE, fill_opacity=0.15),
            Text("Neural\nNetwork", font_size=22, color=PURPLE),
            Text("+50% growth", font_size=16, color=GRAY)
        ).arrange(DOWN, buff=0.1).move_to(ORIGIN)

        arr3 = Arrow(token_box.get_left(), model_box.get_right(), color=PURPLE, buff=0.2)
        self.play(FadeIn(model_box), GrowArrow(arr3))

        # Output
        output_box = VGroup(
            RoundedRectangle(width=2.5, height=1.5, corner_radius=0.15, color=PURPLE, fill_opacity=0.2),
            Text("1.5 Tokens", font_size=30, color=PURPLE)
        ).shift(LEFT * 4)
        pred_label = Text("Prediction", font_size=18, color=GRAY).next_to(output_box, DOWN, buff=0.2)

        arr4 = Arrow(model_box.get_left(), output_box.get_right(), color=PURPLE, buff=0.2)
        self.play(GrowArrow(arr4), FadeIn(output_box), Write(pred_label))
        self.wait(1)

        # --- Stage 3: Return (Denormalization) ---
        self.play(FadeOut(VGroup(token_box, norm_label, model_box, arr3, arr4)))

        stage3 = Text("Return: Denormalization", font_size=28, color=GREEN).shift(UP * 2)
        self.play(ReplacementTransform(stage2, stage3))

        # Move output_box center-left
        self.play(output_box.animate.move_to(LEFT * 4), pred_label.animate.next_to(LEFT * 4 + DOWN * 1, DOWN, buff=0))

        # Reverse exchange
        rev_counter = VGroup(
            RoundedRectangle(width=2.5, height=1.8, corner_radius=0.15, color=GREEN, fill_opacity=0.15),
            Text("Reverse", font_size=18, color=GREEN),
            Text("1 Token = $100", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.1).move_to(ORIGIN)

        arr5 = Arrow(output_box.get_right(), rev_counter.get_left(), color=GREEN, buff=0.2)
        self.play(FadeIn(rev_counter), GrowArrow(arr5))

        # Calculation
        calc = MathTex("1.5 \\times \\$100 = \\$150", font_size=30, color=GREEN).shift(DOWN * 2)
        self.play(Write(calc))

        # Final result
        result_box = VGroup(
            RoundedRectangle(width=3, height=1.5, corner_radius=0.15, color=GREEN, fill_opacity=0.3),
            Text("$150", font_size=42, color=GREEN)
        ).shift(RIGHT * 4)
        real_label = Text("Real-World Value!", font_size=18, color=GREEN).next_to(result_box, DOWN, buff=0.2)

        arr6 = Arrow(rev_counter.get_right(), result_box.get_left(), color=GREEN, buff=0.2)
        self.play(GrowArrow(arr6), FadeIn(result_box), Write(real_label))
        self.wait(2)

        # Key takeaway
        takeaway = Text(
            "Model thinks in Tokens. Humans think in Dollars.",
            font_size=22, color=YELLOW
        ).to_edge(DOWN)
        self.play(Write(takeaway))
        self.wait(2)

        # Clear for Part 2
        self.play(FadeOut(Group(*self.mobjects)))

        # ============================================================
        # PART 2: THE MATH (Algebra in Reverse)
        # ============================================================
        part2_title = Text("The Math: Algebra in Reverse", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(part2_title))

        # --- Min-Max Denormalization ---
        mm_title = Text("1. Min-Max Denormalization", font_size=28, color=BLUE).shift(UP * 2)
        self.play(Write(mm_title))

        forward_mm = MathTex(
            r"Forward:\quad x_{norm} = \frac{x - \text{min}}{\text{max} - \text{min}}",
            font_size=32
        ).shift(UP * 0.8)
        forward_mm.set_color(GRAY)

        reverse_mm = MathTex(
            r"Reverse:\quad x = x_{norm} \times (\text{max} - \text{min}) + \text{min}",
            font_size=32, color=BLUE
        ).shift(DOWN * 0.2)

        self.play(Write(forward_mm))
        self.wait(0.5)

        # Arrow showing reversal
        rev_arrow = MathTex(r"\Downarrow \text{ Rearrange}", font_size=24, color=YELLOW).shift(UP * 0.3)
        self.play(Write(rev_arrow))
        self.play(Write(reverse_mm))

        # Example
        example_mm = MathTex(
            r"x_{norm}=0.5,\; \text{min}=40,\; \text{max}=60",
            r"\Rightarrow x = 0.5 \times 20 + 40 = 50",
            font_size=26, color=GREEN
        ).shift(DOWN * 1.5)
        self.play(Write(example_mm))
        self.wait(2)

        self.play(FadeOut(VGroup(mm_title, forward_mm, rev_arrow, reverse_mm, example_mm)))

        # --- Z-Score Denormalization ---
        zs_title = Text("2. Z-Score Denormalization", font_size=28, color=PURPLE).shift(UP * 2)
        self.play(Write(zs_title))

        forward_zs = MathTex(
            r"Forward:\quad z = \frac{x - \mu}{\sigma}",
            font_size=32
        ).shift(UP * 0.8)
        forward_zs.set_color(GRAY)

        reverse_zs = MathTex(
            r"Reverse:\quad x = z \times \sigma + \mu",
            font_size=32, color=PURPLE
        ).shift(DOWN * 0.2)

        self.play(Write(forward_zs))
        self.wait(0.5)

        rev_arrow2 = MathTex(r"\Downarrow \text{ Rearrange}", font_size=24, color=YELLOW).shift(UP * 0.3)
        self.play(Write(rev_arrow2))
        self.play(Write(reverse_zs))

        # Example
        example_zs = MathTex(
            r"z=1.5,\; \mu=50,\; \sigma=10",
            r"\Rightarrow x = 1.5 \times 10 + 50 = 65",
            font_size=26, color=GREEN
        ).shift(DOWN * 1.5)
        self.play(Write(example_zs))
        self.wait(2)

        # Final message
        final = Text(
            "Normalize to think. Denormalize to understand.",
            font_size=26, color=YELLOW
        ).to_edge(DOWN)
        self.play(Write(final))
        self.wait(3)
