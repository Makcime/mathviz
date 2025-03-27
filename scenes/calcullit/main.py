import sympy
from manim import *
from sympy import expand, latex, simplify
from sympy.parsing.latex import parse_latex


class Mul1(Scene):
    def construct(self):
        # Create eq1: "3 a ⋅ 4 b ⋅ 2"
        # Tokens (indices):
        #   0: "3", 1: "a", 2: "\cdot", 3: "4", 4: "b", 5: "\cdot", 6: "2"
        eq1 = MathTex("{{3}}", "{{a}}", "\\cdot", "{{4}}", "{{b}}", "\\cdot", "{{2}}")
        # Color numbers blue and letters yellow.
        eq1[0].set_color(BLUE)  # "3"
        eq1[1].set_color(YELLOW)  # "a"
        eq1[3].set_color(BLUE)  # "4"
        eq1[4].set_color(YELLOW)  # "b"
        eq1[6].set_color(BLUE)  # "2"

        self.add(eq1)
        self.wait(0.5)

        # Create eq2: "= 12 ab ⋅ 2"
        # Tokens (indices):
        #   0: "=",
        #   1: "12",
        #   2: "ab",
        #   3: "\cdot",
        #   4: "2"
        eq2 = MathTex("=", "{{12}}", "{{ab}}", "\\cdot", "{{2}}")
        eq2[1].set_color(BLUE)  # "12"
        eq2[2].set_color(YELLOW)  # "ab"
        eq2[4].set_color(BLUE)  # "2"
        eq2.next_to(eq1, DOWN, buff=0.5, aligned_edge=LEFT)

        # For eq1 → eq2, we want:
        # - The tokens "3" (eq1[0]) and "4" (eq1[3]) to merge into eq2[1] ("12")
        # - The tokens "a" (eq1[1]) and "b" (eq1[4]) to merge into eq2[2] ("ab")
        # - The dot (eq1[5]) and the trailing "2" (eq1[6]) map to eq2[3] and eq2[4] respectively.
        numbers_group = VGroup(eq1[0], eq1[3])
        letters_group = VGroup(eq1[1], eq1[4])

        self.play(
            FadeIn(eq2[0]),  # fade in "="
            ReplacementTransform(numbers_group.copy(), eq2[1]),
            ReplacementTransform(letters_group.copy(), eq2[2]),
            ReplacementTransform(eq1[5].copy(), eq2[3]),
            ReplacementTransform(eq1[6].copy(), eq2[4]),
        )
        self.wait(0.5)

        # Create eq3: "= 24 ab"
        # Tokens (indices):
        #   0: "=",
        #   1: "24",
        #   2: "ab"
        eq3 = MathTex("=", "{{24}}", "{{ab}}")
        eq3[1].set_color(BLUE)  # "24"
        eq3[2].set_color(YELLOW)  # "ab"
        eq3.next_to(eq2, DOWN, buff=0.5, aligned_edge=LEFT)

        # For eq2 → eq3, we want:
        # - The "=" (eq2[0]) remains "=" (eq3[0])
        # - Merge eq2 tokens: "12" (eq2[1]), "\cdot" (eq2[3]), and "2" (eq2[4]) into eq3[1] ("24")
        # - The "ab" (eq2[2]) remains as "ab" (eq3[2])
        numbers_group_eq2 = VGroup(eq2[1], eq2[3], eq2[4])
        self.play(
            ReplacementTransform(eq2[0].copy(), eq3[0]),
            ReplacementTransform(numbers_group_eq2.copy(), eq3[1]),
            ReplacementTransform(eq2[2].copy(), eq3[2]),
        )
        self.wait(3)


def animate_eq_transformation(
    scene,
    eq1_tokens,
    eq1_groupings,
    eq2_tokens,
    eq2_groupings,
    buff=0.5,
    wait_time=1,
    starting_eq=None,
):
    """
    Create and display eq1 and eq2, then animate a transformation between them.

    Parameters:
      scene: the Scene instance (i.e. self in construct).
      eq1_tokens: list of strings for eq1 tokens (used in MathTex).
      eq1_groupings: dict mapping color (e.g. BLUE) -> list of indices for eq1 tokens to transform.
      eq2_tokens: list of strings for eq2 tokens.
      eq2_groupings: dict mapping color -> list of indices for eq2 tokens.
      buff: vertical spacing between equations.
      wait_time: time to wait after each step.
      starting_eq: an existing MathTex to use as eq1 (if chaining transformations).

    Behavior:
      1. If starting_eq is None, creates eq1 uncolored, adds it to the scene, and animates its colorization.
         Otherwise, uses starting_eq as eq1 (already in the desired state).
      2. Creates eq2, positions it below eq1, and fades in tokens not targeted by any grouping.
      3. Animates the transformation for each color group from eq1 to eq2.
    Returns:
      (eq1, eq2): the MathTex objects.
    """
    # 1. Use the existing eq1 if provided; otherwise, create it.
    if starting_eq is None:
        eq1 = MathTex(*eq1_tokens)
        scene.add(eq1)
        scene.wait(wait_time)
    else:
        eq1 = starting_eq

    # Animate colorizing eq1 according to eq1_groupings.
    color_anims = []
    for color, indices in eq1_groupings.items():
        for i in indices:
            color_anims.append(eq1[i].animate.set_color(color))
    scene.play(*color_anims)
    scene.wait(wait_time)

    # 2. Create eq2 and position it below eq1.
    eq2 = MathTex(*eq2_tokens)
    for color, indices in eq2_groupings.items():
        for i in indices:
            eq2[i].set_color(color)
    eq2.next_to(eq1, DOWN, buff=buff, aligned_edge=LEFT)

    # Fade in any tokens of eq2 that are not part of any grouping.
    transformed_indices = set()
    for indices in eq2_groupings.values():
        transformed_indices.update(indices)
    non_transformed_tokens = VGroup(
        *[eq2[i] for i in range(len(eq2)) if i not in transformed_indices]
    )
    if non_transformed_tokens:
        scene.play(FadeIn(non_transformed_tokens))
    scene.wait(wait_time)

    # 3. Animate the transformation for each color group in eq2 order.
    all_transforms = []
    for color, src_indices in eq1_groupings.items():
        tgt_indices = eq2_groupings.get(color, [])
        # Sort indices for left-to-right order.
        src_sorted = sorted(src_indices)
        tgt_sorted = sorted(tgt_indices)
        # If multiple source tokens must merge into one target:
        if len(tgt_sorted) == 1 and len(src_sorted) > 1:
            all_transforms.append(
                (
                    tgt_sorted[0],
                    VGroup(*[eq1[i] for i in src_sorted]),
                    eq2[tgt_sorted[0]],
                )
            )
        else:
            for i, tgt in enumerate(tgt_sorted):
                if i < len(src_sorted):
                    src = src_sorted[i]
                else:
                    src = src_sorted[-1]
                all_transforms.append((tgt, eq1[src], eq2[tgt]))
    # Sort transformations by target token index.
    all_transforms.sort(key=lambda tup: tup[0])
    for _, src_obj, tgt_obj in all_transforms:
        scene.play(ReplacementTransform(src_obj.copy(), tgt_obj))

    scene.wait(wait_time)
    return eq1, eq2


class Mul2(Scene):
    def construct(self):
        # Example: Multiply "-2 a b ⋅ 3 a^2 b" becomes "= -6 a^3 b^2"
        #
        # eq1 is described as a list of tokens.
        #   Tokens: 0:"{{-2}}", 1:"{{a}}", 2:"{{b}}", 3:"\\cdot", 4:"{{3}}", 5:"{{a}}", 6:"{{^2}}", 7:"{{b}}"
        eq1_tokens = [
            "{{-2}}",
            "{{a}}",
            "{{b}}",
            "\\cdot",
            "{{3}}",
            "{{a^2}}",
            "{{b}}",
        ]
        # Group by color for eq1:
        # Let's say blue for numbers, yellow for the "a" part (and exponent), purple for the "b" parts.
        eq1_groupings = {
            BLUE: [0, 4],  # tokens: -2 and 3
            YELLOW: [1, 5],  # tokens: a, a, and ^2
            PURPLE: [2, 6],  # tokens: b and b
        }
        # eq2 is described as tokens (including the "=" at the start).
        #   Tokens: 0:"=", 1:"{{-6}}", 2:"{{a}}", 3:"{{^3}}", 4:"{{b}}", 5:"{{^2}}"
        eq2_tokens = ["=", "{{-6}}", "{{a^3}}", "{{b^2}}"]
        # Group by color for eq2:
        eq2_groupings = {
            BLUE: [1],  # -6 (blue)
            YELLOW: [2],  # a and ^3 (yellow)
            PURPLE: [3],  # b and ^2 (purple)
        }

        eq1 = MathTex(*eq1_tokens)
        self.add(eq1)
        self.wait(1)

        animate_eq_transformation(
            self,
            eq1_tokens,
            eq1_groupings,
            eq2_tokens,
            eq2_groupings,
            buff=0.5,
            wait_time=1,
        )

        self.wait(3)


class SimpleDistrib1(Scene):
    def construct(self):
        # First transformation: eq1 --> eq2.
        eq1_tokens = [
            "{{-4a}}",  # 0
            "\cdot (",  # 1
            "{{a}}",  # 2
            "{{-2}}",  # 3
            ")",  # 4
        ]
        eq1_groupings = {YELLOW: [0], BLUE: [2], PURPLE: [3]}
        eq2_tokens = [
            "=",
            "{{(-4a)}}",  # 1
            "\cdot",  # 2
            "{{a}}",  # 3
            "{{+}}",  # 4
            "{{(-4a)}}",  # 5
            "\cdot",  # 6
            "{{(-2)}}",  # 7
        ]
        eq2_groupings = {YELLOW: [1, 5], BLUE: [3], PURPLE: [7]}
        eq1_obj, eq2_obj = animate_eq_transformation(
            self,
            eq1_tokens,
            eq1_groupings,
            eq2_tokens,
            eq2_groupings,
            buff=0.5,
            wait_time=1,
        )

        # Second transformation: use previous eq2 (as eq1) --> eq3.
        eq2_groupings = {YELLOW: [1, 2, 3], BLUE: [5, 6, 7]}
        eq3_tokens = [
            "=",
            "{{-4a^2}}",  # 1
            "{{+}}",  # 2
            "{{8a}}",  # 3
        ]
        eq3_groupings = {YELLOW: [1], BLUE: [3]}
        # Use the previous eq2_obj as the starting eq1.
        animate_eq_transformation(
            self,
            eq2_tokens,
            eq2_groupings,
            eq3_tokens,
            eq3_groupings,
            buff=0.5,
            wait_time=1,
            starting_eq=eq2_obj,
        )
        self.wait(3)


class DoubleDistrib1(Scene):
    def construct(self):
        # First transformation: eq1 --> eq2.
        eq1_tokens = [
            "(",
            "2",
            "-a",
            ")\cdot(",
            "3b",
            "+5",
            ")",
        ]
        eq1_groupings = {YELLOW: [1], BLUE: [2], PURPLE: [4], GREEN: [5]}
        eq2_tokens = [
            "=",
            "2",
            "\cdot",
            "3b",
            "+",
            "2",
            "\cdot",
            "5",
            "+",
            "(-a)",
            "\cdot",
            "3b",
            "+",
            "(-a)",
            "\cdot",
            "5",
        ]
        eq2_groupings = {YELLOW: [1, 5], BLUE: [9, 13], PURPLE: [3, 11], GREEN: [7, 15]}
        eq1_obj, eq2_obj = animate_eq_transformation(
            self,
            eq1_tokens,
            eq1_groupings,
            eq2_tokens,
            eq2_groupings,
            buff=0.5,
            wait_time=1,
        )

        # # Second transformation: use previous eq2 (as eq1) --> eq3.
        eq2_groupings = {
            YELLOW: [1, 2, 3],
            BLUE: [5, 6, 7],
            PURPLE: [9, 10, 11],
            GREEN: [13, 14, 15],
        }
        eq3_tokens = [
            "=",
            "6b",
            "+",
            "10",
            "+",
            "(-3ab)",
            "+",
            "(-5a)",
        ]
        eq3_groupings = {YELLOW: [1], BLUE: [3], PURPLE: [5], GREEN: [7]}
        # # Use the previous eq2_obj as the starting eq1.
        eq2_obj, eq3_obj = animate_eq_transformation(
            self,
            eq2_tokens,
            eq2_groupings,
            eq3_tokens,
            eq3_groupings,
            buff=0.5,
            wait_time=1,
            starting_eq=eq2_obj,
        )

        # eq3_groupings = {YELLOW: [1, 2, 3], BLUE: [5, 6, 7], PURPLE:[9,10,11], GREEN:[13,14,15]}
        eq4_tokens = [
            "=",
            "6b",
            "+",
            "10",
            "-3ab",
            "-5a",
        ]
        eq4_groupings = {PURPLE: [4], GREEN: [5]}
        # # Use the previous eq3_obj as the starting eq1.
        animate_eq_transformation(
            self,
            eq3_tokens,
            eq3_groupings,
            eq4_tokens,
            eq4_groupings,
            buff=0.5,
            wait_time=1,
            starting_eq=eq3_obj,
        )

        self.wait(3)


class Add1(Scene):
    def construct(self):
        eq1_tokens = [
            "{{b}}",  # 0
            "{{-7a}}",  # 1
            "{{+6b}}",  # 2
            "{{-2a}}",  # 3
        ]

        eq1_groupings = {YELLOW: [0, 2], BLUE: [1, 3]}

        eq2_tokens = [
            "=",
            "{{-7a}}",  # 1
            "{{-2a}}",  # 2
            "{{+ b}}",  # 3
            "{{+6b}}",  # 4
        ]

        eq2_groupings = {BLUE: [1, 2], YELLOW: [3, 4]}

        eq1_obj, eq2_obj = animate_eq_transformation(
            self,
            eq1_tokens,
            eq1_groupings,
            eq2_tokens,
            eq2_groupings,
            buff=0.5,
            wait_time=1,
        )

        eq3_tokens = [
            "=",
            "{{-9a}}",  # 1
            "{{+7b}}",  # 2
        ]

        eq3_groupings = {BLUE: [1], YELLOW: [2]}
        eq2_obj, eq3_obj = animate_eq_transformation(
            self,
            eq2_tokens,
            eq2_groupings,
            eq3_tokens,
            eq3_groupings,
            buff=0.5,
            wait_time=1,
            starting_eq=eq2_obj,
        )
        self.wait(3)
