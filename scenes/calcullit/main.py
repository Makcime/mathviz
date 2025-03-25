import sympy
from manim import *
from sympy import expand, latex, simplify
from sympy.parsing.latex import parse_latex


def get_simplification_steps(latex_str):
    """
    Parse a LaTeX expression into a Sympy expression and return a list of steps,
    where each step is a tuple (description, LaTeX representation of the expression).
    """
    # Parse the LaTeX input into a Sympy expression.
    expr = parse_latex(latex_str)

    steps = []
    # Step 1: Original expression.
    steps.append(("Original Expression", latex(expr)))

    # Step 2: Expanded expression.
    expanded_expr = expand(expr)
    steps.append(("After Expansion", latex(expanded_expr)))

    # Step 3: Simplified expression.
    simplified_expr = simplify(expanded_expr)
    steps.append(("After Simplification", latex(simplified_expr)))

    return steps


class StepByStepScene(Scene):
    """
    A base Manim scene that takes a LaTeX input expression and displays
    its step-by-step simplification. Each step is written below the previous one.

    To use, override the INPUT_EXPRESSION class variable.
    """

    INPUT_EXPRESSION = r""  # Override this in subclasses with the desired LaTeX string.

    def construct(self):
        # Get the simplification steps as a list of (description, expression) tuples.
        steps = get_simplification_steps(self.INPUT_EXPRESSION)

        # Starting position for the first step.
        start_pos = 3 * UP
        step_objects = []

        # Create and animate each step.
        for description, expr in steps:
            step_tex = MathTex(f"{description}: {expr}")
            if not step_objects:
                # For the first step, position at the top.
                step_tex.move_to(start_pos)
            else:
                # For subsequent steps, place them below the previous one.
                step_tex.next_to(step_objects[-1], DOWN, buff=0.5)
            step_objects.append(step_tex)
            self.play(Write(step_tex))
            self.wait(1)


# ---------------------------
# Function: generate_steps_scene
# ---------------------------
def generate_steps_scene(steps_list):
    """
    Given a list of steps (each either a MathTex object or a LaTeX string),
    return a new Scene class that displays each step one below the previous one.
    """

    class CustomStepsScene(Scene):
        def construct(self):
            step_objects = []
            for step in steps_list:
                # If the step is a string, create a MathTex object; otherwise, assume it's already a MathTex.
                step_obj = MathTex(step) if isinstance(step, str) else step
                if not step_objects:
                    step_obj.to_edge(UP)
                else:
                    step_obj.next_to(step_objects[-1], DOWN, buff=0.5)
                self.play(Write(step_obj))
                step_objects.append(step_obj)
                self.wait(1)

    return CustomStepsScene


# ---------------------------
# Example usage:
# ---------------------------

# A list of test steps (as LaTeX strings).
test_steps = [
    r"Original Expression: 3a \cdot 4b \cdot 2",
    r"After Expansion: 24ab",
    r"After Simplification: 24ab",
]

# Generate a scene class using the provided steps.
CustomScene = generate_steps_scene(test_steps)

# You can now run this scene using Manim, for example:
# manim -pqh your_script.py CustomScene


# Additionally, here are separate scenes for each test expression using the StepByStepScene base class.
class SimplificationScene1(StepByStepScene):
    INPUT_EXPRESSION = r"3 a \cdot 4 b \cdot 2"


class SimplificationScene2(StepByStepScene):
    INPUT_EXPRESSION = r"h^3 - 7h^3 + 3h^3"


class SimplificationScene3(StepByStepScene):
    INPUT_EXPRESSION = r"b - 7a + 6b - 2a"


class SimplificationScene4(StepByStepScene):
    INPUT_EXPRESSION = r"3r - \left(2s - 1\right)"


class SimplificationScene5(StepByStepScene):
    INPUT_EXPRESSION = r"\left(5 - 7h\right)\left(-3\right)"


class SimplificationScene6(StepByStepScene):
    INPUT_EXPRESSION = r"\left(2 - a\right)\left(3b + 5\right)"


class MatchingEquationParts(Scene):
    def construct(self):
        variables = (
            VGroup(MathTex("a"), MathTex("b"), MathTex("c"))
            .arrange_submobjects()
            .shift(UP)
        )

        eq1 = MathTex("{{x}}^2", "+", "{{y}}^2", "=", "{{z}}^2")
        eq2 = MathTex("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2")
        eq3 = MathTex("{{a}}^2", "=", "{{c}}^2", "-", "{{b}}^2")

        self.add(eq1)
        self.wait(0.5)
        self.play(TransformMatchingTex(Group(eq1, variables), eq2))
        self.wait(0.5)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(0.5)


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
        self.wait(0.5)


class Mul2(Scene):
    def construct(self):
        # Create eq1: "-2 a b ⋅ 3 a^2 b"
        eq1 = MathTex(
            "{{-2}}",  # 0
            "{{a}}",  # 1
            "{{b}}",  # 2
            "\\cdot",  # 3
            "{{3}}",  # 4
            "{{a}}",  # 5
            "{{^2}}",  # 6
            "{{b}}",  # 7
        )

        # Color numbers blue and letters yellow.
        eq1[0].set_color(BLUE)
        eq1[4].set_color(BLUE)

        eq1[1].set_color(YELLOW)
        eq1[5].set_color(YELLOW)
        eq1[6].set_color(YELLOW)

        eq1[2].set_color(PURPLE)
        eq1[7].set_color(PURPLE)

        self.add(eq1)
        self.wait(1)

        eq2 = MathTex(
            "=",
            "{{-6}}",  # 1
            "{{a}}",  # 2
            "{{^3}}",  # 3
            "{{b}}",  # 4
            "{{^2}}",  # 5
        )

        eq2[1].set_color(BLUE)
        eq2[2:4].set_color(YELLOW)
        eq2[4:].set_color(PURPLE)

        eq2.next_to(eq1, DOWN, buff=0.5, aligned_edge=LEFT)

        numbers_group = VGroup(eq1[0], eq1[4])
        a_group = VGroup(eq1[1], eq1[5], eq1[6])
        b_group = VGroup(eq1[2], eq1[7])

        self.play(
            FadeIn(eq2[0]),  # fade in "="
            ReplacementTransform(numbers_group.copy(), eq2[1]),
            ReplacementTransform(a_group.copy(), eq2[2:4]),
            ReplacementTransform(b_group.copy(), eq2[4:]),
        )
        self.wait(1)



class SimpleDistrib1(Scene):
    def construct(self):
        eq1 = MathTex(
            "{{-4a}}",  # 0
            "\cdot (",  # 1
            "{{a}}",  # 2
            "{{-2}}",  # 3
            ")",  # 4
        )

        # Color numbers blue and letters yellow.
        eq1[0].set_color(YELLOW)
        eq1[2].set_color(BLUE)
        eq1[3].set_color(PURPLE)

        self.add(eq1)
        self.wait(1)

        eq2 = MathTex(
            "=",
            "{{(-4a)}}",  # 1
            "\cdot",  # 2
            "{{a}}",  # 3
            "{{+}}",  # 4
            "{{(-4a)}}",  # 5
            "\cdot",  # 6
            "{{(-2)}}",  # 7
        )

        # Color numbers blue and letters yellow.
        eq2[1].set_color(YELLOW)
        eq2[5].set_color(YELLOW)

        eq2[3].set_color(BLUE)

        eq2[7].set_color(PURPLE)

        eq2.next_to(eq1, DOWN, buff=0.5, aligned_edge=LEFT)

        # a_group = VGroup(eq1[1], eq1[3])
        # b_group = VGroup(eq1[0], eq1[2])

        self.play(
            ReplacementTransform(eq1[0].copy(), eq2[1]),
            ReplacementTransform(eq1[2].copy(), eq2[3]),
            ReplacementTransform(eq1[0].copy(), eq2[5]),
            ReplacementTransform(eq1[3].copy(), eq2[7]),
            FadeIn(eq2),  # fade in "="
        )
        self.wait(1)


def animate_eq_transformation(
    scene, 
    eq1_tokens, eq1_groupings, 
    eq2_tokens, eq2_groupings, 
    buff=0.5, wait_time=1,
    starting_eq=None
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
    non_transformed_tokens = VGroup(*[eq2[i] for i in range(len(eq2)) if i not in transformed_indices])
    if non_transformed_tokens:
        scene.play(FadeIn(non_transformed_tokens))
    scene.wait(wait_time)
    
    # 3. Animate the transformation for each color group.
    # for color, src_indices in eq1_groupings.items():
    #     tgt_indices = eq2_groupings.get(color, [])
    #     if len(src_indices) >= len(tgt_indices):
    #         group1 = VGroup(*[eq1[i] for i in src_indices])
    #         group2 = VGroup(*[eq2[i] for i in tgt_indices])
    #         scene.play(ReplacementTransform(group1.copy(), group2))
    #     elif len(src_indices) == 1 and len(tgt_indices) > 1:
    #         for tgt in tgt_indices:
    #             scene.play(ReplacementTransform(eq1[src_indices[0]].copy(), eq2[tgt]))
    #     else:
    #         for i in range(min(len(src_indices), len(tgt_indices))):
    #             scene.play(ReplacementTransform(eq1[src_indices[i]].copy(), eq2[tgt_indices[i]]))

    # 4. Animate the transformation for each color group in eq2 order.
    all_transforms = []
    for color, src_indices in eq1_groupings.items():
        tgt_indices = eq2_groupings.get(color, [])
        # Sort indices for left-to-right order.
        src_sorted = sorted(src_indices)
        tgt_sorted = sorted(tgt_indices)
        # If multiple source tokens must merge into one target:
        if len(tgt_sorted) == 1 and len(src_sorted) > 1:
            all_transforms.append((tgt_sorted[0], VGroup(*[eq1[i] for i in src_sorted]), eq2[tgt_sorted[0]]))
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


class Mul3(Scene):
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


class SimpleDistrib2(Scene):
    def construct(self):
        # First transformation: eq1 --> eq2.
        eq1_tokens = [
            "{{-4a}}",  # 0
            "\cdot (",   # 1
            "{{a}}",    # 2
            "{{-2}}",   # 3
            ")"         # 4
        ]
        eq1_groupings = {YELLOW: [0], BLUE: [2], PURPLE: [3]}
        eq2_tokens = [
            "=",
            "{{(-4a)}}",  # 1
            "\cdot",       # 2
            "{{a}}",      # 3
            "{{+}}",      # 4
            "{{(-4a)}}",  # 5
            "\cdot",       # 6
            "{{(-2)}}",   # 7
        ]
        eq2_groupings = {YELLOW: [1, 5], BLUE: [3], PURPLE: [7]}
        eq1_obj, eq2_obj = animate_eq_transformation(
            self, eq1_tokens, eq1_groupings,
            eq2_tokens, eq2_groupings,
            buff=0.5, wait_time=1
        )

        # Second transformation: use previous eq2 (as eq1) --> eq3.
        eq2_groupings = {YELLOW: [1, 2, 3], BLUE: [5, 6, 7]}
        eq3_tokens = [
            "=",
            "{{-4a^2}}",  # 1
            "{{+}}",       # 2
            "{{8a}}",    # 3
        ]
        eq3_groupings = {YELLOW: [1], BLUE: [3]}
        # Use the previous eq2_obj as the starting eq1.
        animate_eq_transformation(
            self, eq2_tokens, eq2_groupings,
            eq3_tokens, eq3_groupings,
            buff=0.5, wait_time=1,
            starting_eq=eq2_obj
        )

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
        eq1_groupings = {YELLOW: [1], BLUE: [2], PURPLE: [4], GREEN:[5]}
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
            "5"
        ]
        eq2_groupings = {YELLOW: [1, 5], BLUE: [9,13], PURPLE: [3,11], GREEN:[7,15]}
        eq1_obj, eq2_obj = animate_eq_transformation(
            self, eq1_tokens, eq1_groupings,
            eq2_tokens, eq2_groupings,
            buff=0.5, wait_time=1
        )

        # # Second transformation: use previous eq2 (as eq1) --> eq3.
        eq2_groupings = {YELLOW: [1, 2, 3], BLUE: [5, 6, 7], PURPLE:[9,10,11], GREEN:[13,14,15]}
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
        eq3_groupings = {YELLOW: [1], BLUE: [3], PURPLE:[5], GREEN:[7]}
        # # Use the previous eq2_obj as the starting eq1.
        eq2_obj, eq3_obj = animate_eq_transformation(
            self, eq2_tokens, eq2_groupings,
            eq3_tokens, eq3_groupings,
            buff=0.5, wait_time=1,
            starting_eq=eq2_obj
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
        eq4_groupings = {PURPLE:[4], GREEN:[5]}
        # # Use the previous eq3_obj as the starting eq1.
        animate_eq_transformation(
            self, eq3_tokens, eq3_groupings,
            eq4_tokens, eq4_groupings,
            buff=0.5, wait_time=1,
            starting_eq=eq3_obj
        )


class Add1(Scene):
    def construct(self):
        eq1_tokens = [
            "{{b}}",  # 0
            "{{-7a}}",  # 1
            "{{+6b}}",  # 2
            "{{-2a}}",  # 3
        ]

        eq1_groupings = {YELLOW: [0, 2], BLUE: [1,3]}

        eq2_tokens = [
            "=",
            "{{-7a}}",  # 1
            "{{-2a}}",  # 2
            "{{+ b}}",  # 3
            "{{+6b}}",  # 4
        ]

        eq2_groupings = {BLUE: [1, 2], YELLOW: [3,4]}

        eq1_obj, eq2_obj = animate_eq_transformation(
            self, eq1_tokens, eq1_groupings,
            eq2_tokens, eq2_groupings,
            buff=0.5, wait_time=1
        )

        eq3_tokens = [
            "=",
            "{{-9a}}",  # 1
            "{{+7b}}",  # 2
        ]

        eq3_groupings = {BLUE: [1], YELLOW: [2]}
        eq2_obj, eq3_obj = animate_eq_transformation(
            self, eq2_tokens, eq2_groupings,
            eq3_tokens, eq3_groupings,
            buff=0.5, wait_time=1,
            starting_eq=eq2_obj
        )

        # # Color numbers blue and letters yellow.
        # eq3[2].set_color(BLUE)
        # eq3[1].set_color(YELLOW)
        #
        # eq3.next_to(eq2, DOWN, buff=0.5, aligned_edge=LEFT)
        #
        # a_group = VGroup(eq2[1], eq2[2])
        # b_group = VGroup(eq2[3], eq2[4])
        #
        # self.play(
        #     FadeIn(eq3[0]),  # fade in "="
        #     ReplacementTransform(a_group.copy(), eq3[1]),
        #     ReplacementTransform(b_group.copy(), eq3[2]),
        # )
        self.wait(1)

