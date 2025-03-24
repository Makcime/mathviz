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
