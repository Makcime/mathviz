from manim import *


class GridScene(Scene):
    def construct(self):

        # Call the function to animate the transformation and get the final text
        Sy = self.animate_transformation("x", "y", position=UR)

        # Move the final text to a new position
        self.play(Sy.animate.to_corner(UR))
        # self.play(final_text_2.animate.to_edge(RIGHT))

        self.wait(1)

        # Create the axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=7,  # Adjusted to fit within the screen
            y_length=7,  # Adjusted to fit within the screen
            axis_config={"include_numbers": True, "font_size": 24},
        )

        # Add gridlines
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=7,  # Adjusted to fit within the screen
            y_length=7,  # Adjusted to fit within the screen
            background_line_style={"stroke_opacity": 0.5},
        )

        # Add to scene
        self.add(grid, axes)

        # Add x and y labels
        x_ = axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT, buff=0.1)
        y_ = axes.get_y_axis_label("y", edge=UP, direction=UP, buff=0.5)

        # Optionally, you can scale the entire scene
        self.play(FadeIn(grid, axes, x_, y_))

        # Add the label "A (2; -4)" at the top left corner
        A = MathTex("A (-2; -4)").to_corner(UL)
        self.play(Write(A))
        self.wait(2)

        # Add a point at the location (2, -4)
        self.drawPoint(axes, cx=-2, cy=-4, label="A", color=RED)
        self.wait(2)

        SyAA = MathTex("S_{y}(A) = A'").next_to(A, DOWN, aligned_edge=LEFT)
        self.play(Write(SyAA))
        self.wait(2)

        SyA = self.animate_transformation("-2", "-4", position=DOWN, relative_to=SyAA)
        self.wait(2)

        self.drawPoint(axes, cx=2, cy=-4, label="A'", color=RED)
        self.wait(2)

    def drawPoint(self, axes, cx, cy, label="P", color=RED):
        # Add a point at the location (2, -4)
        p = Dot(axes.coords_to_point(cx, cy), color=color)

        # Add a label next to the point
        lp = MathTex(label).next_to(p, UR)
        self.play(FadeIn(p), Write(lp))

    def animate_transformation(self, x_val, y_val, position=ORIGIN, relative_to=None):
        # Determine the opposite of x_val
        if x_val.startswith("-"):
            opposite_x_val = x_val[1:]
        else:
            opposite_x_val = "-" + x_val

        # Create the MathTex object for Sy
        Sy_part1 = MathTex(f"S_{{y}} ({x_val}; {y_val}) = ")
        Sy_part2 = MathTex(f"({opposite_x_val}; {y_val})")

        # Position the parts correctly
        if relative_to:
            # Sy_part1.next_to(relative_to, position)
            Sy_part1.next_to(relative_to, position, aligned_edge=LEFT)
        else:
            Sy_part1.move_to(position)
        Sy_part2.next_to(Sy_part1, RIGHT)

        # Display the first part
        self.play(Write(Sy_part1))

        # Create a copy of the x_val
        x_copy = Sy_part1[0][
            3 : len(x_val) + 3
        ].copy()  # Adjust the index to correctly target the x_val

        # Highlight the original x_val in red
        self.play(Sy_part1[0][3 : len(x_val) + 3].animate.set_color(RED))

        # Animate the copy of x_val to -x_val and display the final part
        self.play(
            Write(Sy_part2),
            Transform(x_copy, Sy_part2[0][1 : len(opposite_x_val) + 1].set_color(RED)),
        )  # Transform x_copy to -x_val

        # Group the resulting text
        final_text = VGroup(Sy_part1, Sy_part2, x_copy)

        return final_text
