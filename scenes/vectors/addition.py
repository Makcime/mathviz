from manim import *


class VectorExample(Scene):
    def construct(self):
        # Create a plane with invisible axes but visible grid lines
        plane = NumberPlane(
            x_axis_config={"stroke_width": 0}, y_axis_config={"stroke_width": 0}
        )
        # Define vectors and shift v1 to start at a different location
        # v1 = Vector([1, 2], color=BLUE).shift(RIGHT * 2 + UP * 1)
        v1 = Vector([1, 2], color=BLUE)
        mv1 = Vector([-1, -2], color=YELLOW)
        v2 = Vector([-5, -2], color=GREEN)

        # Create labels with arrow notation
        l1 = MathTex(r"\vec{v}_1", color=BLUE).move_to(v1.get_center() + RIGHT * 0.3)
        ml1 = MathTex(r"-\vec{v}_1", color=YELLOW).move_to(
            mv1.get_center() + LEFT * 0.5
        )
        l2 = MathTex(r"\vec{v}_2", color=GREEN).move_to(v2.get_center() + UP * 0.3)

        # Group vectors with their labels
        v1g = VGroup(v1, l1)
        mv1g = VGroup(mv1, ml1)
        v2g = VGroup(v2, l2)

        # Define the sum vector and its label, placed in the middle
        vsum = Vector([1 - 5, 2 - 2], color=RED)  # Sum of the two vectors
        lsum = MathTex(r"\vec{v}_1 + \vec{v}_2", color=RED).move_to(
            vsum.get_center() + DOWN * 0.3
        )
        vsumg = VGroup(vsum, lsum)

        # Define the diff vector and its label, placed in the middle
        vdiff = Vector([-1 - 5, -2 - 2], color=PURPLE)  # diff of the two vectors
        ldiff = MathTex(r"\vec{v}_2 - \vec{v}_1", color=PURPLE).move_to(
            vdiff.get_center() + RIGHT
        )
        vdiffg = VGroup(vdiff, ldiff)

        # Add groups to the scene
        self.add(plane, v1g, v2g)
        self.wait(2)

        # Animate moving v2 so its tail attaches to the head of v1
        self.play(v2g.animate.shift(v1.get_end()))
        self.play(GrowArrow(vsum), FadeIn(lsum))
        self.play(vsumg.animate.shift(v1.get_start()))
        self.wait(2)

        l1.shift(LEFT)
        self.shift(v2, v1, v1g)
        self.wait(2)

        self.shift(v2, v1, v1g)
        self.wait(2)

        shift_amount = v2.get_start() - vsum.get_start()
        self.play(vsumg.animate.shift(shift_amount))
        self.play(lsum.animate.shift(UP * 0.7))

        self.wait(2)
        mv1g.shift(v1.get_start())
        self.play(GrowArrow(mv1), FadeIn(ml1))
        self.wait(2)

        shift_amount = v2.get_start() - vdiff.get_start()
        vdiffg.shift(shift_amount)

        self.play(GrowArrow(vdiff), FadeIn(ldiff))
        self.wait(2)

    def shift(self, va, vb, vag):
        # Calculate the required shift for v1g so its tail attaches to the head of v2
        shift_amount = va.get_end() - vb.get_start()
        # Animate moving v1g using the calculated shift
        self.play(vag.animate.shift(shift_amount))
