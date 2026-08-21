from manim import *
import numpy as np

# VS Code Dark Theme colors (matches the rest of this repo's projects)
DARK_BG = "#1e1e1e"
TEXT_PRIMARY = "#e0e0e0"
TEXT_SECONDARY = "#9e9e9e"

ACCENT = "#4fc3f7"
ACCENT_WARM = "#ffb74d"
ACCENT_GREEN = "#81c784"
ACCENT_RED = "#e57373"

# The white diagram line/label color overlaid on every example scene below,
# kept visually distinct from the scene's own geometry.
GUIDE_COLOR = "#ffffff"

# Small "world" palette shared by every example scene, so the seven sections
# read as one consistent place rather than seven unrelated icons.
BUILDING_DARK = "#4a4a4a"
BUILDING_MID = "#5e5e5e"
BUILDING_LIGHT = "#727272"
WINDOW_LIT = "#ffe9a8"
ROAD_COLOR = "#333333"
ROAD_LINE = TEXT_SECONDARY
WATER_COLOR = "#4a90d9"
FOLIAGE_COLOR = ACCENT_GREEN
FOLIAGE_DARK = "#4c7a52"
FIGURE_COLOR = TEXT_PRIMARY

FONT = "Times New Roman"
FONT_MONO = "Menlo"

# Manim/Pango renders Text with subtly broken word-spacing at small point
# sizes (glyph advances get rounded off) - rendering bigger then scaling
# down avoids it entirely, so every caption/label goes through this instead
# of calling Text() directly. (Same fix as camera_lens_numbers/scene.py.)
_TEXT_RENDER_SCALE = 4


def make_text(content, font_size=20, **kwargs):
    text = Text(content, font_size=font_size * _TEXT_RENDER_SCALE, **kwargs)
    text.scale(1 / _TEXT_RENDER_SCALE)
    return text


# ----------------------------------------------------------------------
# Shared "world" pieces reused across sections (duplicated-style helpers
# rather than a real asset library, matching this repo's per-project
# convention - see camera_lens_numbers/README.md).

def make_tree(scale=1.0, color=FOLIAGE_COLOR):
    trunk = Rectangle(width=0.1, height=0.35, color="#6b4a35", fill_opacity=1, stroke_width=0)
    top = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.45)
    top.next_to(trunk, UP, buff=-0.1)
    tree = VGroup(trunk, top)
    tree.scale(scale)
    return tree


def make_figure(scale=1.0, color=FIGURE_COLOR):
    head = Circle(radius=0.09, color=color, fill_opacity=1, stroke_width=0)
    body = Line(ORIGIN, DOWN * 0.35, color=color, stroke_width=4)
    body.next_to(head, DOWN, buff=0)
    leg_l = Line(ORIGIN, DOWN * 0.2 + LEFT * 0.1, color=color, stroke_width=4)
    leg_r = Line(ORIGIN, DOWN * 0.2 + RIGHT * 0.1, color=color, stroke_width=4)
    legs = VGroup(leg_l, leg_r)
    legs.next_to(body, DOWN, buff=0)
    fig = VGroup(head, body, legs)
    fig.scale(scale)
    return fig


def make_skyline(n=6, seed=7, width=10, base_height=0.8, jitter=1.6, color=BUILDING_MID):
    """A row of buildings with randomized (but seeded, so reproducible)
    heights - just enough texture to read as a skyline, not a real one."""
    rng = np.random.default_rng(seed)
    bw = width / n
    group = VGroup()
    for i in range(n):
        h = base_height + rng.random() * jitter
        rect = Rectangle(width=bw * 0.82, height=h, color=color, fill_opacity=1, stroke_width=0)
        rect.move_to(RIGHT * (-width / 2 + bw * (i + 0.5)) + UP * (h / 2))
        group.add(rect)
    return group


def make_horizon_line(width=14, color=TEXT_SECONDARY):
    return Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=2)


class CompositionRules(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        self.title_screen()
        self.texture_repetition()
        self.curving_lines()
        self.foreground()
        self.rule_of_thirds()
        self.vanishing_point()
        self.frame_within_frame()
        self.centered_composition()
        self.end_screen()

    # ------------------------------------------------------------------
    def section_header(self, text_content, definition=None):
        header = make_text(text_content, font=FONT, font_size=30, color=ACCENT)
        header.to_edge(UP, buff=0.6)
        self.play(FadeIn(header), run_time=0.4)

        if definition:
            def_text = make_text(definition, font=FONT, font_size=18, color=TEXT_SECONDARY, slant=ITALIC)
            def_text.next_to(header, DOWN, buff=0.25)
            self.play(FadeIn(def_text), run_time=0.4)
            self.wait(1.6)
            self.play(FadeOut(def_text), run_time=0.4)

        return header

    # ------------------------------------------------------------------
    def title_screen(self):
        title = make_text("The Power of Composition", font=FONT, font_size=44, color=TEXT_PRIMARY)
        subtitle = make_text(
            "seven ideas that turn a snapshot into a photograph",
            font=FONT, font_size=20, color=ACCENT,
        )
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.6)

    # ------------------------------------------------------------------
    def texture_repetition(self):
        header = self.section_header(
            "Texture & Repetition",
            "a repeating pattern gives even a plain surface visual rhythm",
        )

        rows, cols, spacing = 5, 8, 0.55
        rng = np.random.default_rng(3)
        grid = VGroup()
        for r in range(rows):
            for c in range(cols):
                lit = rng.random() < 0.35
                sq = Square(
                    side_length=0.32,
                    color=WINDOW_LIT if lit else BUILDING_LIGHT,
                    fill_opacity=1, stroke_color=DARK_BG, stroke_width=2,
                )
                sq.move_to(RIGHT * (c - (cols - 1) / 2) * spacing + UP * (r - (rows - 1) / 2) * spacing)
                grid.add(sq)
        grid.move_to(DOWN * 0.2)

        self.play(LaggedStartMap(FadeIn, grid, lag_ratio=0.02), run_time=2.0)

        mid_row = VGroup(*grid[2 * cols:3 * cols])
        row_box = SurroundingRectangle(mid_row, color=GUIDE_COLOR, buff=0.08)
        self.play(Create(row_box), run_time=0.8)

        caption = make_text("same shape, repeated - the eye reads it as one pattern", font=FONT, font_size=18, color=TEXT_SECONDARY)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.8)
        self.play(FadeOut(grid), FadeOut(row_box), FadeOut(caption), FadeOut(header), run_time=0.6)

    # ------------------------------------------------------------------
    def curving_lines(self):
        header = self.section_header(
            "Curving Lines",
            "an S-curve leads the eye gently into the frame instead of straight through it",
        )

        ground = make_horizon_line(width=13, color=ROAD_LINE).shift(DOWN * 2.6)

        pts = [
            np.array([-5.5, -2.6, 0]),
            np.array([-2.0, -1.6, 0]),
            np.array([0.5, -0.4, 0]),
            np.array([1.5, 0.8, 0]),
            np.array([0.3, 2.2, 0]),
        ]
        river = VMobject(stroke_color=WATER_COLOR, stroke_width=26, fill_opacity=0)
        river.set_points_smoothly(pts)
        guide = VMobject(stroke_color=GUIDE_COLOR, stroke_width=3, fill_opacity=0)
        guide.set_points_smoothly(pts)

        tree_specs = [(-4.7, -2.3, 1.0), (-1.6, -1.2, 0.8), (0.9, 0.1, 0.55), (1.7, 1.4, 0.4)]
        trees = VGroup(*[make_tree(scale=s).move_to(np.array([x, y, 0])) for x, y, s in tree_specs])

        self.play(FadeIn(ground), run_time=0.5)
        self.play(Create(river), run_time=1.4)
        self.play(LaggedStartMap(FadeIn, trees, lag_ratio=0.3), run_time=1.2)
        self.play(Create(guide), run_time=1.2)

        caption = make_text("the S-curve keeps the eye moving instead of stopping short", font=FONT, font_size=18, color=TEXT_SECONDARY)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.8)
        self.play(FadeOut(ground), FadeOut(river), FadeOut(trees), FadeOut(guide), FadeOut(caption), FadeOut(header), run_time=0.6)

    # ------------------------------------------------------------------
    def foreground(self):
        header = self.section_header(
            "Foreground",
            "something close to the lens gives the shot layers instead of a flat background",
        )

        bg_sky = make_skyline(n=7, seed=11, width=11, base_height=0.6, jitter=1.1, color=BUILDING_DARK)
        bg_sky.scale(0.55).shift(UP * 1.4)
        bg_sky.set_opacity(0.55)
        mid_hz = make_horizon_line(width=13, color=TEXT_SECONDARY).shift(UP * 0.65)

        figure = make_figure(scale=1.6, color=FIGURE_COLOR).move_to(DOWN * 1.3)

        leaf_l = Polygon(
            np.array([-6.5, -3.6, 0]), np.array([-6.5, 0.6, 0]),
            np.array([-3.0, -1.2, 0]), np.array([-4.2, -3.6, 0]),
            color=FOLIAGE_DARK, fill_opacity=0.92, stroke_width=0,
        )
        leaf_r = Polygon(
            np.array([6.5, -3.6, 0]), np.array([6.5, 0.6, 0]),
            np.array([3.0, -1.2, 0]), np.array([4.2, -3.6, 0]),
            color=FOLIAGE_DARK, fill_opacity=0.92, stroke_width=0,
        )

        depth_labels = VGroup(
            make_text("background", font=FONT, font_size=14, color=TEXT_SECONDARY).move_to(UP * 2.4 + LEFT * 4.5),
            make_text("foreground", font=FONT, font_size=14, color=GUIDE_COLOR).move_to(DOWN * 3.0 + LEFT * 5.3),
        )

        self.play(FadeIn(bg_sky), FadeIn(mid_hz), run_time=0.8)
        self.play(FadeIn(figure), run_time=0.5)
        self.play(FadeIn(leaf_l), FadeIn(leaf_r), run_time=0.9)
        self.play(FadeIn(depth_labels), run_time=0.5)

        caption = make_text("near, middle, far - three layers read as depth, not a flat cutout", font=FONT, font_size=18, color=TEXT_SECONDARY)
        caption.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.8)
        self.play(
            FadeOut(bg_sky), FadeOut(mid_hz), FadeOut(figure), FadeOut(leaf_l), FadeOut(leaf_r),
            FadeOut(depth_labels), FadeOut(caption), FadeOut(header), run_time=0.6,
        )

    # ------------------------------------------------------------------
    def rule_of_thirds(self):
        header = self.section_header(
            "Rule of Thirds",
            "place the subject on a grid line or intersection - not dead center",
        )

        frame_w, frame_h = 10.5, 5.6
        x1, x2 = -frame_w / 6, frame_w / 6
        y1, y2 = -frame_h / 6, frame_h / 6

        def vline(x):
            return Line(np.array([x, frame_h / 2, 0]), np.array([x, -frame_h / 2, 0]), color=GUIDE_COLOR, stroke_width=2)

        def hline(y):
            return Line(np.array([-frame_w / 2, y, 0]), np.array([frame_w / 2, y, 0]), color=GUIDE_COLOR, stroke_width=2)

        grid = VGroup(vline(x1), vline(x2), hline(y1), hline(y2))

        hills = Polygon(
            np.array([-frame_w / 2, y1, 0]), np.array([-1.5, y1 + 0.9, 0]),
            np.array([0.5, y1 + 0.3, 0]), np.array([2.5, y1 + 1.3, 0]),
            np.array([frame_w / 2, y1 + 0.4, 0]), np.array([frame_w / 2, -frame_h / 2, 0]),
            np.array([-frame_w / 2, -frame_h / 2, 0]),
            color=BUILDING_DARK, fill_opacity=1, stroke_width=0,
        )

        sun = Circle(radius=0.35, color=WINDOW_LIT, fill_opacity=1, stroke_width=0)
        sun.move_to(np.array([x2, y2, 0]))
        highlight = Circle(radius=0.55, color=GUIDE_COLOR, stroke_width=2).move_to(sun.get_center())

        self.play(FadeIn(hills), run_time=0.6)
        self.play(Create(grid), run_time=1.2)
        self.play(FadeIn(sun), run_time=0.5)
        self.play(Create(highlight), run_time=0.5)

        caption = make_text("the horizon sits on a line, the sun sits on an intersection", font=FONT, font_size=18, color=TEXT_SECONDARY)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.8)
        self.play(FadeOut(hills), FadeOut(grid), FadeOut(sun), FadeOut(highlight), FadeOut(caption), FadeOut(header), run_time=0.6)

    # ------------------------------------------------------------------
    def vanishing_point(self):
        header = self.section_header(
            "Vanishing Point",
            "parallel lines appear to converge in the distance - aim the frame at that point",
        )

        vp = np.array([0, 0.4, 0])
        bl = np.array([-5.5, -3.4, 0])
        br = np.array([5.5, -3.4, 0])

        road = Polygon(bl, br, vp, color=ROAD_COLOR, fill_opacity=1, stroke_width=0)
        edge_l = Line(bl, vp, color=GUIDE_COLOR, stroke_width=3)
        edge_r = Line(br, vp, color=GUIDE_COLOR, stroke_width=3)

        ties = VGroup()
        for t in [0.15, 0.32, 0.5, 0.68, 0.84]:
            p_l = bl + t * (vp - bl)
            p_r = br + t * (vp - br)
            ties.add(Line(p_l, p_r, color=ROAD_LINE, stroke_width=2))

        vp_dot = Dot(vp, color=GUIDE_COLOR, radius=0.06)
        vp_label = make_text("vanishing point", font=FONT, font_size=16, color=GUIDE_COLOR)
        vp_label.next_to(vp_dot, UP, buff=0.5)
        vp_arrow = Arrow(vp_label.get_bottom(), vp_dot.get_center(), buff=0.08, color=GUIDE_COLOR, stroke_width=2)

        self.play(FadeIn(road), run_time=0.6)
        self.play(Create(edge_l), Create(edge_r), run_time=1.0)
        self.play(LaggedStartMap(Create, ties, lag_ratio=0.3), run_time=1.2)
        self.play(FadeIn(vp_dot), FadeIn(vp_label), FadeIn(vp_arrow), run_time=0.6)

        caption = make_text("point the frame so the convergence lands where you want the eye to land", font=FONT, font_size=18, color=TEXT_SECONDARY)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.8)
        self.play(
            FadeOut(road), FadeOut(edge_l), FadeOut(edge_r), FadeOut(ties),
            FadeOut(vp_dot), FadeOut(vp_label), FadeOut(vp_arrow), FadeOut(caption), FadeOut(header), run_time=0.6,
        )

    # ------------------------------------------------------------------
    def frame_within_frame(self):
        header = self.section_header(
            "Frame within a Frame",
            "foreground shapes around the edges box the subject in and pull focus toward it",
        )

        bg = make_skyline(n=5, seed=21, width=6, base_height=0.7, jitter=1.3, color=BUILDING_MID)

        outer_w, outer_h = 12.5, 5.8
        opening_w, opening_h = 6.8, 3.2
        bar_color = "#141414"

        top_bar = Rectangle(width=outer_w, height=(outer_h - opening_h) / 2, color=bar_color, fill_opacity=1, stroke_width=0)
        top_bar.move_to(UP * (opening_h / 2 + top_bar.height / 2))
        bottom_bar = top_bar.copy().move_to(DOWN * (opening_h / 2 + top_bar.height / 2))
        left_bar = Rectangle(width=(outer_w - opening_w) / 2, height=outer_h, color=bar_color, fill_opacity=1, stroke_width=0)
        left_bar.move_to(LEFT * (opening_w / 2 + left_bar.width / 2))
        right_bar = left_bar.copy().move_to(RIGHT * (opening_w / 2 + left_bar.width / 2))
        frame_group = VGroup(top_bar, bottom_bar, left_bar, right_bar)
        frame_outline = Rectangle(width=opening_w, height=opening_h, color=GUIDE_COLOR, stroke_width=3)

        diagram = VGroup(bg, frame_group, frame_outline)
        diagram.shift(DOWN * 0.2)

        self.play(FadeIn(bg), run_time=0.7)
        self.play(FadeIn(frame_group), run_time=0.9)
        self.play(Create(frame_outline), run_time=0.8)

        caption = make_text("the dark edges vanish - the eye only reads what's inside the frame", font=FONT, font_size=18, color=TEXT_SECONDARY)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.8)
        self.play(FadeOut(bg), FadeOut(frame_group), FadeOut(frame_outline), FadeOut(caption), FadeOut(header), run_time=0.6)

    # ------------------------------------------------------------------
    def centered_composition(self):
        header = self.section_header(
            "Center",
            "sometimes symmetry earns the middle - stillness instead of dynamic tension",
        )

        arch_w = 3.2
        arch = Polygon(
            np.array([-arch_w / 2, -2.6, 0]), np.array([-arch_w / 2, 1.0, 0]),
            np.array([0, 2.0, 0]), np.array([arch_w / 2, 1.0, 0]), np.array([arch_w / 2, -2.6, 0]),
            color=BUILDING_DARK, fill_opacity=1, stroke_width=0,
        )
        inner_w = arch_w - 0.9
        inner = Polygon(
            np.array([-inner_w / 2, -2.6, 0]), np.array([-inner_w / 2, 0.7, 0]),
            np.array([0, 1.5, 0]), np.array([inner_w / 2, 0.7, 0]), np.array([inner_w / 2, -2.6, 0]),
            color=DARK_BG, fill_opacity=1, stroke_width=0,
        )

        tree_l = make_tree(scale=1.1).move_to(LEFT * 3.2 + DOWN * 1.0)
        tree_r = make_tree(scale=1.1).move_to(RIGHT * 3.2 + DOWN * 1.0)
        figure = make_figure(scale=3.0, color=FIGURE_COLOR).move_to(DOWN * 1.3)

        v_line = Line(UP * 3.0, DOWN * 3.0, color=GUIDE_COLOR, stroke_width=2)
        h_line = Line(LEFT * 4.5, RIGHT * 4.5, color=GUIDE_COLOR, stroke_width=2)
        crosshair = VGroup(v_line, h_line)

        self.play(FadeIn(tree_l), FadeIn(tree_r), run_time=0.6)
        self.play(FadeIn(arch), FadeIn(inner), run_time=0.8)
        self.play(FadeIn(figure), run_time=0.5)
        self.play(Create(crosshair), run_time=0.8)

        caption = make_text("symmetric elements on both sides make the center feel earned, not lazy", font=FONT, font_size=18, color=TEXT_SECONDARY)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.8)
        self.play(
            FadeOut(tree_l), FadeOut(tree_r), FadeOut(arch), FadeOut(inner), FadeOut(figure),
            FadeOut(crosshair), FadeOut(caption), FadeOut(header), run_time=0.6,
        )

    # ------------------------------------------------------------------
    def end_screen(self):
        title = make_text("Composition is a choice, not an accident", font=FONT, font_size=34, color=TEXT_PRIMARY)
        subtitle = make_text(
            "texture, curves, foreground, thirds, vanishing point, frame, center",
            font=FONT, font_size=18, color=ACCENT,
        )
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=0.6)
        self.wait(2.0)
