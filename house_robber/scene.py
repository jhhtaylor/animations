from manim import *
import os

# VS Code Dark Theme colors
DARK_BG = "#1e1e1e"
CARD_BG = "#2d2d2d"
CARD_LIGHT = "#3c3c3c"
ACCENT = "#4fc3f7"
ACCENT_WARM = "#ffb74d"
ACCENT_GREEN = "#81c784"
ACCENT_RED = "#e57373"
TEXT_PRIMARY = "#e0e0e0"
TEXT_SECONDARY = "#9e9e9e"
TEXT_DARK = "#1e1e1e"

FONT = "Times New Roman"
FONT_MONO = "Menlo"

CORNER_RADIUS = 0.12

# Path to icons
ICON_DIR = os.path.join(os.path.dirname(__file__), "icons")


class HouseRobber(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        self.title_screen()
        self.problem_statement()

        # Example 1: Slow with detailed steps
        self.example_header("Example 1: Step by Step")
        self.run_example_slow([1, 2, 3, 1], box_size=1.1, box_buff=0.2)

        # Example 2: Fast - more complex
        self.example_header("Example 2: A More Complex Case")
        self.run_example_fast([2, 7, 9, 3, 1, 5, 8, 2, 4, 6], box_size=0.9, box_buff=0.12)

        self.show_code()
        self.end_screen()

    def create_icon(self, icon_name, size, color):
        """Load and style an SVG icon."""
        icon_path = os.path.join(ICON_DIR, f"{icon_name}.svg")
        icon = SVGMobject(icon_path)
        icon.set_fill(color, opacity=1)
        icon.set_stroke(width=0)
        icon.scale_to_fit_height(size)
        return icon

    def create_house_box(self, value, box_size, highlighted=False):
        """Create a house box with home icon in top-right corner."""
        if highlighted:
            fill_color = ACCENT_WARM
            text_color = TEXT_DARK
            icon_color = TEXT_DARK
        else:
            fill_color = CARD_LIGHT
            text_color = TEXT_PRIMARY
            icon_color = TEXT_SECONDARY

        box = RoundedRectangle(width=box_size, height=box_size, corner_radius=CORNER_RADIUS)
        box.set_fill(fill_color, opacity=0.95)
        box.set_stroke(width=0)

        # Home icon in top-right
        icon_size = box_size * 0.22
        icon = self.create_icon("home", icon_size, icon_color)
        icon.move_to(box.get_corner(UR) + LEFT * 0.15 + DOWN * 0.15)

        # Value in center
        font_size = 36 if box_size >= 1.0 else 26
        value_text = Text(str(value), font=FONT, font_size=font_size, color=text_color)
        value_text.move_to(box.get_center())

        return VGroup(box, icon, value_text)

    def create_person_box(self, label, value, box_size, highlighted=False):
        """Create a person/robber box with person icon in top-right corner."""
        if highlighted:
            fill_color = ACCENT_WARM
            text_color = TEXT_DARK
            icon_color = TEXT_DARK
        else:
            fill_color = CARD_BG
            text_color = TEXT_PRIMARY
            icon_color = TEXT_SECONDARY

        box = RoundedRectangle(width=box_size, height=box_size, corner_radius=CORNER_RADIUS)
        box.set_fill(fill_color, opacity=0.95)
        box.set_stroke(width=0)

        # Label in top-left
        label_size = 14 if box_size >= 1.0 else 10
        label_text = Text(label, font=FONT, font_size=label_size, color=text_color, slant=ITALIC)
        label_text.move_to(box.get_corner(UL) + RIGHT * 0.18 + DOWN * 0.15)

        # Person icon in top-right
        icon_size = box_size * 0.22
        icon = self.create_icon("person", icon_size, icon_color)
        icon.move_to(box.get_corner(UR) + LEFT * 0.15 + DOWN * 0.15)

        # Value in center
        if value:
            font_size = 40 if box_size >= 1.0 else 28
            value_text = Text(value, font=FONT, font_size=font_size, color=text_color)
            value_text.move_to(box.get_center() + DOWN * 0.05)
            return VGroup(box, label_text, icon, value_text)

        return VGroup(box, label_text, icon)

    def create_loot_box(self, label, value, box_size, highlighted=False):
        """Create a loot/temp box with briefcase icon in top-right corner."""
        if highlighted:
            fill_color = ACCENT_WARM
            text_color = TEXT_DARK
            icon_color = TEXT_DARK
        else:
            fill_color = CARD_BG
            text_color = TEXT_PRIMARY
            icon_color = ACCENT_GREEN

        box = RoundedRectangle(width=box_size, height=box_size, corner_radius=CORNER_RADIUS)
        box.set_fill(fill_color, opacity=0.95)
        box.set_stroke(width=0)

        # Label in top-left
        label_size = 14 if box_size >= 1.0 else 10
        label_text = Text(label, font=FONT, font_size=label_size, color=text_color, slant=ITALIC)
        label_text.move_to(box.get_corner(UL) + RIGHT * 0.18 + DOWN * 0.15)

        # Briefcase icon in top-right
        icon_size = box_size * 0.22
        icon = self.create_icon("briefcase", icon_size, icon_color)
        icon.move_to(box.get_corner(UR) + LEFT * 0.15 + DOWN * 0.15)

        # Value in center
        if value:
            font_size = 40 if box_size >= 1.0 else 28
            value_text = Text(value, font=FONT, font_size=font_size, color=text_color)
            value_text.move_to(box.get_center() + DOWN * 0.05)
            return VGroup(box, label_text, icon, value_text)

        return VGroup(box, label_text, icon)

    def run_example_slow(self, houses, box_size, box_buff):
        """Run the DP animation with detailed steps."""
        array_boxes = [self.create_house_box(val, box_size) for val in houses]
        array_group = VGroup(*array_boxes).arrange(RIGHT, buff=box_buff)
        array_group.to_edge(DOWN, buff=1.5)

        # Index labels
        indices = VGroup()
        for i, box in enumerate(array_boxes):
            idx = Text(str(i), font=FONT_MONO, font_size=12, color=TEXT_SECONDARY)
            idx.next_to(box, DOWN, buff=0.1)
            indices.add(idx)

        self.play(*[FadeIn(box) for box in array_boxes], FadeIn(indices), run_time=0.8)
        self.wait(0.3)

        # Explain variables
        explain_box = self.create_text_box(
            "We track two values:\nr1 = max money 2 houses back\nr2 = max money 1 house back",
            width=4.5,
            height=1.8
        )
        explain_box.to_corner(UL, buff=0.5)

        t_box = self.create_loot_box("t", "", box_size, highlighted=True)
        r1_box = self.create_person_box("r1", "", box_size, highlighted=True)
        r2_box = self.create_person_box("r2", "", box_size, highlighted=True)

        first_box_x = array_boxes[0].get_center()[0]
        base_y = array_boxes[0].get_center()[1]
        t_box.move_to([first_box_x + (box_size + box_buff), base_y + (box_size + box_buff) * 2, 0])
        r1_box.move_to([first_box_x, base_y + (box_size + box_buff), 0])
        r2_box.move_to([first_box_x + (box_size + box_buff), base_y + (box_size + box_buff), 0])

        self.play(FadeIn(explain_box), run_time=0.5)
        self.play(FadeIn(t_box), FadeIn(r1_box), FadeIn(r2_box), run_time=0.5)
        self.wait(1.5)

        # Initialize
        new_explain = self.create_text_box("Initialize: no houses\nrobbed yet, so all zero", width=4.5, height=1.2)
        new_explain.move_to(explain_box.get_center())

        new_t = self.create_loot_box("t", "0", box_size, highlighted=True)
        new_r1 = self.create_person_box("r1", "0", box_size, highlighted=True)
        new_r2 = self.create_person_box("r2", "0", box_size, highlighted=True)
        new_t.move_to(t_box.get_center())
        new_r1.move_to(r1_box.get_center())
        new_r2.move_to(r2_box.get_center())

        self.play(
            Transform(explain_box, new_explain),
            Transform(t_box, new_t),
            Transform(r1_box, new_r1),
            Transform(r2_box, new_r2),
            run_time=0.6
        )
        self.wait(1)
        self.play(FadeOut(explain_box), run_time=0.3)

        # Main loop
        r1, r2 = 0, 0

        for i, house_val in enumerate(houses):
            current_x = array_boxes[i].get_center()[0]
            base_y = array_boxes[i].get_center()[1]

            t_target = [current_x, base_y + (box_size + box_buff) * 2, 0]
            r1_target = [current_x - (box_size + box_buff), base_y + (box_size + box_buff), 0]
            r2_target = [current_x, base_y + (box_size + box_buff), 0]

            self.play(
                t_box.animate.move_to(t_target),
                r1_box.animate.move_to(r1_target),
                r2_box.animate.move_to(r2_target),
                run_time=0.5
            )

            # Highlight r1
            new_r1_hl = self.create_person_box("r1", str(r1), box_size, highlighted=True)
            new_r1_hl.move_to(r1_box.get_center())
            new_r2_dim = self.create_person_box("r2", str(r2), box_size, highlighted=False)
            new_r2_dim.move_to(r2_box.get_center())
            new_t_dim = self.create_loot_box("t", str(r2 if i > 0 else 0), box_size, highlighted=False)
            new_t_dim.move_to(t_box.get_center())

            self.play(
                Transform(r1_box, new_r1_hl),
                Transform(r2_box, new_r2_dim),
                Transform(t_box, new_t_dim),
                run_time=0.3
            )

            # Question
            question_box = self.create_text_box(
                f"House {i+1}: Rob it (+{house_val}) or skip?",
                width=4.5, height=0.9
            )
            question_box.to_corner(UL, buff=0.5)
            self.play(FadeIn(question_box), run_time=0.4)
            self.wait(0.5)
            self.play(FadeOut(question_box), run_time=0.3)

            # Plus sign
            plus_sign = Text("+", font=FONT, font_size=36, color=ACCENT_WARM)
            plus_sign.move_to([
                r1_target[0] + (box_size + box_buff) / 2,
                r1_target[1] - (box_size + box_buff) / 2,
                0
            ])

            # Highlight house
            highlighted_house = self.create_house_box(house_val, box_size, highlighted=True)
            highlighted_house.move_to(array_boxes[i].get_center())

            self.play(
                FadeIn(plus_sign),
                Transform(array_boxes[i], highlighted_house),
                run_time=0.3
            )
            self.wait(0.3)

            # Calculate
            r1_plus_val = r1 + house_val
            t = max(r1_plus_val, r2)
            is_rob = r1_plus_val >= r2

            if is_rob:
                explanation = f"{r1}+{house_val}={r1_plus_val} ≥ {r2}"
                exp_color = ACCENT_GREEN
            else:
                explanation = f"{r2} > {r1}+{house_val}={r1_plus_val} SKIP!"
                exp_color = ACCENT_RED

            calc_text = Text(explanation, font=FONT_MONO, font_size=20, color=exp_color)
            calc_text.to_corner(UL, buff=0.5)

            new_t = self.create_loot_box("t", str(t), box_size, highlighted=True)
            new_t.move_to(t_box.get_center())

            self.play(
                FadeIn(calc_text),
                Transform(t_box, new_t),
                run_time=0.5
            )
            self.wait(0.8)

            # Reset house
            reset_house = self.create_house_box(house_val, box_size, highlighted=False)
            reset_house.move_to(array_boxes[i].get_center())

            self.play(
                FadeOut(plus_sign),
                FadeOut(calc_text),
                Transform(array_boxes[i], reset_house),
                run_time=0.3
            )

            # Shift
            shift_explain = self.create_text_box("Shift values forward", width=3.5, height=0.9)
            shift_explain.to_corner(UL, buff=0.5)
            self.play(FadeIn(shift_explain), run_time=0.3)

            new_r1_hl = self.create_person_box("r1", str(r2), box_size, highlighted=True)
            new_r1_hl.move_to(r1_box.get_center())
            self.play(Transform(r1_box, new_r1_hl), run_time=0.4)

            new_r1_dim = self.create_person_box("r1", str(r2), box_size, highlighted=False)
            new_r1_dim.move_to(r1_box.get_center())
            self.play(Transform(r1_box, new_r1_dim), run_time=0.2)

            new_r2_hl = self.create_person_box("r2", str(t), box_size, highlighted=True)
            new_r2_hl.move_to(r2_box.get_center())
            self.play(Transform(r2_box, new_r2_hl), run_time=0.4)

            new_r2_dim = self.create_person_box("r2", str(t), box_size, highlighted=False)
            new_r2_dim.move_to(r2_box.get_center())
            self.play(Transform(r2_box, new_r2_dim), run_time=0.2)

            final_t = self.create_loot_box("t", str(t), box_size, highlighted=False)
            final_t.move_to(t_box.get_center())
            self.play(
                Transform(t_box, final_t),
                FadeOut(shift_explain),
                run_time=0.3
            )

            r1 = r2
            r2 = t
            self.wait(0.3)

        # Final
        final_t_hl = self.create_loot_box("t", str(r2), box_size, highlighted=True)
        final_t_hl.move_to(t_box.get_center())
        self.play(Transform(t_box, final_t_hl), run_time=0.5)

        result_text = self.create_text_box(f"Maximum: ${r2}", width=2.8, height=0.9)
        result_text.next_to(t_box, UP, buff=0.3)
        self.play(FadeIn(result_text), run_time=0.5)
        self.wait(1.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)

    def run_example_fast(self, houses, box_size, box_buff):
        """Run the DP animation fast."""
        array_boxes = [self.create_house_box(val, box_size) for val in houses]
        array_group = VGroup(*array_boxes).arrange(RIGHT, buff=box_buff)
        array_group.to_edge(DOWN, buff=1.2)

        # Index labels
        indices = VGroup()
        for i, box in enumerate(array_boxes):
            idx = Text(str(i), font=FONT_MONO, font_size=12, color=TEXT_SECONDARY)
            idx.next_to(box, DOWN, buff=0.1)
            indices.add(idx)

        self.play(*[FadeIn(box) for box in array_boxes], FadeIn(indices), run_time=0.6)
        self.wait(0.2)

        explain = self.create_text_box("Same approach!", width=3, height=0.8)
        explain.to_corner(UL, buff=0.4)

        t_box = self.create_loot_box("t", "0", box_size, highlighted=False)
        r1_box = self.create_person_box("r1", "0", box_size, highlighted=False)
        r2_box = self.create_person_box("r2", "0", box_size, highlighted=False)

        first_box_x = array_boxes[0].get_center()[0]
        base_y = array_boxes[0].get_center()[1]
        t_box.move_to([first_box_x + (box_size + box_buff), base_y + (box_size + box_buff) * 2, 0])
        r1_box.move_to([first_box_x, base_y + (box_size + box_buff), 0])
        r2_box.move_to([first_box_x + (box_size + box_buff), base_y + (box_size + box_buff), 0])

        self.play(FadeIn(explain), FadeIn(t_box), FadeIn(r1_box), FadeIn(r2_box), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(explain), run_time=0.2)

        r1, r2 = 0, 0

        for i, house_val in enumerate(houses):
            current_x = array_boxes[i].get_center()[0]
            base_y = array_boxes[i].get_center()[1]

            t_target = [current_x, base_y + (box_size + box_buff) * 2, 0]
            r1_target = [current_x - (box_size + box_buff), base_y + (box_size + box_buff), 0]
            r2_target = [current_x, base_y + (box_size + box_buff), 0]

            self.play(
                t_box.animate.move_to(t_target),
                r1_box.animate.move_to(r1_target),
                r2_box.animate.move_to(r2_target),
                run_time=0.25
            )

            highlighted_house = self.create_house_box(house_val, box_size, highlighted=True)
            highlighted_house.move_to(array_boxes[i].get_center())
            self.play(Transform(array_boxes[i], highlighted_house), run_time=0.15)

            r1_plus_val = r1 + house_val
            t = max(r1_plus_val, r2)
            is_rob = r1_plus_val >= r2

            if is_rob:
                explanation = f"{r1}+{house_val}={r1_plus_val} ≥ {r2}"
                exp_color = ACCENT_GREEN
            else:
                explanation = f"{r2} > {r1}+{house_val}={r1_plus_val} SKIP!"
                exp_color = ACCENT_RED

            calc_text = Text(explanation, font=FONT_MONO, font_size=16, color=exp_color)
            calc_text.to_corner(UL, buff=0.4)

            new_t = self.create_loot_box("t", str(t), box_size, highlighted=True)
            new_t.move_to(t_box.get_center())

            self.play(FadeIn(calc_text), Transform(t_box, new_t), run_time=0.25)

            if not is_rob:
                self.wait(0.5)
            else:
                self.wait(0.2)

            reset_house = self.create_house_box(house_val, box_size, highlighted=False)
            reset_house.move_to(array_boxes[i].get_center())
            self.play(FadeOut(calc_text), Transform(array_boxes[i], reset_house), run_time=0.15)

            new_r1 = self.create_person_box("r1", str(r2), box_size, highlighted=True)
            new_r1.move_to(r1_box.get_center())
            self.play(Transform(r1_box, new_r1), run_time=0.15)

            new_r1_dim = self.create_person_box("r1", str(r2), box_size, highlighted=False)
            new_r1_dim.move_to(r1_box.get_center())

            new_r2 = self.create_person_box("r2", str(t), box_size, highlighted=True)
            new_r2.move_to(r2_box.get_center())
            self.play(Transform(r1_box, new_r1_dim), Transform(r2_box, new_r2), run_time=0.15)

            new_r2_dim = self.create_person_box("r2", str(t), box_size, highlighted=False)
            new_r2_dim.move_to(r2_box.get_center())

            final_t = self.create_loot_box("t", str(t), box_size, highlighted=False)
            final_t.move_to(t_box.get_center())
            self.play(Transform(t_box, final_t), Transform(r2_box, new_r2_dim), run_time=0.15)

            r1 = r2
            r2 = t

        final_t_hl = self.create_loot_box("t", str(r2), box_size, highlighted=True)
        final_t_hl.move_to(t_box.get_center())
        self.play(Transform(t_box, final_t_hl), run_time=0.3)

        result_text = self.create_text_box(f"Maximum: ${r2}", width=2.5, height=0.8)
        result_text.next_to(t_box, UP, buff=0.3)
        self.play(FadeIn(result_text), run_time=0.3)
        self.wait(1.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.4)

    def title_screen(self):
        author = Text("By Jon Taylor", font=FONT, font_size=20, color=TEXT_SECONDARY)
        author.to_corner(UL, buff=0.5)

        title = Text("House Robber", font=FONT, font_size=44, color=TEXT_PRIMARY)
        subtitle = Text("Dynamic Programming", font=FONT, font_size=22, color=ACCENT, slant=ITALIC)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2)
        title_group.move_to(ORIGIN)

        self.play(FadeIn(author), FadeIn(title_group), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(author), FadeOut(title_group), run_time=0.4)

    def problem_statement(self):
        credit = Text("LeetCode 198", font=FONT_MONO, font_size=16, color=TEXT_SECONDARY)
        credit.to_corner(UR, buff=0.5)

        title = Text("The Problem", font=FONT, font_size=32, color=TEXT_PRIMARY)
        title.to_edge(UP, buff=0.8)

        problem_text = """You are a robber planning to rob houses.
Each house has money, but adjacent houses
have connected alarms.

If you rob two adjacent houses,
the alarm triggers!

Goal: Maximize money without
triggering any alarms."""

        problem = Text(
            problem_text,
            font=FONT,
            font_size=22,
            color=TEXT_PRIMARY,
            line_spacing=0.9
        )
        problem.move_to(ORIGIN)

        self.play(FadeIn(credit), FadeIn(title), run_time=0.5)
        self.play(FadeIn(problem), run_time=0.8)
        self.wait(3)

        self.play(
            FadeOut(credit),
            FadeOut(title),
            FadeOut(problem),
            run_time=0.5
        )

    def example_header(self, title_text):
        header = Text(title_text, font=FONT, font_size=28, color=ACCENT)
        header.move_to(ORIGIN)
        self.play(FadeIn(header), run_time=0.3)
        self.wait(0.8)
        self.play(FadeOut(header), run_time=0.3)

    def create_text_box(self, text_content, width=3, height=1):
        box = RoundedRectangle(width=width, height=height, corner_radius=CORNER_RADIUS)
        box.set_fill(CARD_BG, opacity=0.95)
        box.set_stroke(width=0)

        text = Text(text_content, font=FONT, font_size=18, color=TEXT_PRIMARY, line_spacing=0.8)
        text.move_to(box.get_center())

        if text.width > width - 0.3:
            text.scale((width - 0.3) / text.width)

        return VGroup(box, text)

    def show_code(self):
        code_label = self.create_text_box("C#", width=1.2, height=0.8)
        code_label.to_corner(UL, buff=0.5)

        code_string = """public int Rob(int[] nums) {
    int rob1 = 0, rob2 = 0;
    foreach(var n in nums) {
        var t = Math.Max(rob1+n, rob2);
        rob1 = rob2;
        rob2 = t;
    }
    return rob2;
}"""

        code_text = Text(code_string, font=FONT_MONO, font_size=16, color=TEXT_PRIMARY, line_spacing=0.7)

        code_bg = RoundedRectangle(
            width=code_text.width + 0.8,
            height=code_text.height + 0.6,
            corner_radius=CORNER_RADIUS
        )
        code_bg.set_fill(CARD_BG, opacity=0.95)
        code_bg.set_stroke(width=0)
        code_bg.move_to(ORIGIN)
        code_text.move_to(code_bg.get_center())

        code = VGroup(code_bg, code_text)

        self.play(FadeIn(code_label), FadeIn(code), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(code_label), FadeOut(code), run_time=0.4)

    def end_screen(self):
        author = Text("By Jon Taylor", font=FONT, font_size=20, color=TEXT_SECONDARY)
        author.to_corner(UL, buff=0.5)

        github = Text("github.com/jhhtaylor", font=FONT_MONO, font_size=20, color=ACCENT)
        github.move_to(ORIGIN)

        thanks = Text("Thanks for watching!", font=FONT, font_size=24, color=TEXT_PRIMARY)
        thanks.next_to(github, DOWN, buff=0.4)

        self.play(FadeIn(author), FadeIn(github), FadeIn(thanks), run_time=0.5)
        self.wait(2)
