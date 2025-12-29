from manim import *


def color_substring_in_mathtex(math_tex_mob, substring, color):
    """
    1) Finds `substring` in the raw LaTeX from `math_tex_mob.get_tex_string()`.
    2) Maps that range [start, end) onto the submobjects in math_tex_mob[0].submobjects
       by cumulatively counting length of submob.tex_string.
    3) If a submob overlaps the substring’s range, color that entire submob.

    NOTE: This may over‐color if your substring crosses submob boundaries.
    """

    # Get the entire raw LaTeX
    full_tex = math_tex_mob.get_tex_string()
    start_idx = full_tex.find(substring)
    if start_idx == -1:
        print(f"[WARN] Substring '{substring}' not found in: {full_tex}")
        return

    end_idx = start_idx + len(substring)

    # We now walk over each submob's .tex_string, and keep a running total of length
    cumulative_length = 0
    for submob in math_tex_mob[0].submobjects:
        # Some submobs have no .tex_string (like SVG paths).
        # We skip those.
        if not hasattr(submob, "tex_string"):
            continue

        submob_text = submob.tex_string
        submob_len = len(submob_text)

        # The submob covers character indices [cumulative_length, cumulative_length + submob_len)
        submob_start = cumulative_length
        submob_end = cumulative_length + submob_len

        # If there's ANY overlap with [start_idx, end_idx), color the whole submob
        if submob_end > start_idx and submob_start < end_idx:
            submob.set_color(color)

        cumulative_length += submob_len


class ColorSubstringExample(Scene):
    def construct(self):
        # A sample MathTex
        expr = MathTex(r"S_{O} (x; -4) = (-x; 4)")
        self.play(Write(expr))

        # Let's color the substring "-4" in YELLOW
        color_substring_in_mathtex(expr, "-4", YELLOW)

        # Also color "4)" in RED, for demonstration
        color_substring_in_mathtex(expr, "4)", RED)

        self.wait(2)
