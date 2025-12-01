import numpy as np
import cv2
from config import (
    MAR_THRESHOLD_100, MAR_THRESHOLD_75, MAR_THRESHOLD_50, MAR_THRESHOLD_25,
    EAR_THRESHOLD_BLINK
)
from geometry_utils import calculate_mar, calculate_ear
from gesture_detection import detect_hand_sign

# peta titik landmark wajah untuk mata
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def detect_face_expression(face_landmarks, frame_w, frame_h, assets):
    lm_points = np.array([(int(l.x * frame_w), int(l.y * frame_h)) for l in face_landmarks.landmark])
    mar = calculate_mar(lm_points)
    left_ear = calculate_ear(lm_points, LEFT_EYE)
    right_ear = calculate_ear(lm_points, RIGHT_EYE)
    
    nose_tip = lm_points[1]
    left_cheek = lm_points[234]
    right_cheek = lm_points[454]
    
    face_center_x = (left_cheek[0] + right_cheek[0]) // 2
    head_turn_ratio = (nose_tip[0] - face_center_x) / (right_cheek[0] - left_cheek[0])
    
    blink_left = left_ear < EAR_THRESHOLD_BLINK
    blink_right = right_ear < EAR_THRESHOLD_BLINK
    
    if blink_left or blink_right: 
        return "head_blink_both", "BLINK"
    elif mar > MAR_THRESHOLD_100:
        return "head_m100", "MOUTH 100%"
    elif mar > MAR_THRESHOLD_75:
        return "head_m75", "MOUTH 75%"
    elif mar > MAR_THRESHOLD_50:
        return "head_m50", "MOUTH 50%"
    elif mar > MAR_THRESHOLD_25:
        return "head_m25", "MOUTH 25%"
    elif head_turn_ratio > 0.15 and "head_right" in assets: 
        return "head_right", "TURN RIGHT"
    elif head_turn_ratio < -0.15 and "head_left" in assets: 
        return "head_left", "TURN LEFT"
    
    return "head_normal", "NORMAL"

def detect_body_pose(pose_landmarks, left_hand_landmarks, right_hand_landmarks):

    lm = pose_landmarks.landmark
    left_wrist = lm[15]
    right_wrist = lm[16]
    left_shoulder = lm[11]
    right_shoulder = lm[12]

    is_left_up = left_wrist.y < left_shoulder.y
    is_right_up = right_wrist.y < right_shoulder.y
    
    left_gesture = detect_hand_sign(left_hand_landmarks)
    right_gesture = detect_hand_sign(right_hand_landmarks)
    
    # deteksi gesture tangan
    if left_gesture == "peace" and right_gesture == "peace": 
        return "body_peace_both"
    elif left_gesture == "point" and right_gesture == "point": 
        return "body_point_both"
    elif left_gesture == "thumb" and right_gesture == "thumb": 
        return "body_thumb_both"
    elif left_gesture == "peace": 
        return "body_peace_right"
    elif right_gesture == "peace": 
        return "body_peace_left"
    elif left_gesture == "point": 
        return "body_point_right"
    elif right_gesture == "point": 
        return "body_point_left"
    elif left_gesture == "thumb": 
        return "body_thumb_right"
    elif right_gesture == "thumb": 
        return "body_thumb_left"
    elif is_left_up and is_right_up: 
        return "body_up_both"
    elif is_left_up: 
        return "body_up_right"
    elif is_right_up: 
        return "body_up_left"
    
    return "body_normal"