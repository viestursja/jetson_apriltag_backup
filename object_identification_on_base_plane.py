# to identify coordintes of test april tag 
# use two other files - get cornesrs_coordinates.py and get_test_object_coordinates.py


import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from get_corners_coordinates import get_corner_coordinates
from get_test_object_coordinates import get_test_oject_coordinates


W = 74
H = 49

# coordintaes of the corners
# corners_dict = {'ll': [51, 447], 'lr': [605, 443], 'ur': [453, 64], 'ul': [167, 63]}
corners_dict = get_corner_coordinates()

# pionts in image
src_points = np.array([
    corners_dict['ll'], 
    corners_dict['lr'], 
    corners_dict['ur'], 
    corners_dict['ul'] 

], dtype=np.float32
)

# points in Cortesian xy system
dst_points = np.array([
    [0, 0],     # Lower-left corner
    [W, 0],     # Lower-right corner
    [W, H],     # Upper-right corner
    [0, H]      # Upper-left corner
], dtype=np.float32)

# perspective trabsformation
matrix = cv.getPerspectiveTransform(src_points, dst_points)

def transform_point(px, py):
    point = np.array([[px, py]], dtype=np.float32)
    point = np.array([point])
    transformed_point = cv.perspectiveTransform(point, matrix)
    return transformed_point[0][0]

# px, py = 290, 256 # Replace with the  pixel coordinates to transform
px, py = get_test_oject_coordinates()
new_x, new_y = transform_point(px, py)
print(f"Transformed coordinates: ({int(new_x)}, {int(new_y)})")

plt.figure(figsize=(10, 6))
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)

cartesian_square = np.array([
    [0, 0],     # Lower-left corner
    [W, 0],     # Lower-right corner
    [W, H],     # Upper-right corner
    [0, H]      # Upper-left corner
])
plt.plot(cartesian_square[:, 0], cartesian_square[:, 1], 'b-')

plt.plot(new_x, new_y, 'ro', label=f'Coordinates ({new_x:.2f}, {new_y:.2f})')

# Set labels and title
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
# plt.title('Point in Cartesian Coordinate System')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()