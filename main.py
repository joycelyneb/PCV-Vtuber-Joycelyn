import cv2
import mediapipe as mp
import numpy as np
import os
from config import *
from asset_loader import load_all_assets, load_background_by_index
from detection import detect_face_expression, detect_body_pose
from animation import calculate_breath_offset, update_background_transition, render_avatar
from image_utils import overlay_png

# --- INIT MEDIAPIPE ---
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

holistic = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    refine_face_landmarks=True
)

# --- LOAD ASSETS ---
assets, ref_body_h, ref_body_w, ref_head_h, ref_head_w = load_all_assets(
    TARGET_BODY_HEIGHT, HEAD_SCALE_FACTOR
)

if assets is None:
    exit()

# --- SETUP CANVAS ---
STATIC_CANVAS_H = ref_body_h + DYNAMIC_TOP_MARGIN
STATIC_CANVAS_W = ref_body_w + EXTRA_CANVAS_WIDTH

# --- LOAD BACKGROUND AWAL ---
background_image = load_background_by_index(0, STATIC_CANVAS_W, STATIC_CANVAS_H, BACKGROUND_FILES)
if background_image is None:
    print("Info: Background awal tidak ditemukan. Pakai hitam.")
    background_image = np.zeros((STATIC_CANVAS_H, STATIC_CANVAS_W, 4), dtype=np.uint8)
    background_image[:, :, 3] = 255

print("Sistem Siap! Tekan 'C' untuk ganti BG dengan Animasi Fade.")

# --- STATE VARIABLES ---
current_bg_index = 0
is_bg_transitioning = False
bg_transition_alpha = 0.0
bg_prev_image = None
bg_next_image = None
frame_counter = 0

# --- MAIN LOOP ---
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: 
        break
    
    # --- INPUT HANDLING ---
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c') or key == ord('C'):
        if not is_bg_transitioning:
            next_bg_candidate = load_background_by_index(
                current_bg_index + 1, STATIC_CANVAS_W, STATIC_CANVAS_H, BACKGROUND_FILES
            )
            
            if next_bg_candidate is not None:
                bg_prev_image = background_image.copy()
                bg_next_image = next_bg_candidate
                current_bg_index += 1
                bg_transition_alpha = 0.0
                is_bg_transitioning = True
                print(f"Start Transition -> BG {current_bg_index}")

    # --- PROCESS FRAME ---
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(rgb_frame)
    
    # --- FACE EXPRESSION DETECTION ---
    current_head_key = "head_normal"
    status_text = "NORMAL"
    
    if results.face_landmarks:
        current_head_key, status_text = detect_face_expression(
            results.face_landmarks, w, h, assets
        )

    # --- BODY POSE DETECTION ---
    detected_pose_key = "body_normal"
    
    if results.pose_landmarks:
        detected_pose_key = detect_body_pose(
            results.pose_landmarks, 
            results.left_hand_landmarks, 
            results.right_hand_landmarks
        )

    # --- IDLE ANIMATION (BREATH) ---
    frame_counter += 1
    breath_offset = calculate_breath_offset(frame_counter, BREATH_SPEED, BREATH_AMPLITUDE)

    # --- BACKGROUND TRANSITION ANIMATION ---
    bg_render_target, is_bg_transitioning, bg_transition_alpha, bg_updated = update_background_transition(
        is_bg_transitioning, bg_transition_alpha, TRANSITION_SPEED, bg_prev_image, bg_next_image
    )
    
    if bg_updated is not None:
        background_image = bg_updated
    
    if bg_render_target is None:
        if background_image is not None:
            bg_render_target = background_image.copy()
        else:
            bg_render_target = np.zeros((STATIC_CANVAS_H, STATIC_CANVAS_W, 4), dtype=np.uint8)

    # --- RENDER AVATAR ---
    avatar_output = bg_render_target
    current_body_img = assets.get(detected_pose_key, assets["body_normal"])
    current_head_img = assets.get(current_head_key, assets["head_normal"])
    
    body_x_centered = (STATIC_CANVAS_W - current_body_img.shape[1]) // 2
    avatar_output = overlay_png(avatar_output, current_body_img, body_x_centered, DYNAMIC_TOP_MARGIN + breath_offset)

    center_body_visual_x = body_x_centered + (current_body_img.shape[1] // 2)
    head_x = center_body_visual_x - (current_head_img.shape[1] // 2) + HEAD_OFFSET_X
    head_y = DYNAMIC_TOP_MARGIN + HEAD_OFFSET_Y + breath_offset
    avatar_output = overlay_png(avatar_output, current_head_img, head_x, head_y)

    # --- DRAW LANDMARKS ON CAMERA FRAME ---
    mp_drawing.draw_landmarks(
        frame, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
        landmark_drawing_spec=None, 
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
    )
    mp_drawing.draw_landmarks(
        frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
    )
    mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

    # --- DISPLAY TEXT ---
    cv2.putText(frame, f"Pose: {detected_pose_key}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    cv2.putText(frame, f"{status_text}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # --- SHOW WINDOWS ---
    cv2.imshow("Camera Debug (Tracker)", frame)
    cv2.imshow("VTuber Avatar", avatar_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()