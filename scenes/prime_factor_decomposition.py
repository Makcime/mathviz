from collections import defaultdict

import sympy
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
        # Decomposition of 120 with exponents
        decomp_120 = MathTex(
            "120 =",
            "{ 2^{3} }",
            "\\times",
            "{ 3 }",
            "\\times",
            "{ 5 }",
            "\\times",
            "{ }",
        )

        decomp_120_ = MathTex(
            "120 =",
            "{ 2^{3} }",
            "\\times",
            "{ 3^{1} }",
            "\\times",
            "{ 5^{1} }",
            "\\times",
            "{ 7^{0} }",
        )
        # decomp_120.next_to(intro, DOWN)

        # Decomposition of 126 with exponents
        decomp_126 = MathTex(
            "126 =",
            "{ 2 }",
            "\\times",
            "{ 3^{2} }",
            "{ }",
            "{ }",
            "\\times",
            "{ 7 }",
        )
        decomp_126_ = MathTex(
            "126 =",
            "{ 2^{1} }",
            "\\times",
            "{ 3^{2} }",
            "\\times",
            "{ 5^{0} }",
            "\\times",
            "{ 7^{1} }",
        )

        decomp_120.to_edge(UP).shift(DOWN * 0.5)
        decomp_120_.align_to(decomp_120, LEFT)
        decomp_120_.align_to(decomp_120, UP)

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
            decomp_120_[1].animate.set_color(GREEN),
            decomp_126_[1].animate.set_color(RED),
        )
        self.play(
            decomp_120_[3].animate.set_color(RED),
            decomp_126_[3].animate.set_color(GREEN),
        )
        self.play(
            decomp_120_[5].animate.set_color(GREEN),
            decomp_126_[5].animate.set_color(RED),
        )
        self.play(
            decomp_120_[7].animate.set_color(RED),
            decomp_126_[7].animate.set_color(GREEN),
        )

        self.wait(1)

        # Create the PGCD expression with terms as separate submobjects
        PGCD = MathTex(
            "PGCD(120, 126) =",
            "{ 2^{1} }",
            "\\times",
            "{ 3^{1} }",
            "\\times",
            "{ 5^{0} }",
            "\\times",
            "{ 7^{0} }",
            # tex_template=TexFontTemplates.french_cursive,
        )
        # PGCD[0].next_to(decomp_126[0], DOWN, aligned_edge=RIGHT)
        # for i in range(1, 8):
        #     PGCD[i].next_to(PGCD[i - 1], RIGHT)
        PGCD.next_to(decomp_126_, DOWN, buff=1, aligned_edge=RIGHT)

        # Set the terms to be invisible initially
        for index in [1, 3, 5, 7]:
            PGCD[index].set_opacity(0)

        # Write the PGCD label and multiplication signs
        self.play(Write(PGCD[0]))  # "PGCD(120, 126) ="
        self.play(
            FadeIn(PGCD[2]),  # "\\times"
            FadeIn(PGCD[4]),
            FadeIn(PGCD[6]),
        )
        self.wait(1)

        # Set the PGCD terms to full opacity and color them red
        for index in [1, 3, 5, 7]:

            PGCD[index].set_color(RED)
            source = decomp_120_
            if index in [1, 5]:
                source = decomp_126_
            self.play(
                ReplacementTransform(source[index].copy(), PGCD[index]),
                PGCD[index].animate.set_opacity(1),
            )

        self.wait(2)

        PGCD_final = MathTex(r"= 2 \times 3 = 6")
        PGCD_final.next_to(PGCD, DOWN).align_to(PGCD[1], LEFT).shift(LEFT * 0.5)

        self.play(Write(PGCD_final))

        # Create the PGCD expression with terms as separate submobjects
        PPCM = MathTex(
            "PPCM(120, 126) =",
            "{ 2^{3} }",
            "\\times",
            "{ 3^{2} }",
            "\\times",
            "{ 5^{1} }",
            "\\times",
            "{ 7^{1} }",
            # tex_template=TexFontTemplates.french_cursive,
        )
        # PGCD[0].next_to(decomp_126[0], DOWN, aligned_edge=RIGHT)
        # for i in range(1, 8):
        #     PGCD[i].next_to(PGCD[i - 1], RIGHT)
        PPCM.next_to(PGCD_final, DOWN).align_to(PGCD, LEFT)

        # Set the terms to be invisible initially
        for index in [1, 3, 5, 7]:
            PPCM[index].set_opacity(0)

        # Write the PGCD label and multiplication signs
        self.play(Write(PPCM[0]))  # "PPCM(120, 126) ="
        self.play(
            FadeIn(PPCM[2]),  # "\\times"
            FadeIn(PPCM[4]),
            FadeIn(PPCM[6]),
        )
        self.wait(1)

        # Set the PPCM terms to full opacity and color them red
        for index in [1, 3, 5, 7]:

            PPCM[index].set_color(GREEN)
            source = decomp_126_
            if index in [1, 5]:
                source = decomp_120_
            self.play(
                ReplacementTransform(source[index].copy(), PPCM[index]),
                PPCM[index].animate.set_opacity(1),
            )

        self.wait(2)

        PPCM_final = MathTex(
            "=",
            "{ 2^{3} }",
            "\\times",
            "{ 3^{2} }",
            "\\times",
            "{ 5 }",
            "\\times",
            "{ 7 }",
            "= 2520",
            # tex_template=TexFontTemplates.french_cursive,
        )
        PPCM_final.next_to(PPCM, DOWN).align_to(PPCM[1], LEFT).shift(LEFT * 0.5)
        self.play(Write(PPCM_final))

        self.wait(2)


class GCDLCMScene(Scene):
    def construct(self):
        # Define the two numbers (you can change these to any integers)
        num1 = 120
        num2 = 126

        # Compute the prime factorizations using sympy
        factors1 = sympy.factorint(num1)
        factors2 = sympy.factorint(num2)

        # Get the set of all primes involved
        primes = sorted(set(factors1.keys()).union(factors2.keys()))

        # Build the exponents lists for both numbers
        exponents1 = [factors1.get(p, 0) for p in primes]
        exponents2 = [factors2.get(p, 0) for p in primes]

        # Compute GCD and LCM exponents
        gcd_exponents = [min(e1, e2) for e1, e2 in zip(exponents1, exponents2)]
        lcm_exponents = [max(e1, e2) for e1, e2 in zip(exponents1, exponents2)]

        # Compute GCD and LCM numerical values
        gcd_value = sympy.gcd(num1, num2)
        lcm_value = sympy.lcm(num1, num2)

        # Function to get factor parts with exponents as separate submobjects
        def get_factor_parts(p, e):
            if e == 0:
                return [f"{p}", "^", "{{", "0", "}}"]
            elif e == 1:
                return [f"{p}"]
            else:
                return [f"{p}", "^", "{{", f"{e}", "}}"]

        # Build the MathTex expressions and record exponent indices
        def build_decomposition(num, exponents, other_exponents):
            decomp_tex = [f"{num}", "="]
            exponent_indices = {}
            current_index = 2  # Start after number and '='

            for idx, p in enumerate(primes):
                e = exponents[idx]
                oe = other_exponents[idx]
                factor_parts = get_factor_parts(p, e)
                decomp_tex.extend(factor_parts)

                # Determine the index of the exponent in decomp_tex
                if e != 1:
                    # Exponent exists
                    exponent_global_index = current_index + factor_parts.index("{{") + 1
                    exponent_indices[p] = (exponent_global_index, e, oe)
                current_index += len(factor_parts)

                # Add multiplication sign if not the last prime
                if idx < len(primes) - 1:
                    decomp_tex.append("\\times")
                    current_index += 1

            return decomp_tex, exponent_indices

        # Build decompositions for num1 and num2
        decomp1_tex, decomp1_exp_indices = build_decomposition(
            num1, exponents1, exponents2
        )
        decomp2_tex, decomp2_exp_indices = build_decomposition(
            num2, exponents2, exponents1
        )

        # Create MathTex objects
        decomp1 = MathTex(*decomp1_tex)
        decomp1.to_edge(UP)
        decomp2 = MathTex(*decomp2_tex)
        decomp2.next_to(decomp1, DOWN, aligned_edge=LEFT)

        # Write the decompositions on the screen
        self.play(Write(decomp1), Write(decomp2))
        self.wait(1)

        # Color the exponents: RED for smaller, GREEN for larger
        # For decomp1
        for p in primes:
            if p in decomp1_exp_indices:
                exp_idx, e1, e2 = decomp1_exp_indices[p]
                if e1 > e2:
                    color = GREEN
                elif e1 < e2:
                    color = RED
                else:
                    color = RED  # Equal exponents, color both RED
                decomp1[exp_idx].set_color(color)

        # For decomp2
        for p in primes:
            if p in decomp2_exp_indices:
                exp_idx, e2, e1 = decomp2_exp_indices[p]
                if e2 > e1:
                    color = GREEN
                elif e2 < e1:
                    color = RED
                else:
                    color = RED
                decomp2[exp_idx].set_color(color)

        self.wait(1)

        # Create the GCD expression
        def build_result_expression(label, exponents):
            result_tex = [label]
            exponent_indices = {}
            current_index = 1  # Start after label

            for idx, p in enumerate(primes):
                e = exponents[idx]
                factor_parts = get_factor_parts(p, e)
                result_tex.extend(factor_parts)

                # Record exponent indices
                if e != 1:
                    exponent_global_index = current_index + factor_parts.index("{{") + 1
                    exponent_indices[p] = (exponent_global_index, e)
                current_index += len(factor_parts)

                # Add multiplication sign if not the last prime
                if idx < len(primes) - 1:
                    result_tex.append("\\times")
                    current_index += 1

            return result_tex, exponent_indices

        # Build GCD expression
        gcd_label = f"\\text{{GCD}}({num1}, {num2}) ="
        gcd_tex, gcd_exp_indices = build_result_expression(gcd_label, gcd_exponents)
        gcd_expr = MathTex(*gcd_tex)
        gcd_expr.next_to(decomp2, DOWN, aligned_edge=LEFT)

        # Set the exponents to be invisible initially
        for p in primes:
            if p in gcd_exp_indices:
                idx, e = gcd_exp_indices[p]
                gcd_expr[idx].set_opacity(0)

        # Write the GCD label and multiplication signs
        self.play(Write(gcd_expr[0]))  # "GCD(num1, num2) ="
        for mob in gcd_expr[1:]:
            if hasattr(mob, "tex_string") and mob.tex_string == "\\times":
                self.play(FadeIn(mob))

        self.wait(1)

        # Animate the exponents transforming into the GCD terms
        for p in primes:
            e = factors1.get(p, 0)
            e2 = factors2.get(p, 0)
            gcd_e = min(e, e2)
            if gcd_e > 0:
                # Determine source exponent (smaller exponent, colored RED)
                if e <= e2:
                    source_expr = decomp1
                    source_exp_indices = decomp1_exp_indices
                else:
                    source_expr = decomp2
                    source_exp_indices = decomp2_exp_indices

                # Only proceed if exponent exists in source expression
                if p in source_exp_indices:
                    source_exp_idx = source_exp_indices[p][0]
                else:
                    continue  # Exponent is 1; no exponent submobject to animate

                # Target exponent in GCD expression
                target_exp_idx = gcd_exp_indices[p][0]

                # Animate transformation
                self.play(
                    ReplacementTransform(
                        source_expr[source_exp_idx].copy(),
                        gcd_expr[target_exp_idx].set_opacity(1).set_color(RED),
                    )
                )

        self.wait(1)

        # Simplify the GCD to its numerical value
        gcd_value_tex = f"= {gcd_value}"
        gcd_value_expr = MathTex(gcd_value_tex)
        gcd_value_expr.next_to(gcd_expr, RIGHT)
        self.play(Write(gcd_value_expr))
        self.wait(1)

        # Build LCM expression
        lcm_label = f"\\text{{LCM}}({num1}, {num2}) ="
        lcm_tex, lcm_exp_indices = build_result_expression(lcm_label, lcm_exponents)
        lcm_expr = MathTex(*lcm_tex)
        lcm_expr.next_to(gcd_expr, DOWN, aligned_edge=LEFT)

        # Set the exponents to be invisible initially
        for p in primes:
            if p in lcm_exp_indices:
                idx, e = lcm_exp_indices[p]
                lcm_expr[idx].set_opacity(0)

        # Write the LCM label and multiplication signs
        self.play(Write(lcm_expr[0]))  # "LCM(num1, num2) ="
        for mob in lcm_expr[1:]:
            if hasattr(mob, "tex_string") and mob.tex_string == "\\times":
                self.play(FadeIn(mob))

        self.wait(1)

        # Animate the exponents transforming into the LCM terms
        for p in primes:
            e = factors1.get(p, 0)
            e2 = factors2.get(p, 0)
            lcm_e = max(e, e2)
            if lcm_e > 0:
                # Determine source exponent (larger exponent, colored GREEN)
                if e >= e2:
                    source_expr = decomp1
                    source_exp_indices = decomp1_exp_indices
                else:
                    source_expr = decomp2
                    source_exp_indices = decomp2_exp_indices

                # Only proceed if exponent exists in source expression
                if p in source_exp_indices:
                    source_exp_idx = source_exp_indices[p][0]
                else:
                    continue  # Exponent is 1; no exponent submobject to animate

                # Target exponent in LCM expression
                target_exp_idx = lcm_exp_indices[p][0]

                # Animate transformation
                self.play(
                    ReplacementTransform(
                        source_expr[source_exp_idx].copy(),
                        lcm_expr[target_exp_idx].set_opacity(1).set_color(GREEN),
                    )
                )

        self.wait(1)

        # Simplify the LCM to its numerical value
        lcm_value_tex = f"= {lcm_value}"
        lcm_value_expr = MathTex(lcm_value_tex)
        lcm_value_expr.next_to(lcm_expr, RIGHT)
        self.play(Write(lcm_value_expr))
        self.wait(2)
