from collections import defaultdict

from manim import *


class PrimeFactorDecomposition(Scene):
    def construct(self):
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
        group_126 = self.decompose_number(126, LEFT * 4.8)

        # Pause before starting the next decomposition
        self.wait(1)

        # Decompose 120
        group_120 = self.decompose_number(120, RIGHT * 4)

        self.wait(2)
        # Optionally, you can adjust the positions or add more numbers

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
        for prime, count in sorted(factor_counts.items()):
            if count == 1:
                factor_strings.append(f"{prime}")
            else:
                factor_strings.extend([f"{prime}"] * count)
        product_string = f"{number} = " + " \\times ".join(factor_strings)
        final_expression = MathTex(product_string)
        final_expression.to_edge(DOWN, buff=1)  # .shift(LEFT * 1.5)

        self.play(FadeTransform(expression, final_expression))
        decomposition_group.add(final_expression)

        # Transform factors into the final expression at the bottom
        self.play(FadeOut(rect_around_factors))

        # Build the LaTeX string for the expression with exponents
        exponent_strings = []
        for prime, count in sorted(factor_counts.items()):
            if count == 1:
                exponent_strings.append(f"{prime}")
            else:
                exponent_strings.append(f"{prime}^{{{count}}}")
        exponent_string = f"{number} = " + " \\times ".join(exponent_strings)
        final_expression_with_powers = MathTex(exponent_string)
        final_expression_with_powers.next_to(final_expression, DOWN, buff=0.3)
        decomposition_group.add(final_expression_with_powers)

        # Transform the final expression to the one with exponents
        self.play(
            TransformMatchingTex(final_expression.copy(), final_expression_with_powers)
        )

        self.wait(1)

        # Shift the entire decomposition group
        self.play(decomposition_group.animate.shift(shift_amount))

        return decomposition_group
