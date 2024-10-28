from collections import defaultdict

from manim import *


class PrimeFactorDecomposition(Scene):
    def construct(self):
        self.next_section()
        # List of primes under 20
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19]
        primes_texts = [MathTex(str(p)) for p in self.primes]

        # Arrange primes horizontally
        self.primes_group = VGroup(*primes_texts).arrange(RIGHT, buff=0.5)

        # Primes label
        self.primes_label = Text("Nombres premiers < 20:")
        self.primes_label.to_edge(UP).shift(DOWN * 0.5)

        # Position primes group
        self.primes_group.next_to(self.primes_label, DOWN, buff=0.3)

        # Add label and primes to scene
        self.play(Write(self.primes_label))
        self.play(Write(self.primes_group))

        # Decompose 126 and move it to the left
        self.next_section()
        group_126, exp_126 = self.decompose_number(126, LEFT * 4.8)

        # Pause before starting the next decomposition
        self.wait(1)

        # Decompose 120
        self.next_section()
        group_120, exp_120 = self.decompose_number(120, RIGHT * 4)

        self.wait(2)
        # Optionally, you can adjust the positions or add more numbers

        # Add label and primes to scene
        self.play(FadeOut(self.primes_label, self.primes_group))

        self.wait(2)

        self.next_section()
        # print("exp 120 : ", exp_120)
        # twos = exp_120.get_part_by_tex("2^{3} ")
        # rect_around_fact = SurroundingRectangle(twos, color=YELLOW)
        # self.play(Create(rect_around_fact))

        # Get the "2" parts in exp_126 and exp_120
        twos_126 = exp_126.get_parts_by_tex("2")
        twos_120 = exp_120.get_parts_by_tex("2^{3}")

        # Create rectangles around them
        rect_126 = SurroundingRectangle(twos_126, color=YELLOW)
        rect_120 = SurroundingRectangle(twos_120, color=YELLOW)

        # Play the animations to create the rectangles simultaneously
        self.play(Create(rect_126), Create(rect_120))

        self.wait(2)

    def decompose_number(self, number, shift_amount):
        # Create a group to hold all elements related to this decomposition
        decomposition_group = VGroup()

        # Vertical line
        vertical_line = Line(
            start=self.primes_group.get_bottom() + DOWN * 0.5, end=DOWN * 2
        )

        # Number at the top
        number_tex = MathTex(str(number))
        number_tex.next_to(vertical_line.get_top() + DOWN * 0.2, LEFT)

        # Add vertical line and number to the group and scene
        self.play(Create(vertical_line))
        self.play(Write(number_tex))
        decomposition_group.add(vertical_line, number_tex)

        # Initialize variables for the decomposition
        current_number = number
        number_mobject = number_tex
        factor_counts = defaultdict(int)
        division_equations = []
        factor_mobjects = []
        number_mobjects = [number_tex]

        # Start decomposing
        while current_number != 1:
            for prime in self.primes:
                if current_number % prime == 0:
                    # Highlight the prime
                    prime_index = self.primes.index(prime)
                    prime_mobject = self.primes_group[prime_index]
                    rect = SurroundingRectangle(prime_mobject, color=RED)
                    self.play(Create(rect))

                    # Update factor count
                    factor_counts[prime] += 1

                    # Display factor beside current number
                    factor = MathTex(str(prime))
                    factor.next_to(number_mobject, RIGHT, buff=0.5)
                    self.play(Write(factor))
                    factor_mobjects.append(factor)
                    decomposition_group.add(factor)

                    # Write division equation on the right
                    new_number = current_number // prime
                    division_eq = MathTex(
                        f"{current_number} \\div {prime} = {new_number}"
                    )
                    if division_equations:
                        division_eq.next_to(
                            division_equations[-1], DOWN, aligned_edge=RIGHT
                        )
                    else:
                        division_eq.to_edge(RIGHT).shift(UP).shift(LEFT * 2)
                    self.play(Write(division_eq))
                    division_equations.append(division_eq)
                    # decomposition_group.add(division_eq)

                    # Place new number under the current one, aligned on the right
                    number_new = MathTex(f"{new_number}")
                    number_new.next_to(number_mobject, DOWN, aligned_edge=RIGHT)
                    self.play(TransformFromCopy(division_eq[-1], number_new))
                    number_mobjects.append(number_new)
                    decomposition_group.add(number_new)

                    # Update current number and mobject
                    current_number = new_number
                    number_mobject = number_new

                    # Fade out division equation and prime highlight
                    self.play(FadeOut(division_eq), FadeOut(rect))

                    break  # Break the inner loop to restart from the smallest prime
            else:
                # If no primes divide current_number, it is a prime itself
                # Highlight the prime (if within our list)
                if current_number in self.primes:
                    prime_index = self.primes.index(current_number)
                    prime_mobject = self.primes_group[prime_index]
                    rect = SurroundingRectangle(prime_mobject, color=RED)
                    self.play(Create(rect))
                else:
                    rect = None

                # Update factor count
                factor_counts[current_number] += 1

                # Display factor beside current number
                factor = MathTex(str(current_number))
                factor.next_to(number_mobject, RIGHT, buff=0.5)
                self.play(Write(factor))
                factor_mobjects.append(factor)
                decomposition_group.add(factor)

                # Write division equation on the right
                division_eq = MathTex(f"{current_number} \\div {current_number} = 1")
                division_eq.next_to(division_equations[-1], DOWN, aligned_edge=RIGHT)
                self.play(Write(division_eq))
                division_equations.append(division_eq)
                # decomposition_group.add(division_eq)

                # Place number 1 under the current number, aligned on the right
                number_new = MathTex("1")
                number_new.next_to(number_mobject, DOWN, aligned_edge=RIGHT)
                self.play(TransformFromCopy(division_eq[-1], number_new))
                number_mobjects.append(number_new)
                decomposition_group.add(number_new)

                # Update current number and mobject
                current_number = 1
                number_mobject = number_new

                # Fade out division equation and prime highlight
                self.play(FadeOut(division_eq))
                if rect:
                    self.play(FadeOut(rect))

        # Group all factor mobjects
        factors_group = VGroup(*factor_mobjects)
        decomposition_group.add(factors_group)

        # Create a rectangle around all factors
        rect_around_factors = SurroundingRectangle(factors_group, color=BLUE)
        self.play(Create(rect_around_factors))
        # decomposition_group.add(rect_around_factors)

        # Build the initial expression "{number} ="
        initial_expression = MathTex(str(number), "=")
        initial_expression.to_edge(DOWN, buff=1).shift(LEFT * 1.5)
        self.play(Write(initial_expression))
        # decomposition_group.add(initial_expression)

        # Initialize the expression VGroup with the initial expression
        expression = VGroup(*initial_expression)

        # For alignment, we can extract the "=" symbol
        equals = initial_expression[1]

        # Iterate over each factor and animate them one by one
        for idx, factor in enumerate(factor_mobjects):
            # Copy the factor to animate
            factor_copy = factor.copy()

            # Determine the positions
            # Get the last element in the expression to position the times symbol
            last_element = expression[-1]

            # Create the multiplication symbol (except for the first factor)
            if idx == 0:
                # No multiplication symbol before the first factor
                times = None
            else:
                times = MathTex("\\times")
                times.next_to(last_element, RIGHT, buff=0.2)
                self.play(Write(times))
                expression.add(times)
                # decomposition_group.add(times)

            # Position the factor copy next to the last element
            if times:
                factor_copy.next_to(times, RIGHT, buff=0.2)
            else:
                factor_copy.next_to(equals, RIGHT, buff=0.2)

            # Animate the factor moving down to its position
            self.play(TransformFromCopy(factor, factor_copy))

            # Add the factor to the expression VGroup
            expression.add(factor_copy)
            # decomposition_group.add(factor_copy)

        # Build the LaTeX string for the product of factors, isolating repeated factors
        factor_strings = []
        isolated_factors = []
        for prime, count in sorted(factor_counts.items()):
            if count == 1:
                factor_strings.append(f"{prime}")
            else:
                factors = [f"{prime}"] * count
                # Join repeated factors with \times and enclose in braces
                repeated_factors = " \\times ".join(factors)
                factor_strings.append(f"{{{{{repeated_factors}}}}}")
                isolated_factors.append(repeated_factors)
        product_string = f"{number} = " + " \\times ".join(factor_strings)

        # Build the final expression, isolating repeated factors
        final_expression = MathTex(
            product_string  # , substrings_to_isolate=isolated_factors
        )
        final_expression.to_edge(DOWN, buff=1)
        final_expression.move_to(expression.get_center())
        self.play(FadeTransform(expression, final_expression))
        decomposition_group.add(final_expression)

        # Transform factors into the final expression at the bottom
        self.play(FadeOut(rect_around_factors))

        # If there are repeated factors, create rectangle and perform exponentiation
        if isolated_factors:
            # Handle the first set of repeated factors (for simplicity)
            repeated_factors_tex = isolated_factors[0]
            # Create a rectangle around the repeated factors in the final expression
            repeated_factors_mobject = final_expression.get_part_by_tex(
                repeated_factors_tex
            )
            rect_around_repeated = SurroundingRectangle(
                repeated_factors_mobject, color=YELLOW
            )
            self.play(Create(rect_around_repeated))
            # decomposition_group.add(rect_around_repeated)

            # Build the LaTeX string for the expression with exponents
            exponent_strings = []
            ssrt_to_iso = ""
            for prime, count in sorted(factor_counts.items()):
                if count == 1:
                    exponent_strings.append(f"{prime}")
                else:
                    ssrt_to_iso = f"{{{{{prime}^{{{count}}} }}}}"
                    exponent_strings.append(ssrt_to_iso)
            exponent_string = f"{number} = " + " \\times ".join(exponent_strings)

            final_expression_with_powers = MathTex(
                exponent_string,
                # substrings_to_isolate=ssrt_to_iso,
            )
            final_expression_with_powers.next_to(final_expression, DOWN, buff=0.3)
            decomposition_group.add(final_expression_with_powers)

            # Transform the final expression to the one with exponents
            print(exponent_string, product_string)
            self.play(
                TransformMatchingTex(
                    final_expression.copy(),
                    final_expression_with_powers,
                    path_alphas=[0, 1],
                    transform_mismatches=True,
                    # fade_transform_mismatches=True,
                ),
                FadeOut(rect_around_repeated),
            )
        else:
            # No repeated factors, so no need for rectangle or exponentiation
            final_expression_with_powers = final_expression

        self.wait(1)

        # Shift the entire decomposition group
        self.play(decomposition_group.animate.shift(shift_amount))

        return decomposition_group, final_expression_with_powers


class PGCD(Scene):
    def construct(self):
        # Create the mathematical expression with double braces

        intro = Tex(
            r"Voici la décomposition en facteurs premiers \\ de 120 et 126 :",
            tex_template=TexFontTemplates.french_cursive,
        )
        # self.play(Write(intro))

        decomp_120 = MathTex(
            "120 = {{ 2^{3} }} \\times {{ 3 }} \\times {{ 5 }} {{ }}",
            tex_template=TexFontTemplates.french_cursive,
            # font_size=144,
        )
        decomp_120_ = MathTex(
            "120 = {{ 2^{3} }} \\times {{ 3^{1} }} \\times {{ 5^{1} }} \\times {{7^{0} }}",
            tex_template=TexFontTemplates.french_cursive,
            # font_size=144,
        )

        decomp_120.next_to(intro, DOWN)
        decomp_120_.align_to(decomp_120, LEFT)
        decomp_120_.align_to(decomp_120, UP)

        decomp_126 = MathTex(
            "126 = {{ 2 }} \\times {{ 3^{2} }} {{ }} \\times {{7}}",
            tex_template=TexFontTemplates.french_cursive,
            # font_size=144,
        )

        decomp_126_ = MathTex(
            "126 = {{ 2^{1} }} \\times {{3^{2} }} \\times {{5^{0} }} \\times {{ 7^{1}}}",
            tex_template=TexFontTemplates.french_cursive,
            # font_size=144,
        )

        decomp_126.next_to(decomp_120, DOWN, aligned_edge=LEFT)
        decomp_126_.align_to(decomp_126, LEFT)
        decomp_126_.align_to(decomp_126, UP)

        self.play(Write(decomp_120), Write(decomp_126))

        self.play(TransformMatchingTex(decomp_120, decomp_120_))
        self.wait(2)
        self.play(TransformMatchingTex(decomp_126, decomp_126_))
        self.wait(2)

        # Animate changing the color of "2^{3}" to blue
        self.play(
            decomp_120_[1].animate.set_color(RED),
            decomp_126_[1].animate.set_color(GREEN),
        )
        self.play(
            decomp_120_[3].animate.set_color(GREEN),
            decomp_126_[3].animate.set_color(RED),
        )
        self.play(
            decomp_120_[5].animate.set_color(RED),
            decomp_126_[5].animate.set_color(GREEN),
        )
        self.play(
            decomp_120_[7].animate.set_color(GREEN),
            decomp_126_[7].animate.set_color(RED),
        )
        self.wait(2)

        PGCD = MathTex(
            "PGCD(120, 126) = {{ 2^{1} }} \\times {{3^{1} }} \\times {{5^{0} }} \\times {{ 7^{0}}}",
            tex_template=TexFontTemplates.french_cursive,
            # font_size=144,
        )

        PGCD.next_to(decomp_126_, DOWN, buff=1.5)

        self.play(TransformMatchingTex(decomp_126, decomp_126_))
