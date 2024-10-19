
from manim import *

class PrimeFactorDecomposition(Scene):
    def construct(self):
        # 1. List of primes under 20
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        primes_texts = [MathTex(str(p)) for p in primes]

        # 2. Arrange primes horizontally
        primes_group = VGroup(*primes_texts).arrange(RIGHT, buff=0.5)

        # 3. Primes label
        primes_label = Text("Primes under 20:")
        primes_label.to_edge(UP).shift(DOWN * 0.5)

        # 4. Position primes group
        primes_group.next_to(primes_label, DOWN, buff=0.3)

        # 5. Add label and primes to scene
        self.play(Write(primes_label))
        self.play(Write(primes_group))

        # 6. Vertical line
        vertical_line = Line(
            start=primes_group.get_bottom() + DOWN * 0.5,
            end=DOWN * 3
        )
        self.play(Create(vertical_line))

        # 7. Number 126
        number_126 = MathTex("126")
        number_126.next_to(vertical_line.get_top(), LEFT)
        self.play(Write(number_126))

        # 8. Highlight number 2 in primes
        prime_2_index = primes.index(2)
        number_2_in_primes = primes_group[prime_2_index]
        rect_around_2 = SurroundingRectangle(number_2_in_primes, color=RED)
        self.play(Create(rect_around_2))

        # 9. Display factor 2 beside 126 (shifted to the right)
        factor_2 = MathTex("2")
        factor_2.next_to(number_126, RIGHT, buff=0.5)
        factor_2.shift(RIGHT * 0.5)  # Shift further to the right
        self.play(Write(factor_2))

        # 10. Write "126 ÷ 2 = 63" on the right
        division_equation = MathTex("126 \\div 2 = 63")
        division_equation.to_edge(RIGHT).shift(UP)
        self.play(Write(division_equation))

        # 11. Place 63 under 126 without replacing 126
        number_63 = MathTex("63")
        number_63.next_to(number_126, DOWN, aligned_edge=LEFT)
        self.play(
            TransformFromCopy(division_equation[-1], number_63)
        )

        # 12. Fade out the division equation and rectangle around 2
        self.play(
            FadeOut(division_equation),
            FadeOut(rect_around_2)
        )

        # 13. Since 63 cannot be divided by 2, proceed to next prime (3)
        # Highlight number 3 in primes
        prime_3_index = primes.index(3)
        number_3_in_primes = primes_group[prime_3_index]
        rect_around_3 = SurroundingRectangle(number_3_in_primes, color=RED)
        self.play(Create(rect_around_3))

        # 14. Display factor 3 beside 63 (shifted to the right)
        factor_3 = MathTex("3")
        factor_3.next_to(number_63, RIGHT, buff=0.5)
        factor_3.shift(RIGHT * 0.5)  # Shift further to the right
        self.play(Write(factor_3))

        # 15. Write "63 ÷ 3 = 21" on the right
        division_equation_2 = MathTex("63 \\div 3 = 21")
        division_equation_2.next_to(division_equation, DOWN, aligned_edge=RIGHT)
        self.play(Write(division_equation_2))

        # 16. Place 21 under 63
        number_21 = MathTex("21")
        number_21.next_to(number_63, DOWN, aligned_edge=LEFT)
        self.play(
            TransformFromCopy(division_equation_2[-1], number_21)
        )

        # 17. Fade out the division equation and rectangle around 3
        self.play(
            FadeOut(division_equation_2),
            FadeOut(rect_around_3)
        )

        # Continue the decomposition as needed
       # You can continue the process similarly for further decomposition
