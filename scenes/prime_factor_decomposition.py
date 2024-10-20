from collections import defaultdict

from manim import *


class PrimeFactorDecomposition(Scene):
    def construct(self):
        # List of primes under 20
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        primes_texts = [MathTex(str(p)) for p in primes]

        # Arrange primes horizontally
        primes_group = VGroup(*primes_texts).arrange(RIGHT, buff=0.5)

        # Primes label
        primes_label = Text("Primes under 20:")
        primes_label.to_edge(UP).shift(DOWN * 0.5)

        # Position primes group
        primes_group.next_to(primes_label, DOWN, buff=0.3)

        # Add label and primes to scene
        self.play(Write(primes_label))
        self.play(Write(primes_group))

        # Vertical line
        vertical_line = Line(start=primes_group.get_bottom() + DOWN * 0.5, end=DOWN * 2)
        self.play(Create(vertical_line))

        # Number 126 at the top
        number_126 = MathTex("126")
        number_126.next_to(vertical_line.get_top() + DOWN * 0.2, LEFT)
        self.play(Write(number_126))

        # Initialize variables for the decomposition
        current_number = 126
        number_mobject = number_126
        factor_counts = defaultdict(int)
        division_equations = []
        factor_mobjects = []
        number_mobjects = [number_126]

        # Start decomposing
        while current_number != 1:
            for prime in primes:
                if current_number % prime == 0:
                    # Highlight the prime
                    prime_index = primes.index(prime)
                    prime_mobject = primes_group[prime_index]
                    rect = SurroundingRectangle(prime_mobject, color=RED)
                    self.play(Create(rect))

                    # Update factor count
                    factor_counts[prime] += 1

                    # Display factor beside current number
                    factor = MathTex(str(prime))
                    factor.next_to(number_mobject, RIGHT, buff=0.5)
                    self.play(Write(factor))
                    factor_mobjects.append(factor)

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
                        division_eq.to_edge(RIGHT).shift(UP)

                    self.play(Write(division_eq))
                    division_equations.append(division_eq)

                    # Place new number under the current one, aligned on the right
                    number_new = MathTex(f"{new_number}")
                    number_new.next_to(number_mobject, DOWN, aligned_edge=RIGHT)
                    self.play(TransformFromCopy(division_eq[-1], number_new))
                    number_mobjects.append(number_new)

                    # Update current number and mobject
                    current_number = new_number
                    number_mobject = number_new

                    # Fade out division equation and prime highlight
                    self.play(FadeOut(division_eq), FadeOut(rect))

                    break  # Break the inner loop to restart from the smallest prime
            else:
                # If no primes divide current_number, it is a prime itself
                # Highlight the prime (if within our list)
                if current_number in primes:
                    prime_index = primes.index(current_number)
                    prime_mobject = primes_group[prime_index]
                    rect = SurroundingRectangle(prime_mobject, color=RED)
                    self.play(Create(rect))

                # Update factor count
                factor_counts[current_number] += 1

                # Display factor beside current number
                factor = MathTex(str(current_number))
                factor.next_to(number_mobject, RIGHT, buff=0.5)
                self.play(Write(factor))
                factor_mobjects.append(factor)

                # Write division equation on the right
                division_eq = MathTex(f"{current_number} \\div {current_number} = 1")
                division_eq.next_to(division_equations[-1], DOWN, aligned_edge=RIGHT)
                self.play(Write(division_eq))
                division_equations.append(division_eq)

                # Place number 1 under the current number, aligned on the right
                number_new = MathTex("1")
                number_new.next_to(number_mobject, DOWN, aligned_edge=RIGHT)
                self.play(TransformFromCopy(division_eq[-1], number_new))
                number_mobjects.append(number_new)

                # Update current number and mobject
                current_number = 1
                number_mobject = number_new

                # Fade out division equation and prime highlight
                self.play(FadeOut(division_eq), FadeOut(rect))

        # Build the LaTeX string for the product of factors, isolating "3 \\times 3"
        product_string = "126 = 2 \\times {3 \\times 3} \\times 7"
        final_expression = MathTex(
            product_string, substrings_to_isolate=["3 \\times 3"]
        )
        final_expression.to_edge(DOWN, buff=1)

        # Group all factor mobjects
        factors_group = VGroup(*factor_mobjects)

        # Create a rectangle around all factors
        rect_around_factors = SurroundingRectangle(factors_group, color=BLUE)
        self.play(Create(rect_around_factors))

        # Transform factors into the final expression at the bottom
        # Position the factors copy at the location of the final expression
        factors_copy = factors_group.copy()
        factors_copy.generate_target()
        factors_copy.target.move_to(final_expression.get_center())

        # Move factors to the final expression position
        self.play(MoveToTarget(factors_copy))

        # Transform factors into the final expression
        self.play(
            TransformMatchingTex(factors_copy, final_expression),
            FadeOut(rect_around_factors),
        )

        # Continue with the rectangle around "3 × 3" and the exponentiation
        # Create a rectangle around "3 × 3" in the final expression
        three_times_three = final_expression.get_part_by_tex("3 \\times 3")
        rect_around_three_times_three = SurroundingRectangle(
            three_times_three, color=YELLOW
        )
        self.play(Create(rect_around_three_times_three))

        # Build the LaTeX string for the expression with exponents, isolating "3^{2}"
        exponent_string = "126 = 2 \\times {3^{2}} \\times 7"
        final_expression_with_powers = MathTex(
            exponent_string, substrings_to_isolate=["3^{2}"]
        )
        final_expression_with_powers.next_to(final_expression, DOWN, buff=0.3)

        # Transform the final expression to the one with exponents
        self.play(
            TransformMatchingTex(
                final_expression.copy(),
                final_expression_with_powers,
                path_alphas=[0, 1],
                transform_mismatches=True,
            ),
            FadeOut(rect_around_three_times_three),
        )

        self.wait(2)
