import math

# RUMUS DASAR
def euclidean_distance(point1, point2):
    x1, y1 = point1.ravel()
    x2, y2 = point2.ravel()
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# ngukur MAR mouth aspect ratio
def calculate_mar(landmarks):
    top_lip = landmarks[13]
    bottom_lip = landmarks[14]
    left_corner = landmarks[61]
    right_corner = landmarks[291]
    vertical = euclidean_distance(top_lip, bottom_lip)
    horizontal = euclidean_distance(left_corner, right_corner)
    if horizontal == 0: 
        return 0
    return vertical / horizontal

# ngukur EAR eye aspect ratio
def calculate_ear(landmarks, indices):
    v1 = euclidean_distance(landmarks[indices[1]], landmarks[indices[5]])
    v2 = euclidean_distance(landmarks[indices[2]], landmarks[indices[4]])
    hor = euclidean_distance(landmarks[indices[0]], landmarks[indices[3]])
    if hor == 0: 
        return 0
    return (v1 + v2) / (2.0 * hor)