from manim import *
import numpy as np

class ICAMathematics(Scene):
    def construct(self):
        # ============================================================
        # PART 1: THE COCKTAIL PARTY PROBLEM
        # ============================================================
        title = Text("Independent Component Analysis (ICA)", font_size=38, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        party_title = Text("The Cocktail Party Problem", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(party_title))

        # Two speakers (sources)
        s1_label = Text("Singer", font_size=18, color=RED).shift(LEFT * 5 + UP * 1)
        s2_label = Text("Guitar", font_size=18, color=GREEN).shift(LEFT * 5 + DOWN * 1)
        s1_icon = Circle(radius=0.3, color=RED, fill_opacity=0.3).next_to(s1_label, LEFT, buff=0.15)
        s2_icon = Circle(radius=0.3, color=GREEN, fill_opacity=0.3).next_to(s2_label, LEFT, buff=0.15)

        sources = VGroup(s1_icon, s1_label, s2_icon, s2_label)
        self.play(FadeIn(sources))

        # Two microphones (observations)
        m1_label = Text("Mic 1", font_size=18, color=ORANGE).shift(RIGHT * 4 + UP * 1)
        m2_label = Text("Mic 2", font_size=18, color=PURPLE).shift(RIGHT * 4 + DOWN * 1)
        m1_icon = Square(side_length=0.5, color=ORANGE, fill_opacity=0.3).next_to(m1_label, RIGHT, buff=0.15)
        m2_icon = Square(side_length=0.5, color=PURPLE, fill_opacity=0.3).next_to(m2_label, RIGHT, buff=0.15)

        mics = VGroup(m1_icon, m1_label, m2_icon, m2_label)
        self.play(FadeIn(mics))

        # Arrows: Each source reaches BOTH mics (mixing!)
        arrows = VGroup(
            Arrow(s1_icon.get_right(), m1_icon.get_left(), color=RED, buff=0.1, stroke_width=2),
            Arrow(s1_icon.get_right(), m2_icon.get_left(), color=RED, buff=0.1, stroke_width=2),
            Arrow(s2_icon.get_right(), m1_icon.get_left(), color=GREEN, buff=0.1, stroke_width=2),
            Arrow(s2_icon.get_right(), m2_icon.get_left(), color=GREEN, buff=0.1, stroke_width=2),
        )

        mix_label = Text("Sounds mix\nin the air!", font_size=16, color=GRAY).move_to(ORIGIN)
        self.play(FadeIn(arrows, lag_ratio=0.1), Write(mix_label))
        self.wait(2)

        self.play(FadeOut(VGroup(sources, mics, arrows, mix_label, party_title)))

        # ============================================================
        # PART 2: THE MATH — MIXING MODEL
        # ============================================================
        math_title = Text("The Mixing Model", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(math_title))

        # X = A * S
        eq_main = MathTex(r"\mathbf{X}", "=", r"\mathbf{A}", r"\cdot", r"\mathbf{S}", font_size=48)
        eq_main[0].set_color(ORANGE)   # X
        eq_main[2].set_color(YELLOW)   # A
        eq_main[4].set_color(GREEN)    # S
        eq_main.shift(UP * 0.5)
        self.play(Write(eq_main))

        # Labels
        labels = VGroup(
            Text("What we observe\n(mixed signals)", font_size=14, color=ORANGE).next_to(eq_main[0], DOWN, buff=0.4),
            Text("Unknown\nmixing matrix", font_size=14, color=YELLOW).next_to(eq_main[2], DOWN, buff=0.4),
            Text("Original sources\n(what we want!)", font_size=14, color=GREEN).next_to(eq_main[4], DOWN, buff=0.4),
        )
        self.play(FadeIn(labels, lag_ratio=0.1))
        self.wait(1)

        # Expanded form
        expanded = MathTex(
            r"\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}",
            "=",
            r"\begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}",
            r"\begin{bmatrix} s_1 \\ s_2 \end{bmatrix}",
            font_size=36
        ).shift(DOWN * 1.8)
        expanded[0].set_color(ORANGE)
        expanded[2].set_color(YELLOW)
        expanded[3].set_color(GREEN)

        self.play(Write(expanded))
        self.wait(2)

        self.play(FadeOut(VGroup(math_title, eq_main, labels, expanded)))

        # ============================================================
        # PART 3: THE GOAL — UNMIXING
        # ============================================================
        goal_title = Text("ICA Goal: Find the Unmixing Matrix", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(goal_title))

        # S = W * X
        eq_goal = MathTex(r"\mathbf{S}", "=", r"\mathbf{W}", r"\cdot", r"\mathbf{X}", font_size=48)
        eq_goal[0].set_color(GREEN)
        eq_goal[2].set_color(TEAL)
        eq_goal[4].set_color(ORANGE)
        eq_goal.shift(UP * 0.3)
        self.play(Write(eq_goal))

        goal_labels = VGroup(
            Text("Recovered\nsources", font_size=14, color=GREEN).next_to(eq_goal[0], DOWN, buff=0.4),
            Text("Unmixing matrix\n(W = A inverse)", font_size=14, color=TEAL).next_to(eq_goal[2], DOWN, buff=0.4),
            Text("Observed\nmixed signals", font_size=14, color=ORANGE).next_to(eq_goal[4], DOWN, buff=0.4),
        )
        self.play(FadeIn(goal_labels, lag_ratio=0.1))

        # Key relationship
        key_eq = MathTex(r"\mathbf{W} = \mathbf{A}^{-1}", font_size=36, color=TEAL).shift(DOWN * 2)
        self.play(Write(key_eq))
        self.wait(2)

        self.play(FadeOut(VGroup(goal_title, eq_goal, goal_labels, key_eq)))

        # ============================================================
        # PART 4: HOW? — INDEPENDENCE + NON-GAUSSIANITY
        # ============================================================
        how_title = Text("The Key Insight", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(how_title))

        insight = Text("Independent signals are NON-Gaussian.", font_size=24, color=YELLOW).shift(UP * 0.5)
        self.play(Write(insight))

        # Left: Mixed (Gaussian-looking cloud)
        np.random.seed(42)
        mixed_label = Text("Mixed (Gaussian)", font_size=18, color=RED).shift(LEFT * 3.5 + DOWN * 0.3)
        # Show a circular scatter plot
        n_pts = 80
        angles = np.random.uniform(0, 2 * np.pi, n_pts)
        radii = np.random.normal(0, 0.6, n_pts)
        mixed_dots = VGroup()
        for a, r in zip(angles, radii):
            x = r * np.cos(a)
            y = r * np.sin(a)
            d = Dot([x - 3.5, y - 1.5, 0], color=RED, radius=0.03)
            mixed_dots.add(d)

        self.play(Write(mixed_label), FadeIn(mixed_dots, lag_ratio=0.01))

        # Right: Separated (Non-Gaussian, uniform-like)
        sep_label = Text("Separated (Non-Gaussian)", font_size=18, color=GREEN).shift(RIGHT * 3.5 + DOWN * 0.3)
        # Show a square/uniform scatter plot
        sep_dots = VGroup()
        for i in range(n_pts):
            x = np.random.uniform(-0.8, 0.8)
            y = np.random.uniform(-0.8, 0.8)
            d = Dot([x + 3.5, y - 1.5, 0], color=GREEN, radius=0.03)
            sep_dots.add(d)

        self.play(Write(sep_label), FadeIn(sep_dots, lag_ratio=0.01))

        algo_text = Text("ICA rotates data until it looks LEAST Gaussian", font_size=18, color=GRAY).to_edge(DOWN)
        self.play(Write(algo_text))
        self.wait(2)

        self.play(FadeOut(VGroup(how_title, insight, mixed_label, mixed_dots, sep_label, sep_dots, algo_text)))

        # ============================================================
        # PART 5: VISUAL DEMO — SIGNAL SEPARATION
        # ============================================================
        demo_title = Text("Signal Separation Demo", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(demo_title))

        t = np.linspace(0, 3, 300)

        # Original sources
        s1 = np.sin(2 * np.pi * 3 * t)          # Pure sine
        s2 = np.sign(np.sin(2 * np.pi * 7 * t)) # Square wave

        # Mixing
        x1 = 0.7 * s1 + 0.3 * s2  # Mixed 1
        x2 = 0.4 * s1 + 0.6 * s2  # Mixed 2

        def make_signal_plot(data, color, label_text, y_pos):
            ax = Axes(
                x_range=[0, 3, 1], y_range=[-1.5, 1.5, 0.5],
                x_length=5, y_length=0.8,
                axis_config={"include_numbers": False, "stroke_width": 1}
            ).shift(y_pos)
            curve = ax.plot(
                lambda x_val: float(np.interp(x_val, t, data)),
                x_range=[0, 3, 0.01], color=color, stroke_width=1.5
            )
            label = Text(label_text, font_size=14, color=color).next_to(ax, LEFT, buff=0.1)
            return VGroup(ax, curve, label)

        # Show mixed signals
        mixed_section = Text("Mixed (X)", font_size=16, color=ORANGE).shift(LEFT * 3 + UP * 0.8)
        mix1 = make_signal_plot(x1, ORANGE, "x1", LEFT * 3 + UP * 0.2)
        mix2 = make_signal_plot(x2, PURPLE, "x2", LEFT * 3 + DOWN * 0.8)

        self.play(Write(mixed_section), FadeIn(VGroup(mix1, mix2)))

        # ICA arrow
        ica_arrow = Arrow(LEFT * 0.3, RIGHT * 0.3, color=TEAL, buff=0)
        ica_label = Text("ICA\n(W)", font_size=16, color=TEAL).next_to(ica_arrow, UP, buff=0.1)
        self.play(GrowArrow(ica_arrow), Write(ica_label))

        # Show recovered sources
        sep_section = Text("Recovered (S)", font_size=16, color=GREEN).shift(RIGHT * 3 + UP * 0.8)
        rec1 = make_signal_plot(s1, RED, "s1", RIGHT * 3 + UP * 0.2)
        rec2 = make_signal_plot(s2, GREEN, "s2", RIGHT * 3 + DOWN * 0.8)

        self.play(Write(sep_section), FadeIn(VGroup(rec1, rec2)))

        # EEG application note
        eeg_note = Text("In EEG: Separates brain signals from eye blinks, muscle noise, etc.",
                         font_size=18, color=YELLOW).to_edge(DOWN)
        self.play(Write(eeg_note))
        self.wait(3)
