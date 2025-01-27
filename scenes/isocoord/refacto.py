from manim import *

##############################################################################
# 1) A small helper/mixin to draw the axes + grid
##############################################################################


class GridMixin:
    def setup_axes_and_grid(self):
        """Create and animate the axes + grid onto the scene."""
        self.axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=7,
            axis_config={
                "include_numbers": True,
                "font_size": 24,
                "tip_width": 0.2,
            },
        )

        self.grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=7,
            background_line_style={"stroke_opacity": 0.5},
        )

        x_label = self.axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT, buff=0.1)
        y_label = self.axes.get_y_axis_label("y", edge=UP, direction=UP, buff=0.5)

        self.xy_plane = VGroup(self.grid, self.axes, x_label, y_label)
        self.xy_plane.scale(0.9)
        self.xy_plane.to_corner(DR, buff=0.8)

        self.play(FadeIn(self.xy_plane))


##############################################################################
# 2) A generic base scene for transformations
##############################################################################


class BaseTransformationScene(Scene, GridMixin):
    """
    A base class that covers:
      - Title
      - A generic transform expression: prefix (x; y) = (x', y')
      - A demonstration of an example point A
    Subclasses override 'get_title_text()', 'get_prefix()', 'transform_func()', etc.
    """

    def get_title_text(self):
        """Override in subclasses."""
        return "Default Transformation Title"

    def get_prefix(self):
        """Override in subclasses."""
        return "S_{x}"

    def get_opposites(self, x_val, y_val):
        """
        If x_val or y_val is purely numeric (e.g. "2", "-3.5"),
        return the numeric negative (as a string).
        Otherwise (e.g. "x", "-x"), prepend or remove '-' to get the symbolic opposite.
        """

        def opposite(val):
            # Attempt to parse as float
            try:
                num = float(val)
                # If numeric, just return its negative as string
                return str(-num)
            except ValueError:
                # If not float, treat as symbolic: prepend or remove '-'
                return val[1:] if val.startswith("-") else f"-{val}"

        return opposite(x_val), opposite(y_val)

    def transform_func(self, x, y):
        """
        Example usage for Sx-like transformation:
          Original (x, y) -> (x, -y).
        In this version, x remains 'x' (or numeric),
        y is replaced by its opposite form (e.g. -4 becomes 4, or y -> -y).
        """
        ox, oy = self.get_opposites(x, y)
        return (x, oy)  # x unchanged, y replaced by its opposite

    def format_if_numeric(self, val):
        """
        If 'val' is numeric (float or a string like '2', '-3.5'),
        format as a short float (e.g. '2', '-3.5').
        Otherwise (e.g. 'x', '-x'), just return it as-is.
        """
        # If val is already a float or int, format it directly:
        if isinstance(val, (int, float)):
            return f"{val:g}"

        # Otherwise assume it's a string and try to parse float
        try:
            num = float(val)
            return f"{num:g}"
        except ValueError:
            # Not numeric => symbolic => return unchanged
            return val

    def get_example_point(self):
        """Override in subclasses.  Returns ((x0, y0), 'A') for the example point."""
        return (2, -4), "A"

    def construct(self):
        # 1) Show title
        title_text = self.get_title_text()
        title = Text(title_text, font_size=36)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # 2) Animate the transformation text for symbolic x,y
        prefix = self.get_prefix()
        transform_equation = self.animate_transformation(prefix, "x", "y")

        # Move them together (title + transform) up-left in one animation
        title.generate_target()
        transform_equation.generate_target()

        title.target.to_corner(UL, buff=0.8)
        transform_equation.target.next_to(title.target, DOWN, aligned_edge=LEFT)

        self.play(MoveToTarget(title), MoveToTarget(transform_equation))

        # 3) Draw grid
        self.setup_axes_and_grid()

        # 4) Show example point A at (x0, y0)
        (x0, y0), label_str = self.get_example_point()
        A_label_tex = MathTex(f"{label_str} ({x0}; {y0})")
        A_label_tex.next_to(transform_equation, DOWN, aligned_edge=LEFT)
        self.play(Write(A_label_tex))

        # Place a dot + label on the axes
        pA = Dot(self.axes.coords_to_point(x0, y0), color=RED)
        pA_label = MathTex(label_str).next_to(pA, UR)

        # Animate from text "A(...)" -> actual dot
        self.play(Circumscribe(A_label_tex))
        self.play(Transform(A_label_tex.copy(), VGroup(pA, pA_label)))

        # 5) The text "prefix(A) = A'"
        transform_of_A_tex = MathTex(f"{prefix}({label_str}) = {label_str}'")
        transform_of_A_tex.next_to(A_label_tex, DOWN, aligned_edge=LEFT)
        self.play(Write(transform_of_A_tex))

        transform_equation = self.animate_transformation(
            prefix, x0, y0, position=DOWN, relative_to=transform_of_A_tex
        )

        # 6) Actually transform (x0, y0) => new coords
        new_x, new_y = self.transform_func(x0, y0)
        try:
            new_x = float(new_x)
            new_y = float(new_y)
        except ValueError:
            # If you can't convert to float, handle gracefully:
            # e.g. skip placing the dot, or show a warning
            pass
        pA_prime = Dot(self.axes.coords_to_point(new_x, new_y), color=RED)
        A_prime_label = MathTex(f"{label_str}'").next_to(pA_prime, UR)

        # Animate transformations / lines
        self.play(
            Circumscribe(transform_equation[2])
        )  # highlight second part (just an example)
        self.play(
            Transform(transform_equation[2].copy(), VGroup(pA_prime, A_prime_label))
        )

        # Draw a dashed line from A to A'
        self.animate_lines(pA, pA_prime)

        self.wait(2)

    def animate_lines(self, p1, p2):
        line = DashedLine(p1, p2, dashed_ratio=0.2)
        self.play(Create(line))

    def animate_transformation(
        self, prefix, x_val, y_val, position=ORIGIN, relative_to=None
    ):
        """
        A generic version of your 'animate_Sx' etc. It constructs something like:
            prefix (x_val; y_val) = (x', y')
        animates it in, and returns the final VGroup.
        """
        # 1) Convert to floats (if we want to do numeric transformation)
        # In your original code, x_val/y_val might be strings like "2", "-4".
        # If your transform depends on them being numeric, parse them:
        try:
            x_f = float(x_val)
            y_f = float(y_val)
        except:
            # If parse fails, just set them to 0 to avoid errors.
            # Or handle purely symbolic scenario.
            x_f, y_f = 0, 0

        # 2) Apply transform_func to get new coords
        nx, ny = self.transform_func(x_val, y_val)

        # Safely convert them to displayable strings
        sx_new = self.format_if_numeric(nx)
        sy_new = self.format_if_numeric(ny)

        # 3) Build the MathTex
        part0 = MathTex(f"{prefix}")
        part1 = MathTex(f"({x_val};{y_val}) = ")
        part2 = MathTex(f"({sx_new};{sy_new})")

        # Position the parts correctly
        if relative_to:
            # Sx_part1.next_to(relative_to, position)
            part0.next_to(relative_to, position, aligned_edge=LEFT)
        else:
            part0.move_to(position)

        part1.next_to(part0, RIGHT)
        part2.next_to(part1, RIGHT)

        # Animate them
        self.play(Write(part0), Write(part1))
        self.play(Write(part2))

        # (Optional) color some subparts if you want. E.g. color x in red, y in yellow
        # Just do direct subobject indexing if consistent across all transformations:
        # x_slice = part1[0][...some range...]
        # x_slice.set_color(RED)
        # etc.
        self.color_specific_parts(
            part1,
            part2,
            old_x=x_val,
            old_y=y_val,
            new_x=sx_new,
            new_y=sy_new,
            prefix=prefix,
        )

        return VGroup(part0, part1, part2)

    def color_specific_parts(self, part1, part2, old_x, old_y, new_x, new_y, prefix):
        """
        Default logic: if old_x != new_x, color those in RED,
                       if old_y != new_y, color those in YELLOW.
        Override in subclasses if each transformation has special logic.
        """
        x_changed = str(old_x) != str(new_x)
        y_changed = str(old_y) != str(new_y)

        if x_changed:
            s = part1.get_tex_string()
            i = s.index("(") + 1
            j = s.index(";")
            y = part1[0][i:j]
            y.set_color(RED)
            self.play(Indicate(y, color=RED, scale_factor=2))

            s = part2.get_tex_string()
            i = s.index("(") + 1
            j = s.index(";")
            y = part2[0][i:j]
            y.set_color(RED)
            self.play(Indicate(y, color=RED, scale_factor=2))

        if y_changed:
            s = part1.get_tex_string()
            i = s.index(";") + 1
            j = s.index(")")
            y = part1[0][i:j]
            y.set_color(YELLOW)
            self.play(Indicate(y, color=YELLOW, scale_factor=2))

            s = part2.get_tex_string()
            i = s.index(";") + 1
            j = s.index(")")
            y = part2[0][i:j]
            y.set_color(YELLOW)
            self.play(Indicate(y, color=YELLOW, scale_factor=2))


##############################################################################
# 3) Each specific transformation is just a subclass
##############################################################################


class SxScene(BaseTransformationScene):
    def get_title_text(self):
        return "Symétrie orthogonale\nd'axe x"

    def get_prefix(self):
        return "S_{x}"

    def transform_func(self, x, y):
        ox, oy = self.get_opposites(x, y)
        return (x, oy)  # x unchanged, y replaced by its opposite

    def get_example_point(self):
        return (2, -4), "A"


class SyScene(BaseTransformationScene):
    def get_title_text(self):
        return "Symétrie orthogonale\nd'axe y"

    def get_prefix(self):
        return "S_{y}"

    def transform_func(self, x, y):
        ox, oy = self.get_opposites(x, y)
        return (ox, y)

    def get_example_point(self):
        return (2, -4), "A"


class SoScene(BaseTransformationScene):
    def get_title_text(self):
        return "Symétrie centrale\nde centre O(0, 0)"

    def get_prefix(self):
        return "S_{O}"

    def transform_func(self, x, y):
        ox, oy = self.get_opposites(x, y)
        return (ox, oy)

    def get_example_point(self):
        return (2, -4), "A"


class RoScene(BaseTransformationScene):
    def color_specific_parts(self, part1, part2, old_x, old_y, new_x, new_y, prefix):
        s = part1.get_tex_string()
        i = s.index("(") + 1
        j = s.index(";")
        y = part1[0][i:j]
        y.set_color(RED)
        self.play(Indicate(y, color=RED, scale_factor=2))

        s = part2.get_tex_string()
        i = s.index(";") + 1
        j = s.index(")")
        y = part2[0][i:j]
        y.set_color(RED)
        self.play(Indicate(y, color=RED, scale_factor=2))

        s = part1.get_tex_string()
        i = s.index(";") + 1
        j = s.index(")")
        y = part1[0][i:j]
        y.set_color(YELLOW)
        self.play(Indicate(y, color=YELLOW, scale_factor=2))

        s = part2.get_tex_string()
        i = s.index("(") + 1
        j = s.index(";")
        y = part2[0][i:j]
        y.set_color(YELLOW)
        self.play(Indicate(y, color=YELLOW, scale_factor=2))

    def animate_lines(self, p1, p2):
        p0 = Dot(self.axes.coords_to_point(0, 0), color=RED)
        l1 = DashedLine(p1, p0, dashed_ratio=0.4)
        l2 = DashedLine(p0, p2, dashed_ratio=0.4)
        self.play(Create(l1))
        self.play(Create(l2))


class Rop(RoScene):
    def get_title_text(self):
        return "Rotation de centre O(0, 0),\net d'amplitude +90°"

    def get_prefix(self):
        return "r_{O; +90^{\\circ}}"

    def transform_func(self, x, y):
        # +90° rotation => (x, y) -> (-y, x)
        ox, oy = self.get_opposites(x, y)
        return (oy, x)

    def get_example_point(self):
        return (2, -4), "A"


class Ron(RoScene):
    def get_title_text(self):
        return "Rotation de centre O(0, 0),\net d'amplitude -90°"

    def get_prefix(self):
        return "r_{O; -90^{\\circ}}"

    def transform_func(self, x, y):
        # -90° rotation => (x, y) -> (y, -x)
        ox, oy = self.get_opposites(x, y)
        return (y, ox)

    def get_example_point(self):
        return (2, -4), "A"


class TOP(BaseTransformationScene):
    def get_title_text(self):
        return r"Translation de vecteur $\overrightarrow{OP}$"

    def get_prefix(self):
        return "t_{\overrightarrow{OP}}"

    def transform_func(self, x, y):
        ox, oy = self.get_opposites(x, y)
        return (ox, oy)

    def get_example_point(self):
        return (2, -4), "A"

    def construct(self):
        # 1) Show title
        title_text = self.get_title_text()
        title = Tex(title_text, font_size=56)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # 2) Animate the transformation text for symbolic x,y
        prefix = self.get_prefix()
        transform_equation = self.animate_transformation(prefix, "x", "y")

        # Move them together (title + transform) up-left in one animation
        title.generate_target()
        transform_equation.generate_target()

        title.target.to_corner(UL, buff=0.8)
        transform_equation.target.next_to(title.target, DOWN, aligned_edge=LEFT)

        self.play(MoveToTarget(title), MoveToTarget(transform_equation))

        # 3) Draw grid
        self.setup_axes_and_grid()

        # 4) Show example point A at (x0, y0)
        (x0, y0), label_str = self.get_example_point()
        A_label_tex = MathTex(f"{label_str} ({x0}; {y0})")
        A_label_tex.next_to(transform_equation, DOWN, aligned_edge=LEFT)
        self.play(Write(A_label_tex))

        # Place a dot + label on the axes
        pA = Dot(self.axes.coords_to_point(x0, y0), color=RED)
        pA_label = MathTex(label_str).next_to(pA, UR)

        # Animate from text "A(...)" -> actual dot
        self.play(Circumscribe(A_label_tex))
        self.play(Transform(A_label_tex.copy(), VGroup(pA, pA_label)))

        # 5) The text "prefix(A) = A'"
        transform_of_A_tex = MathTex(f"{prefix}({label_str}) = {label_str}'")
        transform_of_A_tex.next_to(A_label_tex, DOWN, aligned_edge=LEFT)
        self.play(Write(transform_of_A_tex))

        transform_equation = self.animate_transformation(
            prefix, x0, y0, position=DOWN, relative_to=transform_of_A_tex
        )

        # 6) Actually transform (x0, y0) => new coords
        new_x, new_y = self.transform_func(x0, y0)
        try:
            new_x = float(new_x)
            new_y = float(new_y)
        except ValueError:
            # If you can't convert to float, handle gracefully:
            # e.g. skip placing the dot, or show a warning
            pass
        pA_prime = Dot(self.axes.coords_to_point(new_x, new_y), color=RED)
        A_prime_label = MathTex(f"{label_str}'").next_to(pA_prime, UR)

        # Animate transformations / lines
        self.play(
            Circumscribe(transform_equation[2])
        )  # highlight second part (just an example)
        self.play(
            Transform(transform_equation[2].copy(), VGroup(pA_prime, A_prime_label))
        )

        # Draw a dashed line from A to A'
        self.animate_lines(pA, pA_prime)

        self.wait(2)
