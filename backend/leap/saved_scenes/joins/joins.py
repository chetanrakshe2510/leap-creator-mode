# LEAP_VERTICAL
from manim import *
import numpy as np

# Force native vertical resolution for YouTube Shorts (9:16)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 14.22 * (1080 / 1920)


class JoinVisualization(Scene):
    def construct(self):
        self.camera.background_color = "#0D1117"
        B, G, Y, R = "#4A90D9", "#2ECC71", "#F1C40F", "#E74C3C"
        self.scene_setup_and_inner(B, G, Y, R)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
        self.scene_left_join(B, G, Y, R)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
        self.scene_right_join(B, G, Y, R)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

    # ── helpers (scaled for 14.22-tall vertical frame) ──
    def c(self, txt, w, h, col, op=0.8, fs=24):
        r = Rectangle(width=w, height=h, fill_color=col, fill_opacity=op,
                      stroke_color=WHITE, stroke_width=1.5)
        t = Text(str(txt), font_size=fs, color=WHITE).move_to(r)
        return VGroup(r, t)

    def make_row(self, vals, ws, col, h=0.7, op=0.5, fs=22):
        return VGroup(*[self.c(v, w, h, col, op, fs) for v, w in zip(vals, ws)]).arrange(RIGHT, buff=0)

    def mrow(self, vals, ws, cols, h=0.7, op=0.5, fs=22):
        return VGroup(*[self.c(v, w, h, c, op, fs) for v, w, c in zip(vals, ws, cols)]).arrange(RIGHT, buff=0)

    def tbl(self, hdr, data, ws, col, h=0.7):
        header = self.make_row(hdr, ws, col, h, 0.9, 26)
        rows = [self.make_row(r, ws, col, h) for r in data]
        t = VGroup(header, *rows).arrange(DOWN, buff=0)
        return t, header, rows

    def note(self, label, body, accent, width=6.5):
        lbl = Text(label, font_size=24, weight=BOLD, color=accent)
        msg = Text(body, font_size=20, color=WHITE, line_spacing=0.8)
        msg.set(width=min(msg.width, width - 0.6))
        ct = VGroup(lbl, msg).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        bx = SurroundingRectangle(ct, color=accent, buff=0.25,
                                  fill_color="#1A1A2E", fill_opacity=0.92,
                                  stroke_width=1.5, corner_radius=0.15)
        return VGroup(bx, ct)

    def build_tables(self, B, G):
        ws_a, ws_b = [1.0, 1.8], [1.0, 1.5]
        tA, hA, dA = self.tbl(["ID", "Name"],
                              [["1", "Alice"], ["2", "Bob"], ["3", "Charlie"]], ws_a, B, h=0.7)
        tB, hB, dB = self.tbl(["ID", "Dept"],
                              [["2", "HR"], ["3", "IT"], ["4", "Sales"]], ws_b, G, h=0.7)
        la = Text("Employees", font_size=22, color="#7FB3E0", weight=BOLD)
        lb = Text("Departments", font_size=22, color="#7DCEA0", weight=BOLD)
        ga = VGroup(la, tA).arrange(DOWN, buff=0.2)
        gb = VGroup(lb, tB).arrange(DOWN, buff=0.2)
        return ga, gb, tA, tB, hA, hB, dA, dB

    # ── SCENE 1+2: Setup → Inner Join ──
    def scene_setup_and_inner(self, B, G, Y, R):
        title = Text("DATA JOINS\nVISUALIZED", font_size=48, weight=BOLD, line_spacing=0.7)
        title.to_edge(UP, buff=1.0)
        self.play(FadeIn(title, shift=DOWN * 0.2))
        self.wait(0.8)

        ga, gb, tA, tB, hA, hB, dA, dB = self.build_tables(B, G)
        tables = VGroup(ga, gb).arrange(RIGHT, buff=0.5)
        tables.next_to(title, DOWN, buff=1.5)
        self.play(FadeIn(ga, shift=RIGHT * 0.3), FadeIn(gb, shift=LEFT * 0.3), run_time=1.2)
        self.wait(1)

        # Highlight shared ID columns
        idA = VGroup(hA[0], *[r[0] for r in dA])
        idB = VGroup(hB[0], *[r[0] for r in dB])
        gA = SurroundingRectangle(idA, color=Y, buff=0.06, stroke_width=3)
        gB = SurroundingRectangle(idB, color=Y, buff=0.06, stroke_width=3)
        self.play(Create(gA), Create(gB), run_time=0.7)

        n1 = self.note("\U0001f4cc Setup:", "To join tables, we first locate\nthe shared ID column.", Y)
        n1.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(n1, shift=UP * 0.2), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(n1, shift=DOWN * 0.2), FadeOut(gA), FadeOut(gB), run_time=0.5)

        # ── Scan: connecting lines ──
        # ID 2 match
        l2 = Line(dA[1][0].get_right(), dB[0][0].get_left(), color=WHITE, stroke_width=2.5)
        self.play(Create(l2), run_time=0.5)
        self.play(l2.animate.set_color(G), run_time=0.3)
        # ID 3 match
        l3 = Line(dA[2][0].get_right(), dB[1][0].get_left(), color=WHITE, stroke_width=2.5)
        self.play(Create(l3), run_time=0.5)
        self.play(l3.animate.set_color(G), run_time=0.3)
        # ID 1 no match
        l1 = Line(dA[0][0].get_right(), dA[0][0].get_right() + RIGHT * 1.0,
                  color=WHITE, stroke_width=2.5)
        self.play(Create(l1), run_time=0.3)
        self.play(l1.animate.set_color(R), run_time=0.2)
        self.play(Uncreate(l1), run_time=0.3)
        # ID 4 no match
        l4 = Line(dB[2][0].get_left(), dB[2][0].get_left() + LEFT * 1.0,
                  color=WHITE, stroke_width=2.5)
        self.play(Create(l4), run_time=0.3)
        self.play(l4.animate.set_color(R), run_time=0.2)
        self.play(Uncreate(l4), run_time=0.3)
        self.wait(0.5)

        # "INNER JOIN" label
        ij = Text("INNER JOIN", font_size=40, weight=BOLD, color=Y)
        ij.next_to(tables, DOWN, buff=0.8)
        self.play(FadeIn(ij, scale=1.2), run_time=0.5)

        # Result table
        ws_r, cols_r = [1.0, 1.6, 1.6], [Y, B, G]
        r_hdr = self.mrow(["ID", "Name", "Dept"], ws_r, cols_r, 0.7, 0.9, 26)
        r1 = self.mrow(["2", "Bob", "HR"], ws_r, cols_r)
        r2 = self.mrow(["3", "Charlie", "IT"], ws_r, cols_r)
        result = VGroup(r_hdr, r1, r2).arrange(DOWN, buff=0)
        result.next_to(ij, DOWN, buff=1.0)

        self.play(FadeOut(l2), FadeOut(l3), run_time=0.3)
        bob_s = VGroup(dA[1].copy(), dB[0].copy())
        cha_s = VGroup(dA[2].copy(), dB[1].copy())
        self.play(FadeIn(r_hdr),
                  ReplacementTransform(bob_s, r1),
                  ReplacementTransform(cha_s, r2), run_time=1.5)

        # Dissolve unmatched
        self.play(dA[0].animate.set_opacity(0.3), dB[2].animate.set_opacity(0.3), run_time=0.4)
        self.play(FadeOut(dA[0], shift=DOWN * 0.3, scale=0.3),
                  FadeOut(dB[2], shift=DOWN * 0.3, scale=0.3), run_time=0.8)
        self.wait(0.5)

        n2 = self.note("\u26a0\ufe0f Warning:",
                       "Inner Joins act as a strict filter.\nUnmatched rows are permanently\ndropped.", R)
        n2.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(n2, shift=UP * 0.2), run_time=0.7)
        self.wait(3)
        self.play(FadeOut(n2, shift=DOWN * 0.2), run_time=0.5)

    # ── SCENE 3: Left Join ──
    def scene_left_join(self, B, G, Y, R):
        ga, gb, tA, tB, hA, hB, dA, dB = self.build_tables(B, G)
        tables = VGroup(ga, gb).arrange(RIGHT, buff=0.5)
        tables.move_to(UP * 4.0)
        self.play(FadeIn(ga, shift=RIGHT * 0.2), FadeIn(gb, shift=LEFT * 0.2), run_time=0.8)

        lj = Text("LEFT JOIN", font_size=40, weight=BOLD, color="#6CB4EE")
        lj.next_to(tables, DOWN, buff=0.8)
        self.play(FadeIn(lj, scale=1.2), run_time=0.5)

        anchor = SurroundingRectangle(tA, color=Y, buff=0.06, stroke_width=3)
        atxt = Text("ANCHOR", font_size=18, weight=BOLD, color=Y)
        atxt.next_to(anchor, DOWN, buff=0.1)
        self.play(Create(anchor), FadeIn(atxt), run_time=0.6)
        self.wait(1)

        # FIX 1: Result in anchor order — Alice, Bob, Charlie
        ws_r, cols_r = [1.0, 1.6, 1.6], [Y, B, G]
        r_hdr = self.mrow(["ID", "Name", "Dept"], ws_r, cols_r, 0.7, 0.9, 26)

        # Row 1: Alice + NA
        a_id = self.c("1", 1.0, 0.7, Y, 0.5, 22)
        a_name = self.c("Alice", 1.6, 0.7, B, 0.5, 22)
        na_rect = DashedVMobject(
            Rectangle(width=1.6, height=0.7, stroke_color=GRAY, stroke_width=1.5), num_dashes=14)
        na_txt = Text("NA", font_size=22, color=GRAY_A)
        a_na = VGroup(na_rect, na_txt)
        na_txt.move_to(na_rect)
        r_alice = VGroup(a_id, a_name, a_na).arrange(RIGHT, buff=0)

        # Row 2 & 3
        r_bob = self.mrow(["2", "Bob", "HR"], ws_r, cols_r)
        r_charlie = self.mrow(["3", "Charlie", "IT"], ws_r, cols_r)

        result = VGroup(r_hdr, r_alice, r_bob, r_charlie).arrange(DOWN, buff=0)
        result.next_to(lj, DOWN, buff=1.0)

        self.play(FadeIn(r_hdr), run_time=0.3)

        # FIX 3: Physical slide-down — copies move_to target positions
        # Row 1: Alice slides down, Sales grays out simultaneously
        alice_copy = dA[0].copy()
        self.add(alice_copy)
        alice_tgt = VGroup(a_id, a_name)
        self.play(
            alice_copy.animate.move_to(alice_tgt.get_center()),
            dB[2].animate.set_color("#333333"),  # FIX 4: sync gray-out
            run_time=1,
        )
        self.remove(alice_copy)
        self.add(a_id, a_name)

        # NA cell flashes in
        self.play(FadeIn(a_na, scale=1.3), run_time=0.5)
        flash = SurroundingRectangle(a_na, color=R, buff=0.02, stroke_width=2.5)
        self.play(Create(flash), run_time=0.3)
        self.play(FadeOut(flash), run_time=0.3)

        # Row 2: Bob + HR slide down
        bob_a = dA[1].copy()
        bob_b = dB[0].copy()
        self.add(bob_a, bob_b)
        self.play(
            bob_a.animate.move_to(r_bob.get_center() + LEFT * 0.8),
            bob_b.animate.move_to(r_bob.get_center() + RIGHT * 0.8),
            run_time=1,
        )
        self.remove(bob_a, bob_b)
        self.add(r_bob)

        # Row 3: Charlie + IT slide down
        cha_a = dA[2].copy()
        cha_b = dB[1].copy()
        self.add(cha_a, cha_b)
        self.play(
            cha_a.animate.move_to(r_charlie.get_center() + LEFT * 0.8),
            cha_b.animate.move_to(r_charlie.get_center() + RIGHT * 0.8),
            run_time=1,
        )
        self.remove(cha_a, cha_b)
        self.add(r_charlie)

        # Sales dissolves
        self.play(FadeOut(dB[2], shift=DOWN * 0.3, scale=0.3), run_time=0.8)
        self.wait(0.5)

        n3 = self.note("\U0001f4a1 Crucial Concept:",
                       "The left anchor table keeps all its\nrows. Missing matches are filled\nwith NA.",
                       "#58D68D")
        n3.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(n3, shift=UP * 0.2), run_time=0.7)
        self.wait(3)
        self.play(FadeOut(n3, shift=DOWN * 0.2), run_time=0.5)

    # ── SCENE 4: Right Join ──
    def scene_right_join(self, B, G, Y, R):
        ga, gb, tA, tB, hA, hB, dA, dB = self.build_tables(B, G)
        tables = VGroup(ga, gb).arrange(RIGHT, buff=0.5)
        tables.move_to(UP * 4.0)
        self.play(FadeIn(ga, shift=RIGHT * 0.2), FadeIn(gb, shift=LEFT * 0.2), run_time=0.8)

        rj = Text("RIGHT JOIN", font_size=40, weight=BOLD, color="#58D68D")
        rj.next_to(tables, DOWN, buff=0.8)
        self.play(FadeIn(rj, scale=1.2), run_time=0.5)

        anchor = SurroundingRectangle(tB, color=Y, buff=0.06, stroke_width=3)
        atxt = Text("ANCHOR", font_size=18, weight=BOLD, color=Y)
        atxt.next_to(anchor, DOWN, buff=0.1)
        self.play(Create(anchor), FadeIn(atxt), run_time=0.6)
        self.wait(1)

        # Result: anchor order (Table B) — HR, IT, Sales
        ws_r, cols_r = [1.0, 1.6, 1.6], [Y, B, G]
        r_hdr = self.mrow(["ID", "Name", "Dept"], ws_r, cols_r, 0.7, 0.9, 26)

        r_bob = self.mrow(["2", "Bob", "HR"], ws_r, cols_r)
        r_charlie = self.mrow(["3", "Charlie", "IT"], ws_r, cols_r)

        # Sales row with NA Name
        s_id = self.c("4", 1.0, 0.7, Y, 0.5, 22)
        na_rect = DashedVMobject(
            Rectangle(width=1.6, height=0.7, stroke_color=GRAY, stroke_width=1.5), num_dashes=14)
        na_txt = Text("NA", font_size=22, color=GRAY_A)
        s_na = VGroup(na_rect, na_txt)
        na_txt.move_to(na_rect)
        s_dept = self.c("Sales", 1.6, 0.7, G, 0.5, 22)
        r_sales = VGroup(s_id, s_na, s_dept).arrange(RIGHT, buff=0)

        result = VGroup(r_hdr, r_bob, r_charlie, r_sales).arrange(DOWN, buff=0)
        result.next_to(rj, DOWN, buff=1.0)

        self.play(FadeIn(r_hdr), run_time=0.3)

        # FIX 3+4: physical slide-down with synced gray-out of Alice
        # Row 1: Bob + HR slide down, Alice grays out simultaneously
        bob_a = dA[1].copy()
        bob_b = dB[0].copy()
        self.add(bob_a, bob_b)
        self.play(
            bob_a.animate.move_to(r_bob.get_center() + LEFT * 0.8),
            bob_b.animate.move_to(r_bob.get_center() + RIGHT * 0.8),
            dA[0].animate.set_color("#333333"),  # FIX 4: sync gray-out
            run_time=1,
        )
        self.remove(bob_a, bob_b)
        self.add(r_bob)

        # Row 2: Charlie + IT slide down
        cha_a = dA[2].copy()
        cha_b = dB[1].copy()
        self.add(cha_a, cha_b)
        self.play(
            cha_a.animate.move_to(r_charlie.get_center() + LEFT * 0.8),
            cha_b.animate.move_to(r_charlie.get_center() + RIGHT * 0.8),
            run_time=1,
        )
        self.remove(cha_a, cha_b)
        self.add(r_charlie)

        # Row 3: Sales slides down, NA flashes — FIX 2: FadeIn cells cleanly
        sales_copy = dB[2].copy()
        self.add(sales_copy)
        self.play(
            sales_copy.animate.move_to(VGroup(s_id, s_dept).get_center()),
            run_time=1,
        )
        self.remove(sales_copy)
        self.play(FadeIn(s_id), FadeIn(s_dept), run_time=0.4)

        # NA cell flashes
        self.play(FadeIn(s_na, scale=1.3), run_time=0.5)
        flash = SurroundingRectangle(s_na, color=R, buff=0.02, stroke_width=2.5)
        self.play(Create(flash), run_time=0.3)
        self.play(FadeOut(flash), run_time=0.3)

        # Alice dissolves (already grayed out)
        self.play(FadeOut(dA[0], shift=DOWN * 0.3, scale=0.3), run_time=0.8)
        self.wait(0.5)

        n4 = self.note("\U0001f4a1 Right Join:",
                       "The right anchor table keeps all its\nrows. Missing matches from the left\ntable are filled with NA.",
                       "#58D68D")
        n4.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(n4, shift=UP * 0.2), run_time=0.7)
        self.wait(3)
        self.play(FadeOut(n4, shift=DOWN * 0.2), run_time=0.5)
