from manim import *
import numpy as np

class EEGBiometrics(Scene):
    def construct(self):
        # ============================================================
        # PART 1: WHAT IS EEG-BASED BIOMETRICS?
        # ============================================================
        title = Text("EEG-Based Biometrics", font_size=44, color=YELLOW).to_edge(UP)
        subtitle = Text("Your Brain is Your Password", font_size=26, color=GRAY).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)

        # Show traditional biometrics vs EEG
        trad_title = Text("Traditional Biometrics", font_size=22, color=RED).shift(LEFT * 3.5 + UP * 1.5)
        trad_items = VGroup(
            Text("• Fingerprint", font_size=18),
            Text("• Face", font_size=18),
            Text("• Iris", font_size=18),
            Text("• Voice", font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(trad_title, DOWN, buff=0.2)

        problem = Text("Can be spoofed!", font_size=18, color=RED).next_to(trad_items, DOWN, buff=0.3)

        eeg_title = Text("EEG Biometrics", font_size=22, color=GREEN).shift(RIGHT * 3.5 + UP * 1.5)
        eeg_items = VGroup(
            Text("• Brainwave patterns", font_size=18),
            Text("• Unique to each person", font_size=18),
            Text("• Cannot be stolen", font_size=18),
            Text("• Liveness guaranteed", font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(eeg_title, DOWN, buff=0.2)

        advantage = Text("Cannot be faked!", font_size=18, color=GREEN).next_to(eeg_items, DOWN, buff=0.3)

        # Divider
        divider = Line(UP * 2, DOWN * 2, color=GRAY, stroke_width=1)

        self.play(
            Write(trad_title), FadeIn(trad_items, lag_ratio=0.1),
            Write(eeg_title), FadeIn(eeg_items, lag_ratio=0.1),
            Create(divider)
        )
        self.play(Write(problem), Write(advantage))
        self.wait(2)

        self.play(FadeOut(Group(*self.mobjects).remove(title)))

        # ============================================================
        # PART 2: EEG SIGNAL ACQUISITION
        # ============================================================
        part2 = Text("Step 1: Record Brainwaves", font_size=30, color=BLUE).next_to(title, DOWN, buff=0.3)
        self.play(Write(part2))

        # Headset icon (simplified circle + electrodes)
        head = Circle(radius=1.2, color=WHITE, stroke_width=2).shift(LEFT * 3.5 + DOWN * 0.5)
        # Electrode dots around the head
        electrode_positions = [
            UP * 1.2,              # Cz (top)
            UP * 0.8 + LEFT * 0.9, # C3
            UP * 0.8 + RIGHT * 0.9,# C4
            LEFT * 1.2,            # T7
            RIGHT * 1.2,           # T8
            DOWN * 0.4 + LEFT * 0.9,  # P3
            DOWN * 0.4 + RIGHT * 0.9, # P4
        ]
        electrodes = VGroup()
        e_labels = ["Cz", "C3", "C4", "T7", "T8", "P3", "P4"]
        for pos, lbl in zip(electrode_positions, e_labels):
            dot = Dot(head.get_center() + pos, color=GREEN, radius=0.08)
            label = Text(lbl, font_size=10, color=GREEN).next_to(dot, DOWN, buff=0.05)
            electrodes.add(VGroup(dot, label))

        head_label = Text("EEG Cap", font_size=18).next_to(head, DOWN, buff=0.3)
        self.play(Create(head), FadeIn(electrodes, lag_ratio=0.05), Write(head_label))

        # Show EEG signals coming from the head
        # Multiple channels of EEG
        signal_group = VGroup()
        channel_names = ["Cz", "C3", "C4", "P3"]
        colors = [BLUE, GREEN, YELLOW, RED]
        np.random.seed(42)

        for idx, (ch, col) in enumerate(zip(channel_names, colors)):
            # Create a simple axis for each channel
            y_offset = 1.0 - idx * 0.9
            ax = Axes(
                x_range=[0, 4, 1],
                y_range=[-1, 1, 0.5],
                x_length=4.5,
                y_length=0.7,
                axis_config={"include_numbers": False, "stroke_width": 1}
            ).shift(RIGHT * 2.5 + UP * y_offset)

            # Generate EEG-like signal
            t = np.linspace(0, 4, 200)
            # Mix of alpha, beta, theta waves
            signal = (
                0.4 * np.sin(2 * np.pi * 10 * t + idx) +   # Alpha
                0.2 * np.sin(2 * np.pi * 20 * t + idx*2) + # Beta
                0.3 * np.sin(2 * np.pi * 5 * t + idx*3) +  # Theta
                0.1 * np.random.randn(len(t))               # Noise
            )
            signal = np.clip(signal, -1, 1)

            curve = ax.plot_line_graph(t, signal, add_vertex_dots=False, line_color=col, stroke_width=1.5)
            ch_label = Text(ch, font_size=14, color=col).next_to(ax, LEFT, buff=0.1)
            signal_group.add(VGroup(ax, curve, ch_label))

        # Arrows from head to signals
        sig_arrow = Arrow(head.get_right(), signal_group.get_left(), color=WHITE, buff=0.2)
        self.play(GrowArrow(sig_arrow))
        self.play(FadeIn(signal_group, lag_ratio=0.1))
        self.wait(2)

        self.play(FadeOut(VGroup(head, electrodes, head_label, sig_arrow, part2)))

        # ============================================================
        # PART 3: UNIQUE BRAINWAVE FINGERPRINT
        # ============================================================
        part3 = Text("Step 2: Every Brain is Unique", font_size=30, color=PURPLE).next_to(title, DOWN, buff=0.3)
        self.play(ReplacementTransform(signal_group, VGroup()), Write(part3))

        # Show 3 different people's "brainwave signatures"
        people = ["Person A", "Person B", "Person C"]
        p_colors = [BLUE, GREEN, ORANGE]

        sig_comparison = VGroup()
        for idx, (person, col) in enumerate(zip(people, p_colors)):
            y_off = 1.0 - idx * 1.5
            ax = Axes(
                x_range=[0, 4, 1],
                y_range=[-1.2, 1.2, 0.5],
                x_length=8,
                y_length=1.2,
                axis_config={"include_numbers": False, "stroke_width": 1}
            ).shift(DOWN * 0.5 + UP * y_off)

            t = np.linspace(0, 4, 300)
            # Different frequency mixes per person
            if idx == 0:
                sig = 0.6*np.sin(2*np.pi*10*t) + 0.3*np.sin(2*np.pi*22*t) + 0.1*np.random.randn(len(t))
            elif idx == 1:
                sig = 0.3*np.sin(2*np.pi*8*t) + 0.5*np.sin(2*np.pi*15*t) + 0.1*np.random.randn(len(t))
            else:
                sig = 0.4*np.sin(2*np.pi*12*t) + 0.4*np.sin(2*np.pi*30*t) + 0.1*np.random.randn(len(t))

            sig = np.clip(sig, -1.2, 1.2)
            curve = ax.plot_line_graph(t, sig, add_vertex_dots=False, line_color=col, stroke_width=2)
            label = Text(person, font_size=18, color=col).next_to(ax, LEFT, buff=0.15)
            sig_comparison.add(VGroup(ax, curve, label))

        self.play(FadeIn(sig_comparison, lag_ratio=0.15))

        unique_text = Text("Different patterns = Different identities", font_size=20, color=YELLOW).to_edge(DOWN)
        self.play(Write(unique_text))
        self.wait(2)

        self.play(FadeOut(VGroup(sig_comparison, unique_text, part3)))

        # ============================================================
        # PART 4: THE PIPELINE
        # ============================================================
        part4 = Text("The Authentication Pipeline", font_size=30, color=GREEN).next_to(title, DOWN, buff=0.3)
        self.play(Write(part4))

        # Pipeline: EEG -> Preprocessing -> Feature Extraction -> Classifier -> Identity
        box_style = {"width": 2.2, "height": 1.2, "corner_radius": 0.15}
        stages = [
            ("EEG\nSignal", BLUE),
            ("Pre-\nprocessing", ORANGE),
            ("Feature\nExtraction", PURPLE),
            ("Classifier\n(DNN)", RED),
            ("Identity\nVerified", GREEN),
        ]

        boxes = VGroup()
        for text, color in stages:
            box = VGroup(
                RoundedRectangle(**box_style, color=color, fill_opacity=0.15),
                Text(text, font_size=16, color=color)
            )
            boxes.add(box)

        boxes.arrange(RIGHT, buff=0.4).shift(DOWN * 0.3)

        # Scale to fit
        if boxes.width > 13:
            boxes.scale(13 / boxes.width)

        self.play(FadeIn(boxes, lag_ratio=0.1))

        # Arrows between boxes
        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arr = Arrow(
                boxes[i].get_right(), boxes[i+1].get_left(),
                color=WHITE, buff=0.1, stroke_width=2
            )
            arrows.add(arr)

        self.play(FadeIn(arrows, lag_ratio=0.1))

        # Subtext for each stage
        subtexts = [
            "Record",
            "Filter &\nNormalize",
            "PSD, ERPs,\nCSP",
            "CNN / LSTM",
            "Accept /\nReject"
        ]
        sub_group = VGroup()
        for box, st in zip(boxes, subtexts):
            sub = Text(st, font_size=12, color=GRAY).next_to(box, DOWN, buff=0.2)
            sub_group.add(sub)

        self.play(FadeIn(sub_group, lag_ratio=0.05))

        # Final accuracy text
        accuracy = Text("Accuracy: Up to 99%+ with deep learning", font_size=20, color=YELLOW).to_edge(DOWN)
        self.play(Write(accuracy))
        self.wait(3)
