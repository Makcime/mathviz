from manim import *


class VectorExample(Scene):
    def construct(self):
        # Create a plane with visible grid lines but no axes
        # plane = NumberPlane(
        #     x_axis_config={"stroke_width": 0}, y_axis_config={"stroke_width": 0}
        # )
        # self.add(plane)

        # Define vectors
        vector_1 = Vector([1, 2], color=BLUE)
        vector_2 = Vector([-5, -2], color=GREEN)

        # Create labels with arrow notation
        # Place label_1 slightly to the right of the midpoint of vector_1
        label_1 = MathTex(r"\vec{v}_1", color=BLUE).move_to(
            vector_1.get_center() + RIGHT * 0.3  # Adjust offset as needed
        )
        label_2 = MathTex(r"\vec{v}_2", color=GREEN).move_to(
            vector_2.get_center() + UP * 0.3
        )

        # Group vector_2 and its label so they move together
        v2_group = VGroup(vector_2, label_2)

        # Define the sum vector and its label, placed in the middle
        vector_sum = Vector([1 - 5, 2 - 2], color=RED)  # Sum of the two vectors
        label_sum = MathTex(r"\vec{v}_1 + \vec{v}_2", color=RED).move_to(
            vector_sum.get_center() + DOWN * 0.3
        )

        # Add the plane, first vector, second vector group, and first label to the scene
        self.add(vector_1, v2_group, label_1)

        # Animate moving vector_2 (with its label) so its tail attaches to the head of vector_1
        self.play(v2_group.animate.shift(vector_1.get_end()))

        # Animate the appearance of the sum vector and its label
        self.play(GrowArrow(vector_sum), FadeIn(label_sum))

        self.wait(2)
