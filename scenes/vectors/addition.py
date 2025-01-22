from manim import *


class VectorAddDiffGrid(Scene):
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


class VectorAddDiffNoGrid(Scene):
    def construct(self):
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
        self.add(v1g, v2g)
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


class VectorAddMulti(Scene):
    def construct(self):
        # Define vectors with their respective directions and colors
        v1 = Vector([1, 3], color=BLUE)
        v2 = Vector([-5, -2], color=GREEN)
        v3 = Vector([-3, 2], color=YELLOW)
        v4 = Vector([2, -4], color=PURPLE)

        # Create labels for each vector
        l1 = MathTex(r"\vec{v}_1", color=BLUE).move_to(v1.get_center() + RIGHT * 0.3)
        l2 = MathTex(r"\vec{v}_2", color=GREEN).move_to(v2.get_center() + UP * 0.5)
        l3 = MathTex(r"\vec{v}_3", color=YELLOW).move_to(v3.get_center() + UP * 0.5)
        l4 = MathTex(r"\vec{v}_4", color=PURPLE).move_to(v4.get_center() + RIGHT * 0.3)

        # Group each vector with its label for synchronized movement
        v1g = VGroup(v1, l1)
        v2g = VGroup(v2, l2)
        v3g = VGroup(v3, l3)
        v4g = VGroup(v4, l4)

        # Shift all vectors initially to the right by 1.5 units to position them away from the origin
        v1g.shift(RIGHT * 1.5)
        v2g.shift(RIGHT * 1.5)
        v3g.shift(RIGHT * 1.5)
        v4g.shift(RIGHT * 1.5)

        # Define the sum vector as the sum of all four vectors
        vsum_components = [
            v1.get_vector()[0]
            + v2.get_vector()[0]
            + v3.get_vector()[0]
            + v4.get_vector()[0],
            v1.get_vector()[1]
            + v2.get_vector()[1]
            + v3.get_vector()[1]
            + v4.get_vector()[1],
        ]
        vsum = Vector(vsum_components, color=RED)
        lsum = MathTex(
            r"\vec{v}_1 + \vec{v}_2 + \vec{v}_3 + \vec{v}_4", color=RED
        ).move_to(vsum.get_center() + DOWN * 0.3 + RIGHT * 1.3)
        vsumg = VGroup(vsum, lsum)

        # Define the difference vector (optional, based on original code)
        # Here, assuming you want vdiff = v2 - v1 - v3 - v4
        # Adjust as per your specific requirement
        vdiff_components = [
            v2.get_vector()[0]
            - v1.get_vector()[0]
            - v3.get_vector()[0]
            - v4.get_vector()[0],
            v2.get_vector()[1]
            - v1.get_vector()[1]
            - v3.get_vector()[1]
            - v4.get_vector()[1],
        ]
        vdiff = Vector(vdiff_components, color=PURPLE)
        ldiff = MathTex(
            r"\vec{v}_2 - \vec{v}_1 - \vec{v}_3 - \vec{v}_4", color=PURPLE
        ).move_to(vdiff.get_center() + RIGHT * 0.3)
        vdiffg = VGroup(vdiff, ldiff)

        # Add all vector groups to the scene
        self.add(v1g, v2g, v3g, v4g)
        self.wait(2)

        # Shift vectors tail-to-head
        self.shift(v1, v2, v2g)
        self.shift(v2, v3, v3g)
        self.shift(v3, v4, v4g)

        self.wait(2)

        # Animate the appearance of the sum vector
        shift_amount = v1.get_start() - vsum.get_start()
        vsumg.shift(shift_amount)
        self.play(GrowArrow(vsum), FadeIn(lsum))
        self.wait(2)

        # self.shift(v3, v1, v3g)
        shift_amount = v3.get_end() - v1.get_start()
        self.play(v3g.animate.shift(-shift_amount))

        self.shift(v2, v4, v4g)
        self.wait(1)

        shift_amount = v3.get_start() - vsum.get_start()
        self.play(vsumg.animate.shift(shift_amount))
        self.wait(2)

    def shift(self, va, vb, vag):
        """
        Shifts the moving_group so that its tail attaches to the head of another vector.

        Parameters:
        - va: The fixed vector whose head will be the new tail for the moving_group.
        - vb: The vector to be shifted.
        - vag: The VGroup containing the vector and its label to shift.
        """
        # Calculate the shift amount needed
        shift_amount = va.get_end() - vb.get_start()
        # Animate the shift
        self.play(vag.animate.shift(shift_amount))
