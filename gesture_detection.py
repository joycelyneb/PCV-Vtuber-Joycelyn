import math

# --- HAND GESTURE DETECTION ---
def detect_hand_sign(hand_landmarks):
    """Deteksi gesture tangan (peace, point, thumb, open)"""
    if not hand_landmarks: 
        return None
    
    tips = [4, 8, 12, 16, 20]
    pips = [2, 5, 9, 13, 17]
    
    fingers_up = []
    thumb_tip = hand_landmarks.landmark[4]
    index_base = hand_landmarks.landmark[5]
    pinky_base = hand_landmarks.landmark[17]
    
    dist_thumb_pinky = math.hypot(thumb_tip.x - pinky_base.x, thumb_tip.y - pinky_base.y)
    dist_index_pinky = math.hypot(index_base.x - pinky_base.x, index_base.y - pinky_base.y)
    thumb_up = dist_thumb_pinky > dist_index_pinky * 1.2
    
    fingers_up.append(thumb_up)

    for i in range(1, 5):
        tip = hand_landmarks.landmark[tips[i]]
        pip = hand_landmarks.landmark[pips[i]]
        fingers_up.append(tip.y < pip.y) 

    if fingers_up[1] and fingers_up[2] and not fingers_up[3] and not fingers_up[4]:
        return "peace"
    if fingers_up[1] and not fingers_up[2] and not fingers_up[3] and not fingers_up[4]:
        return "point"
    if fingers_up[0] and not fingers_up[1] and not fingers_up[2] and not fingers_up[3]:
        return "thumb"
    return "open"
