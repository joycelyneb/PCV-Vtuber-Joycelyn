import math

# --- GEOMETRY UTILS ---
def euclidean_distance(point1, point2):
    """Hitung jarak Euclidean antara dua titik"""
    x1, y1 = point1.ravel()
    x2, y2 = point2.ravel()
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_mar(landmarks):
    """Hitung Mouth Aspect Ratio dari face landmarks"""
    top_lip = landmarks[13]
    bottom_lip = landmarks[14]
    left_corner = landmarks[61]
    right_corner = landmarks[291]
    vertical = euclidean_distance(top_lip, bottom_lip)
    horizontal = euclidean_distance(left_corner, right_corner)
    if horizontal == 0: 
        return 0
    return vertical / horizontal

def calculate_ear(landmarks, indices):
    """Hitung Eye Aspect Ratio dari face landmarks"""
    v1 = euclidean_distance(landmarks[indices[1]], landmarks[indices[5]])
    v2 = euclidean_distance(landmarks[indices[2]], landmarks[indices[4]])
    hor = euclidean_distance(landmarks[indices[0]], landmarks[indices[3]])
    if hor == 0: 
        return 0
    return (v1 + v2) / (2.0 * hor)