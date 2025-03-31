# An exmple showing finite deformation of an orthotropic (composite) material in 2D
# Fiber direction is indicated in the plot as well as fiber rotation
# in the deformation process
# In uniaxial tension, orthotropic material will change the length,
# but it will also shear 
# Stiffer direction (fiber direction) tends to allign with the load direction that
# is indicated with arrows
#
# To create animation run: manim -pql orthoDef.py OrthotropicDeformation

from manim import *
import numpy as np

class OrthotropicDeformation(Scene):
    def construct(self):
        # Set background color to white
        self.camera.background_color = WHITE

        # Create the base rectangle that will be transformed
        trans_rect = Rectangle(width=4, height=2, color=BLACK)
        # trans_rect.shift(UP*0.5)
        
        # Create static dashed rectangle with smaller, denser dashes
        static_rect = DashedVMobject(
            trans_rect.copy(),
            num_dashes=70,
            dashed_ratio=0.6,
            stroke_width=1
        ).set_stroke(color=GRAY)

        arrow_offset = 0.2

        # Compute original midpoints for arrows
        old_center = trans_rect.get_center()
        old_left_mid = old_center - np.array([trans_rect.width/2 + arrow_offset, 0, 0]) 
        old_right_mid = old_center + np.array([trans_rect.width/2 + arrow_offset, 0, 0])
        
        # Create arrows with initial positions
        left_arrow = Arrow(
            start=old_left_mid,
            end=old_left_mid + 0.7*LEFT,
            color=BLUE,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15
        )

        right_arrow = Arrow(
            start=old_right_mid,
            end=old_right_mid + 0.7*RIGHT,
            color=BLUE,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Calculate 45° endpoints within the rectangle
        center = trans_rect.get_center()
        diag_vector = UP + RIGHT
        start_point = center + diag_vector
        end_point = center - diag_vector
        
        # Create fibers at 45° angle
        green_fiber = Line(start_point, end_point, stroke_width=4, color=GREEN)
        red_fiber = green_fiber.copy().set_color(RED)
        
        # Create legend with black text
        legend_green = Line(ORIGIN, RIGHT*0.5, color=GREEN, stroke_width=2)
        legend_red = Line(ORIGIN, RIGHT*0.5, color=RED, stroke_width=2)

        # Pair each line with its corresponding text
        legend_green_group = VGroup(legend_green, Tex("current fiber", color=BLACK, font_size=30).next_to(legend_green, RIGHT, buff=0.2))
        legend_red_group = VGroup(legend_red, Tex("initial fiber", color=BLACK, font_size=30).next_to(legend_red, RIGHT, buff=0.2))

        # Arrange these pairs vertically
        legend = VGroup(legend_green_group, legend_red_group).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Move the legend to the upper-right corner
        legend.to_corner(UR, buff=0.5)
        
        # Shear transformation matrix
        shear_matrix = np.array([
            [1.2, 0, 0],
            [-0.1, .8, 0],
            [0, 0, 1]
        ])

        # Group transformable objects
        transform_group = VGroup(trans_rect, green_fiber)

        # Add all elements to scene
        self.add(static_rect, red_fiber, legend)
        self.add(transform_group)
        self.add(left_arrow, right_arrow)

        # Create a ValueTracker to drive the interpolation from 0 to 1
        alpha_tracker = ValueTracker(0)
        
        # Define an updater function for an arrow so it follows the shear transformation
        def update_arrow(arrow, original_start):
            alpha = alpha_tracker.get_value()
            # Interpolate between the original start and its sheared position
            new_start = (1 - alpha) * original_start + alpha * (shear_matrix @ original_start)
            # Keep the arrow horizontal by adding the constant offset (LEFT or RIGHT)
            if np.allclose(original_start, old_left_mid):
                offset = 0.7*LEFT
            else:
                offset = 0.7*RIGHT
            new_end = new_start + offset
            arrow.put_start_and_end_on(new_start, new_end)
        
        # Attach updaters to the arrows
        left_arrow.add_updater(lambda mob, dt: update_arrow(mob, old_left_mid))
        right_arrow.add_updater(lambda mob, dt: update_arrow(mob, old_right_mid))

        # Apply shear transformation
        self.play(
            alpha_tracker.animate.set_value(1),
            transform_group.animate.apply_matrix(shear_matrix), 
            run_time=4)

        # Remove updaters so arrows stay fixed in their final positions
        left_arrow.clear_updaters()
        right_arrow.clear_updaters()

        self.wait(.5)

        # Create angle between fibers (from red to green)
        angle = Angle(red_fiber, green_fiber, radius=0.4, color=BLACK, other_angle=True, stroke_width=2)
        angle_label = MathTex(r"\phi", color=BLACK, font_size=30).next_to(angle, UL*0.1)
        
        self.play(Create(angle), Write(angle_label))
        self.wait(4)