from manim import *

class EpitrochoidDerivation(Scene):
    def construct(self):
        # Define the circles' radii
        R = 3  # Radius of the fixed circle
        r = 1  # Radius of the rolling circle
        d = 2  # Distance from the point to the center of the rolling circle

        # Draw the fixed circle
        fixed_circle = Circle(radius=R, color=BLUE)
        self.play(Create(fixed_circle))

        # Draw the rolling circle at the starting position
        rolling_circle = Circle(radius=r, color=GREEN).move_to([R + r, 0, 0])
        self.play(Create(rolling_circle))

        # Animate the rolling circle moving by a small amount
        small_rotation = 1/12  # Small angle for rotation
        def update_rolling_group(group, alpha):
            theta = alpha * small_rotation * 2 * np.pi
            center_x = (R + r) * np.cos(theta)
            center_y = (R + r) * np.sin(theta)
            group.move_to([center_x, center_y, 0])
            # Rotate the rolling circle relative to its own center
            group[0].rotate(-theta)
        
        rolling_group = VGroup(rolling_circle) 
        self.play(UpdateFromAlphaFunc(
            rolling_group,
            update_rolling_group
        ), run_time=2, rate_func=linear)

        # Calculate the angles for the arcs
        theta = small_rotation * 2 * np.pi
        alpha = theta * (R + r) / r

        # Show the arc length traveled by both circles
        fixed_arc = Arc(radius=R, start_angle=0, angle=theta, color=YELLOW)
        rolling_arc = Arc(radius=r, start_angle=-PI/6, angle=-alpha, arc_center=rolling_circle.get_center(), color=WHITE)
        self.play(Create(fixed_arc), Create(rolling_arc))

        # Draw and label R and r
        center_fixed = fixed_circle.get_center()
        center_rolling = rolling_circle.get_center()
        radius_R = Line(center_fixed, fixed_circle.point_at_angle(PI/6), color=YELLOW)
        radius_r = Line(center_rolling, rolling_circle.point_at_angle(PI+PI/6), color=RED)  # Point_at_angle ensures correct end of radius
        self.play(Create(radius_R), Create(radius_r))

        R_label = MathTex("R").next_to(radius_R, UP, buff=-0.3)
        r_label = MathTex("r").next_to(radius_r, LEFT, buff=-0.45)
        r_label.shift(UP * 0.25)
        self.play(Write(R_label), Write(r_label))

        # Draw and label theta and alpha
        theta_arc = Arc(radius=0.5, start_angle=0, angle=theta, arc_center=center_fixed, color=WHITE)
        theta_label = MathTex("\\theta").next_to(theta_arc, DOWN, buff=0.1)
        alpha_arc = Arc(radius=0.5, start_angle=-PI/6, angle=-alpha, arc_center=center_rolling, color=WHITE)
        alpha_label = MathTex("\\alpha").next_to(alpha_arc, DOWN, buff=0.1)
        self.play(Create(theta_arc), Write(theta_label))
        self.play(Create(alpha_arc), Write(alpha_label))

        # Move everything smaller and into a corner
        corner_group = VGroup(fixed_circle, rolling_circle, fixed_arc, rolling_arc, radius_R, radius_r, R_label, r_label, theta_arc, theta_label, alpha_arc, alpha_label)
        self.play(corner_group.animate.scale(0.75).to_edge(LEFT))

        # Use the extra space to derive the equation
        # Start with Rtheta = ralpha
        arc_length_equation = MathTex("R\\theta = r\\alpha").to_edge(UP)
        arc_length_equation.scale(0.75)
        arc_length_equation.shift(RIGHT * 2.5)
        self.play(Write(arc_length_equation))
        self.wait(1)

        # Show the relationship between theta and alpha
        relation = MathTex("\\alpha = \\frac{R\\theta}{r}").next_to(arc_length_equation, DOWN, buff=1)
        relation.scale(0.75)
        self.play(Write(relation))
        self.wait(1)

        # Derive the x(t) and y(t) equations
        x_equation = MathTex("x(\\theta) = (R + r)\\cos(\\theta) - r\\cos\\left(\\theta + \\alpha)").next_to(relation, DOWN, buff=1)
        x_equation.scale(0.75)
        self.play(Write(x_equation))
        self.wait(1)
        
       # Identify and create a copy of the alpha symbol from the relation equation
        alpha_in_relation = relation[0][0].copy()  # The alpha symbol in the relation equation

        # Move the alpha symbol to the alpha in the x(t) equation
        self.play(alpha_in_relation.animate.move_to(x_equation[0][-2].get_center()))
        self.wait(1)

        # After moving, replace the alpha in the x(t) equation with the substituted expression
        alpha_substitute = relation[0][2:9].copy()  # Copy the substitution expression

        # Replace alpha in x_equation with the substitution
        x_equation_with_sub = MathTex("x(\\theta) = (R + r)\\cos(\\theta) - r\\cos\\left(\\theta + \\frac{R\\theta}{r}\\right)").move_to(x_equation)
        x_equation_with_sub.scale(0.75)
        # Match the parts and do the substitution without the alpha moving back
        self.play(FadeOut(alpha_in_relation))
        self.play(TransformMatchingTex(x_equation, x_equation_with_sub, transform_mismatches=True))
        self.wait(1)
        
        x_equation_final = MathTex("x(\\theta) = (R + r)\\cos(\\theta) - r\\cos\\left(\\frac{R+r}{r} \\cdot\\theta)").move_to(x_equation)
        x_equation_final.scale(0.75)
        self.play(TransformMatchingTex(x_equation_with_sub, x_equation_final, transform_mismatches=True))
        self.wait(1)
        box = SurroundingRectangle(x_equation_final, color=WHITE, buff=0.2)
        self.play(Create(box))
        self.wait(3)