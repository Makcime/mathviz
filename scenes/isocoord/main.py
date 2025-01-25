from manim import *


def drawGrid(self):
    # Create the axes
    self.axes = Axes(
        x_range=[-5, 5, 1],
        y_range=[-5, 5, 1],
        x_length=7,  # Adjusted to fit within the screen
        y_length=7,  # Adjusted to fit within the screen
        axis_config={
            "include_numbers": True,
            "font_size": 24,
            # "tip_length": 1.1,
            "tip_width": 0.2,
        },
    )

    # Add gridlines
    self.grid = NumberPlane(
        x_range=[-5, 5, 1],
        y_range=[-5, 5, 1],
        x_length=7,  # Adjusted to fit within the screen
        y_length=7,  # Adjusted to fit within the screen
        background_line_style={"stroke_opacity": 0.5},
    )

    # Add to scene
    # self.add(grid, axes)

    # Add x and y labels
    x_ = self.axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT, buff=0.1)
    y_ = self.axes.get_y_axis_label("y", edge=UP, direction=UP, buff=0.5)

    self.xyPlane = VGroup(self.grid, self.axes, x_, y_)
    self.xyPlane.scale(0.9)
    self.xyPlane.to_corner(DR, buff=0.8)

    self.play(FadeIn(self.xyPlane))


class Sx(Scene):
    def construct(self):

        title = Text("Symétrie orthogonale d'axe x", font_size=36)
        self.play(Write(title))  # Animate the writing of the title
        self.play(title.animate.to_edge(UP))

        Sx = self.animate_Sx("x", "y")

        # Fade out the title
        # self.play(Sx.animate.to_corner(UL), FadeOut(title))

        # 1) Create "targets" for each
        title.generate_target()
        Sx.generate_target()

        # 2) Move them in the "target" space
        title.target.to_corner(UL, buff=0.8)
        Sx.target.next_to(title.target, DOWN, aligned_edge=LEFT)

        # 3) Animate them both at once
        self.play(MoveToTarget(title), MoveToTarget(Sx))

        drawGrid(self)

        A = MathTex("A (2; -4)").next_to(Sx, DOWN, aligned_edge=LEFT)
        self.play(Write(A))

        p1 = Dot(self.axes.coords_to_point(2, -4), color=RED)
        lp = MathTex("A").next_to(p1, UR)
        self.play(Circumscribe(A))
        self.play(Transform(A.copy(), VGroup(p1, lp)))

        SxAA = MathTex("S_{x}(A) = A'").next_to(A, DOWN, aligned_edge=LEFT)
        self.play(Write(SxAA))

        SxA = self.animate_Sx("2", "-4", position=DOWN, relative_to=SxAA)

        p2 = Dot(self.axes.coords_to_point(2, 4), color=RED)
        lp = MathTex("A'").next_to(p2, UR)
        self.play(Circumscribe(SxA[1]))
        self.play(Transform(SxA[1].copy(), VGroup(p2, lp)))

        self.play(GrowFromEdge(DashedLine(p1, p2), DL))

        self.wait(3)

    def animate_Sx(self, x_val, y_val, position=ORIGIN, relative_to=None):
        # Determine the opposite of y_val
        if y_val.startswith("-"):
            opposite_y_val = y_val[1:]
        else:
            opposite_y_val = "-" + y_val

        # Create the MathTex object for Sx
        Sx_part1 = MathTex(f"S_{{x}} ({x_val}; {y_val}) = ")
        Sx_part2 = MathTex(f"({x_val}; {opposite_y_val})")

        # Position the parts correctly
        if relative_to:
            # Sx_part1.next_to(relative_to, position)
            Sx_part1.next_to(relative_to, position, aligned_edge=LEFT)
        else:
            Sx_part1.move_to(position)
        Sx_part2.next_to(Sx_part1, RIGHT)

        # Display the first part
        self.play(Write(Sx_part1))

        y = Sx_part1[0][5 : len(y_val) + 5]
        y.set_color(RED)
        my = Sx_part2[0][3 : len(opposite_y_val) + 3]

        # Create a copy of the y_val
        y_copy = y.copy()  # Adjust the index to correctly target the x_val

        # Highlight the original x_val in red
        self.play(Indicate(y, color=RED, scale_factor=2))

        # Animate the copy of x_val to -x_val and display the final part
        self.play(
            Write(Sx_part2),
            Transform(y_copy, my.set_color(RED)),
        )  # Transform x_copy to -x_val

        self.play(Indicate(y))
        self.play(Indicate(my))

        # Group the resulting text
        final_text = VGroup(Sx_part1, Sx_part2, y_copy)

        return final_text


class Sy(Scene):
    def construct(self):
        # Write the title at the beginning
        title = Text("Symétrie orthogonale d'axe y", font_size=36)
        self.play(Write(title))  # Animate the writing of the title
        self.play(title.animate.to_edge(UP))

        Sy = self.animate_Sy("x", "y")

        # Fade out the title
        self.play(Sy.animate.to_corner(UR), FadeOut(title))

        drawGrid(self)

        # Add the label "A (2; -4)" at the top left corner
        A = MathTex("A (-2; -4)").to_corner(UL)
        self.play(Write(A))
        # self.wait(2)

        p1 = Dot(self.axes.coords_to_point(-2, -4), color=RED)
        lp = MathTex("A").next_to(p1, UR)
        self.play(Circumscribe(A))
        self.play(Transform(A.copy(), VGroup(p1, lp)))

        SyAA = MathTex("S_{y}(A) = A'").next_to(A, DOWN, aligned_edge=LEFT)
        self.play(Write(SyAA))
        # self.wait(2)

        SyA = self.animate_Sy("-2", "-4", position=DOWN, relative_to=SyAA)
        # self.wait(2)

        p2 = Dot(self.axes.coords_to_point(2, -4), color=RED)
        lp = MathTex("A'").next_to(p2, UR)
        self.play(Circumscribe(SyA[1]))
        self.play(Transform(SyA[1].copy(), VGroup(p2, lp)))

        self.play(GrowFromEdge(DashedLine(p1, p2), DL))

        self.wait(3)

    def animate_Sy(self, x_val, y_val, position=ORIGIN, relative_to=None):
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

        x = Sy_part1[0][3 : len(x_val) + 3]
        x.set_color(RED)
        mx = Sy_part2[0][1 : len(opposite_x_val) + 1]

        # Create a copy of the x_val
        x_copy = x.copy()  # Adjust the index to correctly target the x_val

        # Highlight the original x_val in red
        self.play(Indicate(x, color=RED, scale_factor=2))

        # Animate the copy of x_val to -x_val and display the final part
        self.play(
            Write(Sy_part2),
            Transform(x_copy, mx.set_color(RED)),
        )  # Transform x_copy to -x_val

        self.play(Indicate(x))
        self.play(Indicate(mx))

        # Group the resulting text
        final_text = VGroup(Sy_part1, Sy_part2, x_copy)

        return final_text


class So(Scene):
    def construct(self):
        # Write the title at the beginning
        title = Text("Symétrie centrale de centre O(0, 0)", font_size=36)
        self.play(Write(title))  # Animate the writing of the title
        self.play(title.animate.to_edge(UP))

        So = self.animate_So("x", "y")

        # Fade out the title
        self.play(So.animate.to_corner(UR), FadeOut(title))

        drawGrid(self)

        # Add the label "A (2; -4)" at the top left corner
        A = MathTex("A (-2; -4)").to_corner(UL)
        self.play(Write(A))
        # self.wait(2)

        p1 = Dot(self.axes.coords_to_point(-2, -4), color=RED)
        lp = MathTex("A").next_to(p1, UL)
        self.play(Circumscribe(A))
        self.play(Transform(A.copy(), VGroup(p1, lp)))

        SoAA = MathTex("S_{O}(A) = A'").next_to(A, DOWN, aligned_edge=LEFT)
        self.play(Write(SoAA))
        # self.wait(2)

        SoA = self.animate_So("-2", "-4", position=DOWN, relative_to=SoAA)
        # self.wait(2)

        p2 = Dot(self.axes.coords_to_point(2, 4), color=RED)
        lp = MathTex("A'").next_to(p2, UL)

        self.play(Circumscribe(SoA[1]))
        self.play(Transform(SoA[1].copy(), VGroup(p2, lp)))

        self.play(GrowFromEdge(DashedLine(p1, p2), DL))

        self.wait(3)

    def animate_So(self, x_val, y_val, position=ORIGIN, relative_to=None):
        # Determine the opposite of x_val
        if x_val.startswith("-"):
            opposite_x_val = x_val[1:]
        else:
            opposite_x_val = "-" + x_val

        # Determine the opposite of y_val
        if y_val.startswith("-"):
            opposite_y_val = y_val[1:]
        else:
            opposite_y_val = "-" + y_val

        # Create the MathTex object for Sy
        So_part1 = MathTex(f"S_{{O}} ({x_val}; {y_val}) = ")
        So_part2 = MathTex(f"({opposite_x_val}; {opposite_y_val})")

        # Position the parts correctly
        if relative_to:
            # Sy_part1.next_to(relative_to, position)
            So_part1.next_to(relative_to, position, aligned_edge=LEFT)
        else:
            So_part1.move_to(position)
        So_part2.next_to(So_part1, RIGHT)

        # Display the first part
        self.play(Write(So_part1))

        x = So_part1[0][3 : len(x_val) + 3]
        x.set_color(RED)
        mx = So_part2[0][1 : len(opposite_x_val) + 1]

        y = So_part1[0][len(x_val) + 4 : len(y_val) + len(x_val) + 4]
        y.set_color(YELLOW)
        my = So_part2[0][
        len(opposite_x_val) + 2 : len(opposite_y_val) + len(opposite_x_val) + 2
    ]

        # Create a copy of the x_val
        x_copy = x.copy()  # Adjust the index to correctly target the x_val
        y_copy = y.copy()  # Adjust the index to correctly target the x_val

        # Highlight the original x_val in red
        self.play(Indicate(x, color=RED, scale_factor=2))
        self.play(Indicate(y, color=YELLOW, scale_factor=2))

        # Animate the copy of x_val to -x_val and display the final part
        self.play(
            Write(So_part2),
            Transform(x_copy, mx.set_color(RED)),
            Transform(y_copy, my.set_color(YELLOW)),
        )  # Transform x_copy to -x_val

        self.play(Indicate(x, color=RED, scale_factor=2))
        self.play(Indicate(mx, color=RED, scale_factor=2))

        self.play(Indicate(y, color=YELLOW, scale_factor=2))
        self.play(
            Indicate(my, color=YELLOW, scale_factor=2)
        )  # Group the resulting text

        final_text = VGroup(So_part1, So_part2, x_copy, y_copy)

        return final_text


class Rop(Scene):
    def construct(self):
        # Write the title at the beginning
        title = Text("Rotation de centre O(0, 0), \n et d'ampliture +90°", font_size=36)
        self.play(Write(title))  # Animate the writing of the title
        self.play(title.animate.to_edge(UP))

        Rop = self.animate_Rop("x", "y")

        # Fade out the title
        self.play(Rop.animate.to_corner(UR), FadeOut(title))

        drawGrid(self)

        # Add the label "A (2; -4)" at the top left corner
        A = MathTex("A (-2; -4)").to_corner(UL)
        self.play(Write(A))
        # self.wait(2)

        p0 = Dot(self.axes.coords_to_point(0, 0), color=RED)
        p1 = Dot(self.axes.coords_to_point(-2, -4), color=RED)
        lp = MathTex("A").next_to(p1, UL)
        self.play(Circumscribe(A))
        self.play(Transform(A.copy(), VGroup(p1, lp)))

        RopAA = MathTex("R_{O; +90^{\circ}}(A) = A'").next_to(
            A, DOWN, aligned_edge=LEFT
        )
        self.play(Write(RopAA))
        # self.wait(2)

        RopA = self.animate_Rop("-2", "-4", position=DOWN, relative_to=RopAA)
        # self.wait(2)

        p2 = Dot(self.axes.coords_to_point(4, -2), color=RED)
        lp = MathTex("A'").next_to(p2, UL)

        self.play(Circumscribe(RopA[1]))
        self.play(Transform(RopA[1].copy(), VGroup(p2, lp)))

        self.play(GrowFromEdge(DashedLine(p1, p0), DL))
        self.play(GrowFromEdge(DashedLine(p0, p2), UL))

        self.wait(3)

    def animate_Rop(self, x_val, y_val, position=ORIGIN, relative_to=None):
        # Determine the opposite of x_val
        if x_val.startswith("-"):
            opposite_x_val = x_val[1:]
        else:
            opposite_x_val = "-" + x_val

        # Determine the opposite of y_val
        if y_val.startswith("-"):
            opposite_y_val = y_val[1:]
        else:
            opposite_y_val = "-" + y_val

        # Create the MathTex object for Sy
        Rop_part1 = MathTex(f"r_{{O; +90^{{\circ}}}} ({x_val}; {y_val}) = ")
        Rop_part2 = MathTex(f"({opposite_y_val}; {x_val})")

        # Position the parts correctly
        if relative_to:
            # Sy_part1.next_to(relative_to, position)
            Rop_part1.next_to(relative_to, position, aligned_edge=LEFT)
        else:
            Rop_part1.move_to(position)
        Rop_part2.next_to(Rop_part1, RIGHT)

        x = Rop_part1[0][8 : len(x_val) + 8]
        x.set_color(RED)
        mx = Rop_part2[0][1 : len(opposite_x_val) + 1]
        mx.set_color(BLACK)

        y = Rop_part1[0][len(x_val) + 9 : len(y_val) + len(x_val) + 9]
        y.set_color(YELLOW)
        my = Rop_part2[0][
        len(opposite_y_val) + 2 : len(x_val) + len(opposite_y_val) + 2
    ]
        my.set_color(BLACK)

        # Create a copy of the x_val
        x_copy = x.copy()  # Adjust the index to correctly target the x_val
        y_copy = y.copy()  # Adjust the index to correctly target the x_val

        # Animate the copy of x_val to -x_val and display the final part
        self.play(
            Write(Rop_part1),
            Write(Rop_part2),
        )

        self.play(Indicate(x, color=RED, scale_factor=2))
        my.set_color(RED)
        self.play(Indicate(my, color=RED, scale_factor=2))

        self.play(Indicate(y, color=YELLOW, scale_factor=2))
        mx.set_color(YELLOW)
        self.play(
            Indicate(mx, color=YELLOW, scale_factor=2)
        )  # Group the resulting text

        final_text = VGroup(Rop_part1, Rop_part2, x_copy, y_copy)

        return final_text


class Ron(Scene):
    def construct(self):
        # Write the title at the beginning
        title = Text("Rotation de centre O(0, 0), \n et d'ampliture -90°", font_size=36)
        self.play(Write(title))  # Animate the writing of the title
        self.play(title.animate.to_edge(UP))

        Ron = self.animate_Ron("x", "y")

        # Fade out the title
        self.play(Ron.animate.to_corner(UR), FadeOut(title))

        drawGrid(self)

        # Add the label "A (2; -4)" at the top left corner
        A = MathTex("A (-2; -4)").to_corner(UL)
        self.play(Write(A))
        # self.wait(2)

        p0 = Dot(self.axes.coords_to_point(0, 0), color=RED)
        p1 = Dot(self.axes.coords_to_point(2, -4), color=RED)
        lp = MathTex("A").next_to(p1, UL)
        self.play(Circumscribe(A))
        self.play(Transform(A.copy(), VGroup(p1, lp)))

        RonAA = MathTex("R_{O; -90^{\circ}}(A) = A'").next_to(
            A, DOWN, aligned_edge=LEFT
        )
        self.play(Write(RonAA))
        # self.wait(2)

        RonA = self.animate_Ron("2", "-4", position=DOWN, relative_to=RonAA)
        # self.wait(2)

        p2 = Dot(self.axes.coords_to_point(-4, -2), color=RED)
        lp = MathTex("A'").next_to(p2, UL)

        self.play(Circumscribe(RonA[1]))
        self.play(Transform(RonA[1].copy(), VGroup(p2, lp)))

        self.play(GrowFromEdge(DashedLine(p1, p0), DR))
        self.play(GrowFromEdge(DashedLine(p0, p2), UR))

        self.wait(3)

    def animate_Ron(self, x_val, y_val, position=ORIGIN, relative_to=None):
        # Determine the opposite of x_val
        if x_val.startswith("-"):
            opposite_x_val = x_val[1:]
        else:
            opposite_x_val = "-" + x_val

        # Determine the opposite of y_val
        if y_val.startswith("-"):
            opposite_y_val = y_val[1:]
        else:
            opposite_y_val = "-" + y_val

        # Create the MathTex object for Sy
        Ron_part1 = MathTex(f"r_{{O; -90^{{\circ}}}} ({x_val}; {y_val}) = ")
        Ron_part2 = MathTex(f"({y_val}; {opposite_x_val})")

        # Position the parts correctly
        if relative_to:
            # Sy_part1.next_to(relative_to, position)
            Ron_part1.next_to(relative_to, position, aligned_edge=LEFT)
        else:
            Ron_part1.move_to(position)
        Ron_part2.next_to(Ron_part1, RIGHT)

        x = Ron_part1[0][8 : len(x_val) + 8]
        x.set_color(RED)
        mx = Ron_part2[0][1 : len(opposite_x_val) + 1]
        mx.set_color(BLACK)

        y = Ron_part1[0][len(x_val) + 9 : len(y_val) + len(x_val) + 9]
        y.set_color(YELLOW)
        my = Ron_part2[0][len(y_val) + 2 : len(opposite_x_val) + len(y_val) + 2]
        my.set_color(BLACK)

        # Create a copy of the x_val
        x_copy = x.copy()  # Adjust the index to correctly target the x_val
        y_copy = y.copy()  # Adjust the index to correctly target the x_val

        # Animate the copy of x_val to -x_val and display the final part
        self.play(
            Write(Ron_part1),
            Write(Ron_part2),
        )

        self.play(Indicate(x, color=RED, scale_factor=2))
        my.set_color(RED)
        self.play(Indicate(my, color=RED, scale_factor=2))

        self.play(Indicate(y, color=YELLOW, scale_factor=2))
        mx.set_color(YELLOW)
        self.play(
            Indicate(mx, color=YELLOW, scale_factor=2)
        )  # Group the resulting text

        final_text = VGroup(Ron_part1, Ron_part2, x_copy, y_copy)

        return final_text
