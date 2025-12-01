import cv2
import numpy as np
import os
from image_utils import resize_keep_aspect

# --- ASSET MAPPINGS ---
FILE_MAP_HEAD = {
    "head_normal": "face_neutral.png",
    "head_happy": "face_happy.png",
    "head_blink_both": "eyes_closed_both.png",
    "head_smiling": "face_smiling.png",
    "head_left": "head_left.png",
    "head_right": "head_right.png",
    "head_m25": "mouth_O_25.png",
    "head_m50": "mouth_O_50.png",
    "head_m75": "mouth_O_75.png",
    "head_m100": "mouth_O_100.png"
}

FILE_MAP_BODY = {
    "body_normal": "body_normal.png",
    "body_up_both": "hand_up_both.png",
    "body_up_left": "hand_up_left.png",
    "body_up_right": "hand_up_right.png",
    "body_peace_left": "hand_peace_left.png",
    "body_peace_right": "hand_peace_right.png",
    "body_peace_both": "hand_peace_both.png",
    "body_point_left": "hand_point_left.png",
    "body_point_right": "hand_point_right.png",
    "body_point_both": "hand_point_both.png",
    "body_thumb_left": "hand_tumbsup_left.png", 
    "body_thumb_right": "hand_thumbsup_right.png",
    "body_thumb_both": "hand_thumbsup_both.png"
}

def load_asset(filename, scale_size=None, is_height=True):
    """Load PNG asset dari folder assets"""
    path = os.path.join("assets", filename)
    if not os.path.exists(path): 
        path = filename
    if not os.path.exists(path):
        return None
    
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
    
    if scale_size is not None:
        img = resize_keep_aspect(img, scale_size, is_height=is_height)
    
    return img

def load_all_assets(target_body_height, head_scale_factor):
    """Load semua aset (kepala, badan, background)"""
    print("Memuat aset...")
    assets = {}
    
    # --- LOAD BODY NORMAL TERLEBIH DAHULU ---
    path_body = os.path.join("assets", FILE_MAP_BODY["body_normal"])
    if not os.path.exists(path_body):
        path_body = FILE_MAP_BODY["body_normal"]
        if not os.path.exists(path_body):
            if os.path.exists("body_straight-removebg-preview.png"):
                path_body = "body_straight-removebg-preview.png"
            elif os.path.exists("assets/body_straight-removebg-preview.png"):
                path_body = "assets/body_straight-removebg-preview.png"
            else:
                print("CRITICAL ERROR: body_normal.png tidak ditemukan!")
                return None, 0, 0, 0, 0

    img_body_ref = cv2.imread(path_body, cv2.IMREAD_UNCHANGED)
    assets["body_normal"] = resize_keep_aspect(img_body_ref, target_body_height, is_height=True)
    ref_body_h, ref_body_w = assets["body_normal"].shape[:2]

    # --- LOAD SISA BODY ---
    for key, filename in FILE_MAP_BODY.items():
        if key == "body_normal": 
            continue
        path = os.path.join("assets", filename)
        if not os.path.exists(path): 
            path = filename
        if os.path.exists(path):
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            assets[key] = resize_keep_aspect(img, target_body_height, is_height=True)
        else:
            assets[key] = assets["body_normal"]

    # --- LOAD KEPALA ---
    ref_head_w, ref_head_h = 0, 0
    for key, filename in FILE_MAP_HEAD.items():
        path = os.path.join("assets", filename)
        if not os.path.exists(path): 
            path = filename
        if os.path.exists(path):
            img_head = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if key == "head_normal": 
                target_head_w = int(ref_body_w * head_scale_factor)
                assets[key] = resize_keep_aspect(img_head, target_head_w, is_height=False)
                ref_head_h, ref_head_w = assets[key].shape[:2] 
            else: 
                if ref_head_w > 0:
                    assets[key] = cv2.resize(img_head, (ref_head_w, ref_head_h), interpolation=cv2.INTER_AREA)
                else:
                    assets[key] = img_head
        else:
            if "head_normal" in assets:
                assets[key] = assets["head_normal"]

    return assets, ref_body_h, ref_body_w, ref_head_h, ref_head_w

def load_background_by_index(idx, w_target, h_target, background_files):
    """Load background gambar dengan resize crop ke canvas size"""
    if not background_files: 
        return None
    
    fname = background_files[idx % len(background_files)]
    bg_path = os.path.join("assets", fname)
    if not os.path.exists(bg_path): 
        bg_path = fname 
    
    if not os.path.exists(bg_path):
        return None
    
    bg_img = cv2.imread(bg_path)
    if bg_img is None: 
        return None
    
    (h_orig, w_orig) = bg_img.shape[:2]
    ratio_bg = w_orig / h_orig
    ratio_canvas = w_target / h_target
    
    if ratio_bg > ratio_canvas:
        bg_img = resize_keep_aspect(bg_img, h_target, is_height=True)
        (h, w) = bg_img.shape[:2]
        sx = (w - w_target) // 2
        bg_img = bg_img[:, sx:sx+w_target]
    else:
        bg_img = resize_keep_aspect(bg_img, w_target, is_height=False)
        (h, w) = bg_img.shape[:2]
        sy = (h - h_target) // 2
        bg_img = bg_img[sy:sy+h_target, :]
        
    if bg_img.shape[2] == 3:
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)
    if bg_img.shape[:2] != (h_target, w_target):
        bg_img = cv2.resize(bg_img, (w_target, h_target))
    
    return bg_img
