from manim import *
from collections import defaultdict

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
        vertical_line = Line(
            start=primes_group.get_bottom() + DOWN * 0.5,
            end=DOWN * 3
        )
        self.play(Create(vertical_line))

        # Number 126 at the top
        number_126 = MathTex("126")
        number_126.next_to(vertical_line.get_top(), LEFT)
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

                    # Display factor beside current number (shifted right)
                    factor = MathTex(str(prime))
                    factor.next_to(number_mobject, RIGHT, buff=0.5)
                    # factor.shift(RIGHT * 0.5)
                    self.play(Write(factor))
                    factor_mobjects.append(factor)

                    # Write division equation on the right
                    new_number = current_number // prime
                    division_eq = MathTex(f"{current_number} \\div {prime} = {new_number}")
                    if division_equations:
                        division_eq.next_to(division_equations[-1], DOWN, aligned_edge=RIGHT)
                    else:
                        division_eq.to_edge(RIGHT).shift(UP)
                    self.play(Write(division_eq))
                    division_equations.append(division_eq)

                    # Place new number under the current one, aligned on the right
                    number_new = MathTex(f"{new_number}")
                    number_new.next_to(number_mobject, DOWN, aligned_edge=RIGHT)
                    self.play(
                        TransformFromCopy(division_eq[-1], number_new)
                    )
                    number_mobjects.append(number_new)

                    # Update current number and mobject
                    current_number = new_number
                    number_mobject = number_new

                    # Fade out division equation and prime highlight
                    self.play(
                        FadeOut(division_eq),
                        FadeOut(rect)
                    )

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

                # Display factor beside current number (shifted right)
                factor = MathTex(str(current_number))
                factor.next_to(number_mobject, RIGHT, buff=0.5)
                factor.shift(RIGHT * 0.5)
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
                self.play(
                    TransformFromCopy(division_eq[-1], number_new)
                )
                number_mobjects.append(number_new)

                # Update current number and mobject
                current_number = 1
                number_mobject = number_new

                # Fade out division equation and prime highlight
                self.play(
                    FadeOut(division_eq),
                    FadeOut(rect)
                )

        # After the decomposition loop
        # print(factor_counts)  # Debugging

        # Build the LaTeX string for the product of factors
        factor_texts = [factor.get_tex_string() for factor in factor_mobjects]
        product_string = " \\times ".join(factor_texts)
        final_expression = MathTex(f"126 = {product_string}")
        final_expression.to_edge(DOWN, buff=1)  # Move up from bottom edge
        self.play(Write(final_expression))

        # Build the LaTeX string for the expression with exponents
        exponent_strings = []
        for prime in sorted(factor_counts.keys()):
            count = factor_counts[prime]
            if count == 1:
                exponent_strings.append(f"{prime}")
            else:
                exponent_strings.append(f"{prime}^{{{count}}}")

        exponent_string = " \\times ".join(exponent_strings)
        final_expression_with_powers = MathTex(f"126 = {exponent_string}")

        # Position the final expression with powers below the previous final expression
        final_expression_with_powers.next_to(final_expression, DOWN, buff=0.3)

        self.play(Write(final_expression_with_powers))
        self.wait(2)  # Pause to see the final expressions
