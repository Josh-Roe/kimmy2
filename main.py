from manim import *

class EpitrochoidDerivation(Scene):
    def construct(self):
        # Define the circles' radii
        R = 3  # Radius of the fixed circle
        r = 1  # Radius of the rolling circle

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
        alpha_arc = Arc(radius=0.3, start_angle=-PI/6, angle=-alpha, arc_center=center_rolling, color=WHITE)
        alpha_label = MathTex("\\alpha").next_to(alpha_arc, DOWN, buff=0.1)
        alpha_label.shift(RIGHT*0.3)
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
                # Create a dotted line triangle connecting the centers of both circles and the point on the rolling circle
        rolling_tip = fixed_circle.get_center() + np.array([(R+r)*0.75 * np.cos(theta), 0, 0])
        center_fixed = fixed_circle.get_center()
        center_rolling = rolling_circle.get_center()
        triangle_lines = VGroup(
            DashedLine(center_fixed, rolling_tip, color=WHITE),
            DashedLine(center_rolling, rolling_tip, color=WHITE)
        )
        self.play(Create(triangle_lines))
        self.wait(2)
        Rrcos = MathTex("(R + r)\\cos(\\theta)").next_to(triangle_lines, DOWN, buff=-0.01)
        Rrcos.scale(0.5)
        Rrcos.shift(RIGHT*0.3)
        R_target = Rrcos[0][1]  # The position of R in (R + r)
        r_target = Rrcos[0][3]  # The position of r in (R + r)
        R_label_new = R_label.copy()
        r_label_new = r_label.copy()
        R_label_new.scale(0.5/0.75)
        r_label_new.scale(0.5/0.75)
        self.play(R_label_new.animate.move_to(R_target), r_label_new.animate.move_to(r_target),
                  Write(Rrcos)
                  )
        self.wait(1)
        R_label_new.set_opacity(0)
        r_label_new.set_opacity(0)
        
        Rrsin = MathTex("(R + r)\\sin(\\theta)").next_to(triangle_lines, RIGHT, buff=-0.6)
        Rrsin.scale(0.5)
        Rrsin.shift(DOWN*0.3)
        R_target = Rrsin[0][1]  # The position of R in (R + r)
        r_target = Rrsin[0][3]  # The position of r in (R + r)
        R_label_new = R_label.copy()
        r_label_new = r_label.copy()
        R_label_new.scale(0.5/0.75)
        r_label_new.scale(0.5/0.75)
        self.play(R_label_new.animate.move_to(R_target), r_label_new.animate.move_to(r_target),
                  Write(Rrsin)
                  )
        self.wait(1)
        R_label_new.set_opacity(0)
        r_label_new.set_opacity(0)

        # Derive the x(t) and y(t) equations
        x_equation = MathTex("x(\\theta) = ").next_to(relation, DOWN, buff=2)
        x_equation.scale(0.75)
        y_equation = MathTex("y(\\theta) = ").next_to(x_equation, DOWN, buff=1)
        y_equation.scale(0.75)
        x_equation.shift(LEFT*3)
        y_equation.shift(LEFT*3)
        self.play(Write(x_equation), Write(y_equation))
        self.wait(1)
        # Animate R and r labels moving to the equation
        self.play(Rrcos.animate.scale(1.5), Rrsin.animate.scale(1.5))
        self.play(Rrcos.animate.next_to(x_equation), Rrsin.animate.next_to(y_equation))
        self.wait(1)
        self.play(FadeOut(triangle_lines))
        
        new_radius_r = radius_r.copy()
        self.play(new_radius_r.animate.rotate(5*PI/6, about_point=center_rolling))
        self.play(r_label.animate.next_to(new_radius_r, UP, buff=0.06))
        
        
        
        rolling_tip2 = fixed_circle.get_center() + np.array([0, (R+r)*0.75 * np.sin(theta), 0])
        center_fixed = fixed_circle.get_center()
        center_rolling = rolling_circle.get_center()
        triangle_lines2 = VGroup(
            DashedLine(center_fixed, rolling_tip2, color=WHITE),
            DashedLine(center_rolling, rolling_tip2, color=WHITE)
        )
        self.play(Create(triangle_lines2))
        self.wait(2)
        
        new_theta_arc = Arc(radius=0.3*0.75, start_angle=-5*PI/6, angle=-theta, arc_center=center_rolling, color=YELLOW)
        
        alphaandtheta = MathTex("\\theta + \\alpha")
        alphaandtheta.move_to(alpha_label)
        alphaandtheta.scale(0.5)
        self.play(FadeOut(radius_r),Create(new_theta_arc))
        self.play(ReplacementTransform(alpha_label, alphaandtheta))
        self.play(alphaandtheta.animate.next_to(alpha_arc, DOWN, buff=0.1))
        rolling_edge = rolling_circle.get_center() + np.array([r*0.75 * np.cos(-PI/6), r*0.75*np.sin(-PI/6), 0])
        rolling_edge2 = rolling_circle.get_center() + np.array([r*0.75 * np.cos(-PI/6), 0, 0])
        newline = Line(center_rolling, rolling_edge, color=GREEN)
        newline2 = Line(rolling_edge, rolling_edge2, color=GREEN)
        self.play(Create(newline), Create(newline2))
        
        angle_center = rolling_circle.get_center() + np.array([0.2 * np.cos(-PI/12), 0.2 * np.sin(-PI/12), 0])
        angle_end = rolling_circle.get_center() + np.array([np.cos(PI/3),np.sin(PI/3), 0])
        angleline = Line(angle_center, angle_end, color=WHITE, stroke_width=1)
        self.play(Create(angleline))
        
        angle_text = MathTex("\\pi - \\theta - \\alpha").next_to(angleline, UP, buff=0.1)
        angle_text.scale(0.75)
        self.play(Write(angle_text))
        
        x_add = MathTex(r"+\, r\cos\left(\pi - \theta - \alpha\right)").next_to(Rrcos, RIGHT, buff=-0.4)
        y_add = MathTex(r"-\, r\sin\left(\pi - \theta - \alpha\right)").next_to(Rrsin, RIGHT, buff=-0.4)

        x_add.scale(0.75)
        y_add.scale(0.75)
        newrlabel = r_label.copy()
        newrlabel2 = r_label.copy()
        newangle = angle_text.copy()
        newangle2 = angle_text.copy()
        self.play(Write(x_add), Write(y_add), newrlabel.animate.move_to(x_add[0][1]), newrlabel2.animate.move_to(y_add[0][1]), newangle.animate.move_to(x_add[0][8]), newangle2.animate.move_to(y_add[0][8]))

        newrlabel.set_opacity(0)
        newrlabel2.set_opacity(0)
        newangle.set_opacity(0)
        newangle2.set_opacity(0)
        x_add2 = MathTex(r"+\, r\cos\left(\theta + \alpha - \pi\right)").move_to(x_add)
        y_add2 = MathTex(r"+\, r\sin\left(\theta + \alpha - \pi\right)").move_to(y_add)
        x_add2.scale(0.75)
        y_add2.scale(0.75)
        
        self.play(Transform(x_add, x_add2), Transform(y_add, y_add2))
        
        x_add3 = MathTex(r"-\, r\cos\left(\theta + \alpha\right)").next_to(Rrcos, RIGHT, buff=-0.29)
        y_add3 = MathTex(r"-\, r\sin\left(\theta + \alpha\right)").next_to(Rrsin, RIGHT, buff=-0.29)
        x_add3.scale(0.75)
        y_add3.scale(0.75)
        x_add.set_opacity(0)
        y_add.set_opacity(0)
        self.play(Transform(x_add2, x_add3), Transform(y_add2, y_add3))
        
        # Identify and create a copy of the alpha symbol from the relation equation
        alpha_in_relation = relation[0][0].copy()  # The alpha symbol in the relation equation
        alpha_in_relation2 = relation[0][0].copy()
        # Move the alpha symbol to the alpha in the x(t) equation
        self.play(alpha_in_relation.animate.move_to(x_add3[0][-2].get_center()), alpha_in_relation2.animate.move_to(y_add3[0][-2].get_center()))
        alpha_in_relation.set_opacity(0)
        alpha_in_relation2.set_opacity(0)
        self.wait(1)
        x_add4 = MathTex(r"-\, r\cos\left(\theta + \frac{R\theta}{r}\right)").next_to(Rrcos, RIGHT, buff=-0.29)
        y_add4 = MathTex(r"-\, r\sin\left(\theta + \frac{R\theta}{r}\right)").next_to(Rrsin, RIGHT, buff=-0.29)
        x_add4.scale(0.75)
        y_add4.scale(0.75)
        x_add2.set_opacity(0)
        y_add2.set_opacity(0)
        self.play(Transform(x_add3, x_add4), Transform(y_add3, y_add4))
        
        x_add5 = MathTex(r"-\, r\cos\left(\frac{R+r}{r}\cdot\theta)").next_to(Rrcos, RIGHT, buff=-0.29)
        y_add5 = MathTex(r"-\, r\sin\left(\frac{R+r}{r}\cdot\theta)").next_to(Rrsin, RIGHT, buff=-0.29)
        x_add5.scale(0.75)
        y_add5.scale(0.75)
        x_add3.set_opacity(0)
        y_add3.set_opacity(0)
        self.play(Transform(x_add4, x_add5), Transform(y_add4, y_add5))
        
        self.play(FadeOut(newline), FadeOut(newline2), FadeOut(angleline), FadeOut(angle_text), FadeOut(alphaandtheta), FadeOut(new_theta_arc), FadeOut(triangle_lines2), FadeOut(r_label), FadeOut(alpha_arc), FadeOut(new_radius_r), FadeOut(fixed_arc), FadeOut(rolling_arc))

        d_line = Line(center_rolling, center_rolling + [1,0,0], color=WHITE)
        self.play(Create(d_line))
        d_text = MathTex("d").next_to(d_line, RIGHT, buff=0.3)
        self.play(Write(d_text))
        self.play(
            UpdateFromAlphaFunc(d_line, lambda l, alpha: l.put_start_and_end_on(
                center_rolling,
                center_rolling + 1 * np.array([np.cos(2 * PI * alpha), np.sin(2 * PI * alpha), 0])
            )),
            run_time=4  # Adjust the runtime for the speed of rotation
        )
        newdtext = d_text.copy()
        newdtext2 = d_text.copy()
        newdtext.scale(0.75)
        newdtext2.scale(0.75)
        self.play(FadeOut(d_line))
        x_add6 = MathTex(r"-\, d\cos\left(\frac{R+r}{r}\cdot\theta)").next_to(Rrcos, RIGHT, buff=-0.29)
        y_add6 = MathTex(r"-\, d\sin\left(\frac{R+r}{r}\cdot\theta)").next_to(Rrsin, RIGHT, buff=-0.29)
        x_add6.scale(0.75)
        y_add6.scale(0.75)
        x_add4.set_opacity(0)
        y_add4.set_opacity(0)
        self.play(Transform(x_add5,x_add6),Transform(y_add5,y_add6),newdtext.animate.move_to(x_add5[0][1]), newdtext2.animate.move_to(y_add5[0][1]))
        newdtext.set_opacity(0)
        newdtext2.set_opacity(0)
        finalsigmagroup = VGroup(x_equation, y_equation, x_add5, y_add5, Rrcos, Rrsin)
        box = SurroundingRectangle(finalsigmagroup, color=WHITE, buff=0.2)
        self.play(Create(box))
        self.wait(3)
