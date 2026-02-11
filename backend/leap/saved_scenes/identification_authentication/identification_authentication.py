from manim import *
import numpy as np

class EEGIdentificationVsAuthentication(Scene):
    def construct(self):
        # ============================================================
        # TITLE
        # ============================================================
        title = Text("EEG Biometrics", font_size=44, color=YELLOW).to_edge(UP)
        subtitle = Text("Identification vs Authentication", font_size=28, color=GRAY).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)

        # Core question
        q1 = Text('"Who are you?"', font_size=30, color=BLUE).shift(LEFT * 3 + UP * 1)
        q2 = Text('"Are you who you claim to be?"', font_size=26, color=GREEN).shift(RIGHT * 2.5 + UP * 1)

        l1 = Text("= Identification (1 : N)", font_size=22, color=BLUE).next_to(q1, DOWN, buff=0.2)
        l2 = Text("= Authentication (1 : 1)", font_size=22, color=GREEN).next_to(q2, DOWN, buff=0.2)

        div = Line(UP * 1.5, DOWN * 2.5, color=GRAY, stroke_width=1)

        self.play(Write(q1), Write(l1))
        self.play(Write(q2), Write(l2))
        self.play(Create(div))
        self.wait(2)

        self.play(FadeOut(VGroup(q1, q2, l1, l2, div, subtitle)))

        # ============================================================
        # PART 1: IDENTIFICATION (1:N)
        # ============================================================
        part1 = Text("Identification (1 : N)", font_size=34, color=BLUE).next_to(title, DOWN, buff=0.3)
        self.play(Write(part1))

        scenario = Text("Unknown person walks up to a secure door.", font_size=20, color=GRAY).next_to(part1, DOWN, buff=0.3)
        self.play(Write(scenario))

        # Unknown person's EEG on the left
        unknown_box = VGroup(
            RoundedRectangle(width=2.5, height=1.5, corner_radius=0.15, color=BLUE, fill_opacity=0.15),
            Text("?", font_size=48, color=BLUE),
        ).shift(LEFT * 4.5 + DOWN * 1)
        unknown_label = Text("Unknown\nEEG Signal", font_size=16, color=BLUE).next_to(unknown_box, DOWN, buff=0.15)

        self.play(FadeIn(unknown_box), Write(unknown_label))

        # Database of N enrolled users on the right
        db_title = Text("Enrolled Database (N users)", font_size=18, color=WHITE).shift(RIGHT * 2.5 + DOWN * 0.2)

        db_users = VGroup()
        user_names = ["Alice", "Bob", "Carol", "Dave", "Eve"]
        user_colors = [RED, ORANGE, YELLOW, PURPLE, TEAL]
        for i, (name, col) in enumerate(zip(user_names, user_colors)):
            row = VGroup(
                Dot(color=col, radius=0.1),
                Text(name, font_size=16, color=col),
            ).arrange(RIGHT, buff=0.15)
            db_users.add(row)

        db_users.arrange(DOWN, buff=0.15).next_to(db_title, DOWN, buff=0.2)

        db_frame = SurroundingRectangle(VGroup(db_title, db_users), color=GRAY, buff=0.2)
        self.play(FadeIn(db_frame), Write(db_title), FadeIn(db_users, lag_ratio=0.05))

        # Arrow: Unknown -> Compare against ALL
        compare_arrow = Arrow(unknown_box.get_right(), db_frame.get_left(), color=BLUE, buff=0.15)
        compare_text = Text("Compare\nagainst all N", font_size=14, color=BLUE).next_to(compare_arrow, UP, buff=0.1)
        self.play(GrowArrow(compare_arrow), Write(compare_text))

        # Highlight match: Carol
        match_highlight = SurroundingRectangle(db_users[2], color=GREEN, buff=0.05)
        match_text = Text("Match Found! You are Carol.", font_size=20, color=GREEN).shift(DOWN * 2.8)

        self.play(Create(match_highlight), Write(match_text))
        self.wait(1)

        # Key property
        prop1 = Text("Key: System searches the entire database. No claim needed.", font_size=16, color=YELLOW).to_edge(DOWN)
        self.play(Write(prop1))
        self.wait(2)

        # Clear
        self.play(FadeOut(VGroup(
            part1, scenario, unknown_box, unknown_label,
            db_title, db_users, db_frame, compare_arrow, compare_text,
            match_highlight, match_text, prop1
        )))

        # ============================================================
        # PART 2: AUTHENTICATION (1:1)
        # ============================================================
        part2 = Text("Authentication (1 : 1)", font_size=34, color=GREEN).next_to(title, DOWN, buff=0.3)
        self.play(Write(part2))

        scenario2 = Text('Person claims "I am Carol" and provides EEG.', font_size=20, color=GRAY).next_to(part2, DOWN, buff=0.3)
        self.play(Write(scenario2))

        # Claimed identity on the left
        claim_box = VGroup(
            RoundedRectangle(width=2.5, height=1.5, corner_radius=0.15, color=GREEN, fill_opacity=0.15),
            Text("Carol?", font_size=36, color=GREEN),
        ).shift(LEFT * 4.5 + DOWN * 1)
        claim_label = Text('Claims to be\n"Carol"', font_size=16, color=GREEN).next_to(claim_box, DOWN, buff=0.15)

        self.play(FadeIn(claim_box), Write(claim_label))

        # Single stored template on the right
        template_title = Text("Carol's Stored Template", font_size=18, color=YELLOW).shift(RIGHT * 3 + DOWN * 0.2)

        # Show stored EEG as a simple waveform
        np.random.seed(10)
        t = np.linspace(0, 3, 200)
        sig = 0.5 * np.sin(2 * np.pi * 10 * t) + 0.3 * np.sin(2 * np.pi * 22 * t)

        template_ax = Axes(
            x_range=[0, 3, 1], y_range=[-1, 1, 0.5],
            x_length=4, y_length=1.5,
            axis_config={"include_numbers": False, "stroke_width": 1}
        ).next_to(template_title, DOWN, buff=0.2)

        template_curve = template_ax.plot(
            lambda x: 0.5 * np.sin(2 * np.pi * 10 * x) + 0.3 * np.sin(2 * np.pi * 22 * x),
            x_range=[0, 3, 0.01], color=YELLOW, stroke_width=2
        )
        template_frame = SurroundingRectangle(VGroup(template_title, template_ax), color=YELLOW, buff=0.2)

        self.play(FadeIn(template_frame), Write(template_title), Create(template_ax), Create(template_curve))

        # Arrow: Claim -> Single template
        auth_arrow = Arrow(claim_box.get_right(), template_frame.get_left(), color=GREEN, buff=0.15)
        auth_text = Text("Compare\n1 vs 1", font_size=14, color=GREEN).next_to(auth_arrow, UP, buff=0.1)
        self.play(GrowArrow(auth_arrow), Write(auth_text))

        # Result
        result_accept = Text("Match! Access Granted", font_size=22, color=GREEN).shift(DOWN * 2.8)
        self.play(Write(result_accept))

        prop2 = Text("Key: System only checks ONE stored template. Claim required.", font_size=16, color=YELLOW).to_edge(DOWN)
        self.play(Write(prop2))
        self.wait(2)

        # Clear
        self.play(FadeOut(VGroup(
            part2, scenario2, claim_box, claim_label,
            template_title, template_ax, template_curve, template_frame,
            auth_arrow, auth_text, result_accept, prop2
        )))

        # ============================================================
        # PART 3: SUMMARY TABLE
        # ============================================================
        summary_title = Text("Summary", font_size=34, color=YELLOW).next_to(title, DOWN, buff=0.3)
        self.play(Write(summary_title))

        # Build table manually with fixed positions
        col_x = [-4.5, -1.0, 3.0]

        header_items = [
            Text("", font_size=18),
            Text("Identification", font_size=20, color=BLUE),
            Text("Authentication", font_size=20, color=GREEN),
        ]
        for h, x in zip(header_items, col_x):
            h.move_to([x, 1.2, 0])

        headers = VGroup(*header_items)

        rows_data = [
            ("Question", '"Who are you?"', '"Are you Carol?"'),
            ("Comparison", "1 : N", "1 : 1"),
            ("Claim", "Not needed", "Required"),
            ("Speed", "Slower (search all)", "Faster (check one)"),
            ("Use Case", "Surveillance", "Login / Access"),
        ]

        table_rows = VGroup()
        for i, (label, id_val, auth_val) in enumerate(rows_data):
            y = 0.5 - i * 0.5
            items = [
                Text(label, font_size=16, color=GRAY).move_to([col_x[0], y, 0]),
                Text(id_val, font_size=16, color=BLUE).move_to([col_x[1], y, 0]),
                Text(auth_val, font_size=16, color=GREEN).move_to([col_x[2], y, 0]),
            ]
            table_rows.add(VGroup(*items))

        h_line = Line(
            LEFT * 6 + UP * 0.9,
            RIGHT * 6 + UP * 0.9,
            color=GRAY, stroke_width=1
        )

        self.play(FadeIn(headers), Create(h_line))
        self.play(FadeIn(table_rows, lag_ratio=0.08))
        self.wait(3)
