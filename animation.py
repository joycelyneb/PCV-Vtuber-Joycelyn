import math
import numpy as np
import cv2

# logika napas idle animation
def calculate_breath_offset(frame_counter, breath_speed, breath_amplitude):
    return int(math.sin(frame_counter * breath_speed) * breath_amplitude)

# logika transisi background
def update_background_transition(is_transitioning, transition_alpha, transition_speed, 
                                  bg_prev, bg_next):
    if is_transitioning and bg_prev is not None and bg_next is not None:
        transition_alpha += transition_speed
        
        if transition_alpha >= 1.0:
            transition_alpha = 1.0
            is_transitioning = False
            bg_render_target = bg_next.copy()
            return bg_render_target, is_transitioning, transition_alpha, bg_next
        else:
            # campur BG lama dan BG baru dengan fade
            bg_render_target = cv2.addWeighted(bg_next, transition_alpha, bg_prev, 1.0 - transition_alpha, 0)
            return bg_render_target, is_transitioning, transition_alpha, None
    else:
        return None, is_transitioning, transition_alpha, None

#composting avatar
def render_avatar(canvas, body_img, head_img, body_x, body_y, head_x, head_y):
    from image_utils import overlay_png
    
    # tempel body
    canvas = overlay_png(canvas, body_img, body_x, body_y)
    
    # tempel head
    canvas = overlay_png(canvas, head_img, head_x, head_y)
    
    return canvas