

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import json
import math
# from get_corners_coordinates import get_corner_coordinates
# from get_test_object_coordinates import get_test_oject_coordinates
from B_lib_apriltag_identify_tags import identify_corner_coordinates

# run to create corners_coordinates.json
identify_corner_coordinates()

# field size
W = 621
H = 458
h = 480

print('Field transposition starts ......')
print('----------------------------------')
# coordinates of corners
with open('corners_coordinates.json', 'r') as f:
    corners_dict = json.load(f)

# corner pionts in image
src_points = np.array([
    corners_dict['ll'], 
    corners_dict['lr'], 
    corners_dict['ur'], 
    corners_dict['ul'] 
], dtype=np.float32
)

# points in Cortesian xy system - Field
dst_points = np.array([
    [0, 0],     # Lower-left corner
    [W, 0],     # Lower-right corner
    [W, H],     # Upper-right corner
    [0, H]      # Upper-left corner
], dtype=np.float32)

# perspective trabsformation towards corners
matrix = cv.getPerspectiveTransform(src_points, dst_points)

# function to transform coordinates from img to Field
def transform_point(px, py):
    point = np.array([[px, py]], dtype=np.float32)
    point = np.array([point])
    transformed_point = cv.perspectiveTransform(point, matrix)
    print(f'Transformed point {transformed_point}')
    return transformed_point[0][0]

# Box transformation
with open ('box_coordinates.json', 'r') as f:
    boxes = json.load(f)

box_0 = boxes['box_1']
corner_coordinates = []

# for box in box_0:
center_x, center_y, height, width, angle = box_0
center_y = h - center_y
x_min = (center_x - width / 2)
y_min = (center_y - height / 2)
x_max = (center_x + width / 2)
y_max = (center_y + height / 2)

# x - y pairs of corner cooredinates
x_points = [x_min, x_max, x_max, x_min, x_min]
y_points = [y_max, y_max, y_min, y_min, y_max]

# transform center
center_new = transform_point(center_x, center_y)
print(f'Center new coordinates: {center_new}')
print('------------------------------------')

#transformation of corners
x_points_transformed = []
y_points_transformed = []

for i in range(5):
    new_corner_i = transform_point(x_points[i], y_points[i])
    # print(f'New corner {i}, {new_corner_i.astype(int)}')
    # new_corner_i = new_corner_i.astype(int)
    new_corner_i = new_corner_i.tolist()
    x_points_transformed.append(new_corner_i[0])
    y_points_transformed.append(new_corner_i[1])

print(f'X points transformed: {x_points_transformed} ')
print(f'Y points transformed: {y_points_transformed} ')
print(f'Angle: {angle}')
print('----------------------')


#-----------------------Plot Original img -----------------------------
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


plt.plot(x_points, y_points, color='blue')
plt.plot(center_x, center_y, 'o', color='blue')


plt.title('Original Plane')
# plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
# ----------------------- Plot Transformed plane ----------------------------

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


# Plot rectangle using corner points
plt.plot(x_points_transformed,  y_points_transformed, color='blue')
plt.plot(center_new[0], center_new[1], 'o', color='blue')

# # rotated box
# plt.plot(x_points_rotated, y_points_rotated, color = 'g')

# Set labels and title
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Transformed Plane')
# plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()