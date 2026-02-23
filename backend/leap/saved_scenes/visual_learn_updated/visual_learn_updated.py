# LEAP_VERTICAL
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# Force Vertical Canvas Configuration (9:16 Aspect Ratio)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

class VisualThinkingVoiceover(VoiceoverScene, MovingCameraScene):
    def construct(self):
        # 1. Setup Voiceover
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        # --- TITLE ---
        title = Text(
            "Why Visual Thinking\nMakes Learning Easier", 
            font_size=32, 
            weight=BOLD
        ).to_edge(UP, buff=0.8)
        
        with self.voiceover(text="Why does visual thinking make learning so much easier? Let's break it down.") as tracker:
            self.play(Write(title), run_time=tracker.duration)

        # --- SCENE 1: Text vs Visuals ---
        text_block = Text(
            "Text requires sequential\ndecoding. You must read\nsentences one by one to\nbuild a mental model.",
            font_size=24,
            t2c={"Text": RED, "sequential": YELLOW, "mental model": BLUE},
            line_spacing=1.2
        ).next_to(title, DOWN, buff=0.8)
        
        with self.voiceover(text="Text requires sequential decoding. You have to read words one by one just to build a mental picture.") as tracker:
            self.play(FadeIn(text_block, shift=UP), run_time=tracker.duration)

        # Visual equivalent (Network nodes)
        node_a = Circle(radius=0.4, color=RED, fill_opacity=0.6).move_to(ORIGIN)
        node_b = Circle(radius=0.4, color=YELLOW, fill_opacity=0.6).next_to(node_a, DOWN + LEFT, buff=0.5)
        node_c = Circle(radius=0.4, color=BLUE, fill_opacity=0.6).next_to(node_a, DOWN + RIGHT, buff=0.5)
        
        nodes = VGroup(node_a, node_b, node_c)
        lines = VGroup(
            Line(node_a.get_center(), node_b.get_center()).set_z_index(-1),
            Line(node_a.get_center(), node_c.get_center()).set_z_index(-1),
            Line(node_b.get_center(), node_c.get_center()).set_z_index(-1)
        )
        visual_diagram = VGroup(lines, nodes).next_to(title, DOWN, buff=1.2)

        with self.voiceover(text="But with visuals, your brain processes the relationships immediately.") as tracker:
            self.play(ReplacementTransform(text_block, visual_diagram), run_time=tracker.duration)
        
        concept_label = Text(
            "Instant Recognition", 
            font_size=28, 
            color=GREEN
        ).next_to(visual_diagram, DOWN, buff=0.6)
        
        with self.voiceover(text="This leads to instant recognition of the core concept.") as tracker:
            self.play(FadeIn(concept_label, shift=UP), run_time=tracker.duration)

        # --- SCENE 2: Processing Speed ---
        with self.voiceover(text="Now let's talk about speed.") as tracker:
            self.play(self.camera.frame.animate.shift(DOWN * 7), run_time=tracker.duration)
        
        speed_title = Text("Processing Speed", font_size=36, weight=BOLD).next_to(concept_label, DOWN, buff=3.5)
        self.play(FadeIn(speed_title, shift=DOWN))

        # Speed Comparison
        text_label = Text("Reading Text:", font_size=24).next_to(speed_title, DOWN, buff=1.0).to_edge(LEFT, buff=0.5)
        text_bg = Rectangle(width=3.5, height=0.4, color=GRAY).next_to(text_label, DOWN, buff=0.3).align_to(text_label, LEFT)
        text_fill = Rectangle(width=0.01, height=0.4, color=RED, fill_opacity=1).align_to(text_bg, LEFT).align_to(text_bg, UP)

        visual_label = Text("Seeing Visuals:", font_size=24).next_to(text_bg, DOWN, buff=0.8).align_to(text_label, LEFT)
        visual_bg = Rectangle(width=3.5, height=0.4, color=GRAY).next_to(visual_label, DOWN, buff=0.3).align_to(visual_label, LEFT)
        visual_fill = Rectangle(width=3.5, height=0.4, color=GREEN, fill_opacity=1).align_to(visual_bg, LEFT).align_to(visual_bg, UP)

        self.play(
            Write(text_label), FadeIn(text_bg),
            Write(visual_label), FadeIn(visual_bg)
        )
        self.add(text_fill)
        
        with self.voiceover(text="While reading text takes time and effort to absorb...") as tracker:
            self.play(text_fill.animate.stretch_to_fit_width(3.5, about_edge=LEFT), run_time=tracker.duration, rate_func=linear)
        
        with self.voiceover(text="Visuals are processed almost instantaneously.") as tracker:
            self.play(FadeIn(visual_fill, run_time=0.15))
            self.wait(max(0, tracker.duration - 0.15))
        
        speed_fact = Text("60,000x Faster!", font_size=28, color=YELLOW, weight=BOLD).next_to(visual_bg, DOWN, buff=0.4).align_to(visual_bg, LEFT)
        with self.voiceover(text="In fact, the brain processes images up to sixty thousand times faster than text.") as tracker:
            self.play(Write(speed_fact), run_time=tracker.duration)

        # --- SCENE 3: Retention ---
        # Clear screen to make space
        with self.voiceover(text="Finally, how well do we remember it?") as tracker:
            self.play(
                FadeOut(speed_title), FadeOut(text_label), FadeOut(text_bg), FadeOut(text_fill),
                FadeOut(visual_label), FadeOut(visual_bg), FadeOut(visual_fill), FadeOut(speed_fact),
                run_time=tracker.duration
            )

        retention_title = Text("Memory Retention", font_size=36, weight=BOLD).move_to(self.camera.frame.get_center() + UP*2.5)
        self.play(Write(retention_title))

        chart = BarChart(
            values=[20, 80],
            bar_names=["Reading", "Seeing"],
            y_range=[0, 100, 20],
            y_length=3.5,
            x_length=3.0,
            bar_colors=[BLUE, GREEN],
            bar_fill_opacity=0.8
        ).next_to(retention_title, DOWN, buff=0.8)

        with self.voiceover(text="People typically remember only 20 percent of what they read...") as tracker:
            self.play(DrawBorderThenFill(chart), run_time=tracker.duration)

        pct_read = Text("20%", font_size=20).next_to(chart.bars[0], UP, buff=0.2)
        pct_see = Text("80%", font_size=20).next_to(chart.bars[1], UP, buff=0.2)

        with self.voiceover(text="...but they retain up to 80 percent of what they see and do.") as tracker:
            self.play(FadeIn(pct_read, shift=UP), FadeIn(pct_see, shift=UP), run_time=tracker.duration)

        conclusion = Text("See it. Learn it.", font_size=36, color=YELLOW, weight=BOLD).next_to(chart, DOWN, buff=1.0)
        with self.voiceover(text="So, don't just read it. See it, and learn it faster.") as tracker:
            self.play(Write(conclusion), run_time=tracker.duration)

        self.play(FadeOut(Group(*self.mobjects)))