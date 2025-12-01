import cv2
import numpy as np
import math

# --- FUNGSI IMAGE PROCESSING ---
def resize_keep_aspect(image, target_dim, is_height=True):
    """Resize gambar dengan mempertahankan aspect ratio"""
    if image is None: 
        return None
    (h, w) = image.shape[:2]
    if is_height:
        aspect_ratio = w / h
        new_h = target_dim
        new_w = int(new_h * aspect_ratio)
    else:
        aspect_ratio = h / w
        new_w = target_dim
        new_h = int(new_w * aspect_ratio)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized

def overlay_png(bg, fg, x_offset, y_offset):
    """Overlay foreground PNG (with alpha) ke background"""
    if fg is None or bg is None: 
        return bg
    bg = bg.copy()
    
    if fg.shape[2] == 3:
        fg = cv2.cvtColor(fg, cv2.COLOR_BGR2BGRA)

    bg_h, bg_w, _ = bg.shape
    fg_h, fg_w, _ = fg.shape

    y1, y2 = max(0, y_offset), min(bg_h, y_offset + fg_h)
    x1, x2 = max(0, x_offset), min(bg_w, x_offset + fg_w)

    fg_y1 = max(0, -y_offset)
    fg_y2 = fg_y1 + (y2 - y1)
    fg_x1 = max(0, -x_offset)
    fg_x2 = fg_x1 + (x2 - x1)

    if y1 >= y2 or x1 >= x2 or fg_y1 >= fg_y2 or fg_x1 >= fg_x2:
        return bg

    fg_cropped = fg[fg_y1:fg_y2, fg_x1:fg_x2]
    roi = bg[y1:y2, x1:x2]

    if roi.shape[:2] != fg_cropped.shape[:2]:
        fg_cropped = cv2.resize(fg_cropped, (roi.shape[1], roi.shape[0]))

    alpha = fg_cropped[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha

    for c in range(0, 3):
        roi[:, :, c] = (alpha * fg_cropped[:, :, c] + alpha_inv * roi[:, :, c])
    
    if bg.shape[2] == 4:
        roi[:, :, 3] = np.maximum(roi[:, :, 3], fg_cropped[:, :, 3])

    bg[y1:y2, x1:x2] = roi
    return bg
