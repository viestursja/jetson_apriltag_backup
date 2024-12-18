# to identify coordintes of test april tag 
# use two other files - get cornesrs_coordinates.py and get_test_object_coordinates.py


import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import json
from shapely.geometry import Polygon
from shapely.affinity import rotate
import math
# from get_corners_coordinates import get_corner_coordinates
# from get_test_object_coordinates import get_test_oject_coordinates
from B_lib_apriltag_identify_tags import identify_corner_coordinates

# run to create corners_coordinates.json
identify_corner_coordinates()

# field size
W = 621
H = -458

print('Object transposition starts ......')
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
    return transformed_point[0][0]

# Box transformation

with open ('box_coordinates.json', 'r') as f:
    boxes = json.load(f)

box_0 = boxes['box_2']
# print(f'box_0: {box_0}')

corner_coordinates = []
# for box in box_0:
center_x, center_y, height, width, angle = box_0
# center_y = center_y * (-1)
x_min = (center_x - width / 2)
y_min = (center_y - height / 2)
x_max = (center_x + width / 2)
y_max = (center_y + height / 2)
corner_coordinates.append([[x_min, y_min], [x_max, y_max]])

center_new = transform_point(center_x, center_y)
print(f'Center new coordinates: {center_new}')
# Corner coordinates: [[[164, 70], [243, 184]]]
print('--------------------------------------')
print(f'Xmin, Ymin; Xmax, Ymax: {corner_coordinates}')
print('--------------------------------------')
# corner transformation

x_min, y_min = corner_coordinates[0][0]
x_max, y_max = corner_coordinates[0][1]

# x - y pairs of corner cooredinates
x_points = [x_min, x_max, x_max, x_min]
y_points = [y_max, y_max, y_min, y_min]

print(f'X points original {(x_points)}')
print(f'Y points original {(y_points)}')
print('------------------')

#transformation of corners
x_points_transformed = []
y_points_transformed = []

for i in range(4):
    new_corner_i = transform_point(x_points[i], y_points[i])
    print(f'New corner {i}, {new_corner_i.astype(int)}')
    # new_corner_i = new_corner_i.astype(int)
    new_corner_i = new_corner_i.tolist()
    x_points_transformed.append(new_corner_i[0])
    y_points_transformed.append(new_corner_i[1])

# x_points_transformed.append(x_points_transformed[0])
# y_points_transformed.append(y_points_transformed[0])
print(f'X points transformed: {x_points_transformed} ')
print(f'Y points transformed: {y_points_transformed} ')
print(f'Angle: {angle}')
print('----------------------')

# ======================= Poligon ============================

box_not_rotated = Polygon([(x_points_transformed[0], y_points_transformed[0]),
                           (x_points_transformed[1], y_points_transformed[1]),
                           (x_points_transformed[2], y_points_transformed[2]),
                           (x_points_transformed[3], y_points_transformed[3])])

box_not_rotated_coordinates = list(box_not_rotated.exterior.coords)[:4]

print(f'Poligon coordinates {box_not_rotated_coordinates}')

angle_deg = math.degrees(angle)

rotated_box = rotate(box_not_rotated, angle_deg, origin='center')

rotated_box_coordinates = list(rotated_box.exterior.coords)[:4]

print(f'Rotated box coord: {rotated_box_coordinates}')

x_points_rotated = [x[0] for x in rotated_box_coordinates]
y_points_rotated = [y[1] for y in rotated_box_coordinates]
x_points_rotated.append(x_points_rotated[0])
y_points_rotated.append(y_points_rotated[0])

# ----------------------- End Polygon ----------------------------

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
plt.plot(x_points_transformed,  y_points_transformed, color='r')
plt.plot(center_new[0], center_new[1], 'o', color='r')
#first point
plt.plot(x_points_transformed[0], y_points_transformed[0], 'o', color='blue')
plt.plot(x_points_transformed[1], y_points_transformed[1], 'o', color='magenta')

# rotated box
plt.plot(x_points_rotated, y_points_rotated, color = 'g')




# Set labels and title
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
# plt.title('Point in Cartesian Coordinate System')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()