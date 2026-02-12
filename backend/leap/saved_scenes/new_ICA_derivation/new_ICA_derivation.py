from manim import *
import numpy as np

class ICAAlgorithmDeepDive(Scene):
    def construct(self):
        # ============================================================
        # PART 1: REVERSE CENTRAL LIMIT THEOREM
        # ============================================================
        title = Text("ICA: The Algorithm", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        clt_title = Text("Core Intuition: Reverse CLT", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(clt_title))

        # CLT: Adding independent signals -> Gaussian
        clt_text = Text("Central Limit Theorem (The Mixer)", font_size=20, color=RED).shift(UP * 0.8)
        clt_desc = Text("Adding independent signals -> Gaussian", font_size=16, color=GRAY).next_to(clt_text, DOWN, buff=0.1)
        self.play(Write(clt_text), Write(clt_desc))

        # Show: Spiky + Flat = Gaussian
        np.random.seed(42)
        n = 200

        # Spiky distribution (Laplace-like)
        spiky_ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 0.5],
                        x_length=3, y_length=1.2,
                        axis_config={"include_numbers": False, "stroke_width": 1}).shift(LEFT * 4.5 + DOWN * 1)
        spiky_curve = spiky_ax.plot(lambda x: 0.8 * np.exp(-2 * abs(x)),
                                     x_range=[-3, 3, 0.02], color=RED, stroke_width=2)
        spiky_label = Text("Spiky\n(Speech)", font_size=12, color=RED).next_to(spiky_ax, DOWN, buff=0.1)

        # Plus sign
        plus = Text("+", font_size=30, color=WHITE).shift(LEFT * 2.2 + DOWN * 1)

        # Flat distribution (Uniform-like)
        flat_ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 0.5],
                       x_length=3, y_length=1.2,
                       axis_config={"include_numbers": False, "stroke_width": 1}).shift(DOWN * 1)
        flat_curve = flat_ax.plot(
            lambda x: 0.5 if abs(x) < 1.5 else 0.0,
            x_range=[-3, 3, 0.02], color=ORANGE, stroke_width=2, discontinuities=[-1.5, 1.5]
        )
        flat_label = Text("Flat\n(Image)", font_size=12, color=ORANGE).next_to(flat_ax, DOWN, buff=0.1)

        # Equals
        equals = Text("=", font_size=30, color=WHITE).shift(RIGHT * 2.2 + DOWN * 1)

        # Gaussian result
        gauss_ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 0.5],
                        x_length=3, y_length=1.2,
                        axis_config={"include_numbers": False, "stroke_width": 1}).shift(RIGHT * 4.5 + DOWN * 1)
        gauss_curve = gauss_ax.plot(lambda x: np.exp(-x**2 / 2),
                                     x_range=[-3, 3, 0.02], color=YELLOW, stroke_width=2)
        gauss_label = Text("Gaussian\n(Mixed)", font_size=12, color=YELLOW).next_to(gauss_ax, DOWN, buff=0.1)

        self.play(
            FadeIn(VGroup(spiky_ax, spiky_curve, spiky_label)),
            Write(plus),
            FadeIn(VGroup(flat_ax, flat_curve, flat_label)),
            Write(equals),
            FadeIn(VGroup(gauss_ax, gauss_curve, gauss_label)),
        )
        self.wait(1)

        # ICA reversal
        ica_text = Text("ICA (The Un-mixer): Find signals that are LEAST Gaussian!", font_size=18, color=GREEN).to_edge(DOWN)
        self.play(Write(ica_text))
        self.wait(2)

        self.play(FadeOut(VGroup(
            clt_title, clt_text, clt_desc, ica_text,
            spiky_ax, spiky_curve, spiky_label, plus,
            flat_ax, flat_curve, flat_label, equals,
            gauss_ax, gauss_curve, gauss_label
        )))

        # ============================================================
        # PART 2: STEP 1 — CENTERING
        # ============================================================
        step1_title = Text("Step 1: Centering", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(step1_title))

        center_eq = MathTex(r"x' = x - \text{mean}(x)", font_size=40, color=WHITE).shift(UP * 0.5)
        self.play(Write(center_eq))

        center_desc = Text("Remove the DC offset. Focus on variations only.", font_size=18, color=GRAY).next_to(center_eq, DOWN, buff=0.3)
        self.play(Write(center_desc))

        # Visual: Scatter before and after centering
        np.random.seed(7)
        pts_raw = np.random.randn(40, 2) * 0.6 + np.array([2, 1.5])  # Off-center

        before_label = Text("Before", font_size=16, color=RED).shift(LEFT * 3 + DOWN * 0.5)
        before_dots = VGroup()
        for p in pts_raw:
            before_dots.add(Dot([p[0] - 5, p[1] - 2.5, 0], color=RED, radius=0.04))

        # After centering
        pts_centered = pts_raw - pts_raw.mean(axis=0)
        after_label = Text("After", font_size=16, color=GREEN).shift(RIGHT * 3 + DOWN * 0.5)
        after_dots = VGroup()
        for p in pts_centered:
            after_dots.add(Dot([p[0] + 3, p[1] - 1.5, 0], color=GREEN, radius=0.04))

        # Origin cross for after
        origin_h = Line(LEFT * 0.3 + DOWN * 1.5 + RIGHT * 3, RIGHT * 0.3 + DOWN * 1.5 + RIGHT * 3, color=WHITE, stroke_width=1)
        origin_v = Line(UP * 0.3 + DOWN * 1.5 + RIGHT * 3, DOWN * 0.3 + DOWN * 1.5 + RIGHT * 3, color=WHITE, stroke_width=1)

        arrow_center = Arrow(LEFT * 1.5 + DOWN * 1.5, RIGHT * 1.5 + DOWN * 1.5, color=YELLOW, buff=0)
        arrow_text = Text("Center", font_size=14, color=YELLOW).next_to(arrow_center, UP, buff=0.05)

        self.play(Write(before_label), FadeIn(before_dots))
        self.play(GrowArrow(arrow_center), Write(arrow_text))
        self.play(Write(after_label), FadeIn(after_dots), Create(origin_h), Create(origin_v))
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            step1_title, center_eq, center_desc,
            before_label, before_dots, after_label, after_dots,
            origin_h, origin_v, arrow_center, arrow_text
        )))

        # ============================================================
        # PART 3: STEP 2 — WHITENING
        # ============================================================
        step2_title = Text("Step 2: Whitening (Sphering)", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(step2_title))

        whiten_desc = Text("Make data uncorrelated with unit variance.", font_size=18, color=GRAY).next_to(step2_title, DOWN, buff=0.2)
        self.play(Write(whiten_desc))

        # Ellipse -> Circle visualization
        # Before: Tilted ellipse (correlated data)
        np.random.seed(15)
        n_pts = 60
        # Generate correlated data
        cov = np.array([[2, 1.2], [1.2, 1]])
        L = np.linalg.cholesky(cov)
        raw = np.random.randn(n_pts, 2) @ L.T

        ell_dots = VGroup()
        for p in raw:
            ell_dots.add(Dot([p[0] * 0.5 - 3.5, p[1] * 0.5 - 0.8, 0], color=RED, radius=0.04))

        ell_label = Text("Correlated\n(Ellipse)", font_size=14, color=RED).shift(LEFT * 3.5 + DOWN * 2.5)

        # Ellipse outline
        ellipse = Ellipse(width=3.5, height=1.5, color=RED, stroke_width=1.5).rotate(0.45).shift(LEFT * 3.5 + DOWN * 0.8)

        self.play(FadeIn(ell_dots), Create(ellipse), Write(ell_label))

        # Arrow
        whiten_arrow = Arrow(LEFT * 1.2 + DOWN * 0.8, RIGHT * 1.2 + DOWN * 0.8, color=YELLOW, buff=0)
        whiten_text = Text("Whiten\n(PCA)", font_size=14, color=YELLOW).next_to(whiten_arrow, UP, buff=0.05)
        self.play(GrowArrow(whiten_arrow), Write(whiten_text))

        # After: Perfect circle (whitened data)
        # Whiten: Z = D^-1/2 * V^T * X
        whitened = raw @ np.linalg.inv(L.T)  # Simple whitening
        circ_dots = VGroup()
        for p in whitened:
            circ_dots.add(Dot([p[0] * 0.5 + 3.5, p[1] * 0.5 - 0.8, 0], color=GREEN, radius=0.04))

        circ_label = Text("Uncorrelated\n(Circle)", font_size=14, color=GREEN).shift(RIGHT * 3.5 + DOWN * 2.5)
        circle = Circle(radius=1.2, color=GREEN, stroke_width=1.5).shift(RIGHT * 3.5 + DOWN * 0.8)

        self.play(FadeIn(circ_dots), Create(circle), Write(circ_label))

        why_text = Text("Now A is just a rotation matrix! Only need to find the angle.", font_size=16, color=YELLOW).to_edge(DOWN)
        self.play(Write(why_text))
        self.wait(2)

        self.play(FadeOut(VGroup(
            step2_title, whiten_desc,
            ell_dots, ellipse, ell_label,
            whiten_arrow, whiten_text,
            circ_dots, circle, circ_label, why_text
        )))

        # ============================================================
        # PART 4: STEP 3 — KURTOSIS
        # ============================================================
        step3_title = Text("Step 3: Maximize Non-Gaussianity", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(step3_title))

        kurt_title = Text("The Metric: Kurtosis", font_size=22, color=YELLOW).next_to(step3_title, DOWN, buff=0.2)
        self.play(Write(kurt_title))

        # Kurtosis equation
        kurt_eq = MathTex(r"\text{Kurt}(x) = E[x^4] - 3", font_size=36).shift(UP * 0.2)
        self.play(Write(kurt_eq))

        # Three distribution types
        kurt_types = VGroup(
            Text("Gaussian: Kurt = 0", font_size=16, color=GRAY),
            Text("Super-Gaussian (Speech): Kurt > 0  [Spiky]", font_size=16, color=RED),
            Text("Sub-Gaussian (Images): Kurt < 0  [Flat]", font_size=16, color=ORANGE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).shift(DOWN * 0.7)
        self.play(FadeIn(kurt_types, lag_ratio=0.1))

        # Visual: Show the three shapes side by side
        shapes_group = VGroup()
        shape_data = [
            ("Sub-Gaussian\nKurt < 0", ORANGE, lambda x: 0.5 if abs(x) < 1.5 else 0.0),
            ("Gaussian\nKurt = 0", GRAY, lambda x: 0.8 * np.exp(-x**2 / 2)),
            ("Super-Gaussian\nKurt > 0", RED, lambda x: 0.9 * np.exp(-2 * abs(x))),
        ]

        for i, (lbl, col, func) in enumerate(shape_data):
            ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 0.5],
                      x_length=3, y_length=1,
                      axis_config={"include_numbers": False, "stroke_width": 1}
                      ).shift(LEFT * 4 + RIGHT * i * 4 + DOWN * 2.5)
            if "Sub" in lbl:
                curve = ax.plot(func, x_range=[-3, 3, 0.02], color=col, stroke_width=2, discontinuities=[-1.5, 1.5])
            else:
                curve = ax.plot(func, x_range=[-3, 3, 0.02], color=col, stroke_width=2)
            label = Text(lbl, font_size=11, color=col).next_to(ax, DOWN, buff=0.08)
            shapes_group.add(VGroup(ax, curve, label))

        self.play(FadeIn(shapes_group, lag_ratio=0.1))
        self.wait(2)

        self.play(FadeOut(VGroup(step3_title, kurt_title, kurt_eq, kurt_types, shapes_group)))

        # ============================================================
        # PART 5: THE ROTATION ALGORITHM
        # ============================================================
        algo_title = Text("The Rotation Algorithm", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.2)
        self.play(Write(algo_title))

        # Show whitened data as a circle of dots
        np.random.seed(99)
        # Generate 2 independent uniform sources
        s1 = np.random.uniform(-1, 1, 80)
        s2 = np.random.uniform(-1, 1, 80)
        S = np.vstack([s1, s2])

        # Mix with a rotation
        theta_true = 0.7  # True mixing angle
        A = np.array([[np.cos(theta_true), -np.sin(theta_true)],
                       [np.sin(theta_true), np.cos(theta_true)]])
        X = A @ S  # Mixed (but already whitened since sources are uniform)

        data_dots = VGroup()
        for i in range(80):
            data_dots.add(Dot([X[0, i] * 1.5, X[1, i] * 1.5 - 0.8, 0], color=BLUE_C, radius=0.04))

        self.play(FadeIn(data_dots))

        # Show rotation line
        angle_tracker = ValueTracker(0)
        
        rot_line = always_redraw(lambda: Line(
            ORIGIN + DOWN * 0.8,
            np.array([2 * np.cos(angle_tracker.get_value()), 2 * np.sin(angle_tracker.get_value()), 0]) + DOWN * 0.8,
            color=YELLOW, stroke_width=3
        ))

        angle_label = always_redraw(lambda: Text(
            f"angle = {angle_tracker.get_value():.2f} rad",
            font_size=16, color=YELLOW
        ).shift(RIGHT * 4.5 + UP * 0.5))

        self.play(Create(rot_line), Write(angle_label))

        # Step labels
        steps_text = VGroup(
            Text("1. Pick random angle", font_size=14, color=WHITE),
            Text("2. Project data onto axis", font_size=14, color=WHITE),
            Text("3. Measure Kurtosis", font_size=14, color=WHITE),
            Text("4. Rotate to maximize |Kurt|", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).shift(RIGHT * 4 + DOWN * 0.5)
        self.play(FadeIn(steps_text, lag_ratio=0.1))

        # Animate rotation: sweep from 0 to true angle
        # Show kurtosis changing
        kurt_display = always_redraw(lambda: Text(
            f"|Kurt| = {abs(self._compute_kurt(X, angle_tracker.get_value())):.2f}",
            font_size=18, color=GREEN
        ).shift(RIGHT * 4 + DOWN * 2))

        self.add(kurt_display)

        # Animate: random start -> sweep to find max
        self.play(angle_tracker.animate.set_value(0.3), run_time=1)
        self.play(angle_tracker.animate.set_value(theta_true), run_time=2)

        # Found it!
        found = Text("Maximum Non-Gaussianity found!", font_size=20, color=GREEN).to_edge(DOWN)
        self.play(Write(found))
        self.wait(2)

        # Final: show recovered axes
        line2 = Line(
            ORIGIN + DOWN * 0.8,
            np.array([2 * np.cos(theta_true + np.pi/2), 2 * np.sin(theta_true + np.pi/2), 0]) + DOWN * 0.8,
            color=RED, stroke_width=3
        )
        ic_label = Text("IC 1", font_size=14, color=YELLOW).next_to(rot_line, UP, buff=0.05)
        ic2_label = Text("IC 2", font_size=14, color=RED).next_to(line2.get_end(), RIGHT, buff=0.05)

        self.play(Create(line2), Write(ic_label), Write(ic2_label))

        final_text = Text("These axes are the Independent Components!", font_size=18, color=YELLOW).to_edge(DOWN)
        self.play(ReplacementTransform(found, final_text))
        self.wait(3)

    def _compute_kurt(self, X, angle):
        """Compute kurtosis of data projected onto angle."""
        w = np.array([np.cos(angle), np.sin(angle)])
        proj = w @ X
        proj = proj - proj.mean()
        if proj.std() > 0:
            proj = proj / proj.std()
        return float(np.mean(proj**4) - 3)
