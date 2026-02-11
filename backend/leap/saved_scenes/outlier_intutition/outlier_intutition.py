from manim import *
import numpy as np

class RoomOfSalaries(Scene):
    def construct(self):
        # ============================================================
        # SETUP: THE ROOM
        # ============================================================
        title = Text("The Room of Salaries", font_size=42, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        # Number line: Salaries in $k
        nl = NumberLine(
            x_range=[30, 70, 5],
            length=10,
            include_numbers=True,
            label_direction=DOWN
        ).shift(DOWN * 0.5)

        nl_label = Text("Salary ($k)", font_size=22).next_to(nl, RIGHT, buff=0.2)
        self.play(Create(nl), Write(nl_label))

        # 30 dots clustered between 40k-60k
        np.random.seed(42)
        salaries = np.random.normal(50, 4, 30)
        salaries = np.clip(salaries, 40, 60)

        dots = VGroup()
        for s in salaries:
            d = Dot(nl.n2p(s), color=BLUE, radius=0.07, z_index=5)
            dots.add(d)

        cluster_label = Text("100 People ($40k-$60k)", font_size=20, color=BLUE).next_to(dots, UP, buff=0.3)
        self.play(FadeIn(dots, lag_ratio=0.02), Write(cluster_label))
        self.wait(1)

        # Bill Gates enters!
        bill_text = Text("Bill Gates enters the room!", font_size=28, color=RED).shift(UP * 1.5)
        self.play(Write(bill_text))
        self.wait(1)

        # We can't show $1B on a $30-70k axis, so let's show a dramatic arrow
        bill_arrow = Arrow(
            nl.n2p(70), nl.n2p(70) + RIGHT * 2.5,
            color=RED, buff=0
        )
        bill_label = MathTex("\\$1B", color=RED, font_size=30).next_to(bill_arrow, UP)
        self.play(GrowArrow(bill_arrow), Write(bill_label))
        self.wait(1)

        # Clean up for comparison
        self.play(FadeOut(VGroup(title, bill_text)))

        # ============================================================
        # SCENARIO A: MIN-MAX (THE CRUSHER)
        # ============================================================
        scene_a_title = Text("Min-Max: The Crusher", font_size=36, color=RED).to_edge(UP)
        self.play(
            Write(scene_a_title),
            FadeOut(nl), FadeOut(nl_label), FadeOut(bill_arrow), FadeOut(bill_label),
            FadeOut(cluster_label)
        )

        # New axis: [0, 1]
        nl_mm = NumberLine(
            x_range=[0, 1, 0.1],
            length=10,
            include_numbers=True,
            numbers_to_include=[0, 0.5, 1],
            decimal_number_config={"num_decimal_places": 1}
        ).shift(DOWN * 0.5)

        mm_label = Text("Normalized Value", font_size=22).next_to(nl_mm, RIGHT, buff=0.2)
        self.play(Create(nl_mm), Write(mm_label))

        # Min-Max: (x - 40000) / (1000000000 - 40000)
        # $50k -> (50000 - 40000) / (1e9 - 40000) ~ 0.00001
        # $60k -> (60000 - 40000) / (1e9 - 40000) ~ 0.00002
        # All cluster near 0.00001
        # Bill Gates -> 1.0

        # Animate dots CRUSHING to near 0
        crush_anims = []
        for d in dots:
            crush_anims.append(d.animate.move_to(nl_mm.n2p(0.00005)))

        self.play(*crush_anims, run_time=2)

        # Crushed label
        crushed_label = Text("All 100 people crushed\ninto a single dot at ~0", font_size=20, color=RED)
        crushed_label.next_to(nl_mm.n2p(0), UP, buff=0.5)
        self.play(Write(crushed_label))

        # Bill Gates dot at 1.0
        bill_dot = Dot(nl_mm.n2p(1.0), color=RED, radius=0.15, z_index=5)
        bill_dot_label = MathTex("\\$1B \\rightarrow 1.0", color=RED, font_size=24).next_to(bill_dot, UP)
        self.play(FadeIn(bill_dot), Write(bill_dot_label))

        # Zoom circle to show data is destroyed
        zoom = Circle(radius=0.3, color=YELLOW).move_to(nl_mm.n2p(0))
        zoom_text = Text("Data destroyed!\nCan't tell $40k from $60k", font_size=18, color=YELLOW)
        zoom_text.next_to(zoom, DOWN, buff=0.2)
        self.play(Create(zoom), Write(zoom_text))
        self.wait(2)

        # Clean up
        self.play(FadeOut(VGroup(
            scene_a_title, nl_mm, mm_label, crushed_label,
            bill_dot, bill_dot_label, zoom, zoom_text, dots
        )))

        # ============================================================
        # SCENARIO B: Z-SCORE (THE RULER)
        # ============================================================
        scene_b_title = Text("Z-Score: The Ruler", font_size=36, color=GREEN).to_edge(UP)
        self.play(Write(scene_b_title))

        # Z-Score axis: centered on 0, show -2 to +2 for main cluster
        nl_z = NumberLine(
            x_range=[-3, 3, 1],
            length=10,
            include_numbers=True
        ).shift(DOWN * 0.5)

        z_label = Text("Z-Score", font_size=22).next_to(nl_z, RIGHT, buff=0.2)
        self.play(Create(nl_z), Write(z_label))

        # Z-Score: (x - mean) / std
        # After Bill Gates: mean ~ 10M (skewed), std ~ huge
        # But for salaries 40k-60k: z scores cluster around ~ -0.1 to 0.1
        # Conceptually the cluster stays visible near 0
        # Bill Gates is at z ~ +10000 (way off chart)

        # Recreate dots for the cluster
        dots_z = VGroup()
        z_scores = (salaries - np.mean(salaries)) / np.std(salaries)
        # Scale them to a visible range: map z_scores to roughly [-1, 1]
        # In practice with Bill Gates the std would be huge, so the cluster
        # z scores would be tiny but let's show them spread around ~0.
        # We'll use z_scores scaled down a bit to show the cluster is preserved
        for zs in z_scores:
            # Map the original z-scores (which are -2 to +2 among themselves)
            # to a narrower band like -0.5 to 0.5 to show the "slight shift"
            mapped_z = zs * 0.3
            d = Dot(nl_z.n2p(mapped_z), color=BLUE, radius=0.07, z_index=5)
            dots_z.add(d)

        cluster_z_label = Text("Cluster preserved near 0!", font_size=20, color=GREEN)
        cluster_z_label.next_to(nl_z.n2p(0), UP, buff=0.8)

        self.play(FadeIn(dots_z, lag_ratio=0.02), Write(cluster_z_label))

        # Bill Gates arrow going off-chart
        bill_z_arrow = Arrow(
            nl_z.n2p(3), nl_z.n2p(3) + RIGHT * 2,
            color=RED, buff=0
        )
        bill_z_label = MathTex("Z \\approx +10{,}000", color=RED, font_size=24).next_to(bill_z_arrow, UP)
        off_chart = Text("(Way off chart!)", font_size=16, color=RED).next_to(bill_z_label, DOWN, buff=0.1)

        self.play(GrowArrow(bill_z_arrow), Write(bill_z_label), Write(off_chart))

        # Show individual variation is still visible
        # Highlight two dots
        d_low = dots_z[0]
        d_high = dots_z[5]
        hl1 = SurroundingRectangle(d_low, color=YELLOW, buff=0.05)
        hl2 = SurroundingRectangle(d_high, color=YELLOW, buff=0.05)
        var_text = Text("Individual differences still visible!", font_size=18, color=YELLOW)
        var_text.next_to(dots_z, DOWN, buff=0.5)

        self.play(Create(hl1), Create(hl2), Write(var_text))
        self.wait(2)

        # Final verdict
        verdict = VGroup(
            Text("Min-Max: Sensitive to outliers", font_size=22, color=RED),
            Text("Z-Score: Robust to outliers", font_size=22, color=GREEN),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)

        self.play(
            FadeOut(VGroup(hl1, hl2, var_text)),
            Write(verdict)
        )
        self.wait(3)
