import cv2
import numpy as np
import matplotlib.pyplot as plt
from get_corners_coordinates import get_corner_coordinates
from get_test_object_coordinates import get_test_oject_coordinates

# size of field in centimeters
W = 49
H = 74

corners_dict = get_corner_coordinates()
print( f'Corners dict: {corners_dict}')

src_points = np.array([
    corners_dict.get('ll'),  # Lower-left corner
    corners_dict.get('lr'),  # Lower-right corner
    corners_dict.get('ur'),  # Upper-right corner
    corners_dict.get('ul')   # Upper-left corner
], dtype=np.float32)

print(f'corners array: {src_points}')

# Physical coordinates in the desired Cartesian system
# Assuming 'L' is the physical length of the side

dst_points = np.array([
    [0, 0],     # Lower-left corner
    [W, 0],     # Lower-right corner
    [W, H],     # Upper-right corner
    [0, H]      # Upper-left corner
], dtype=np.float32)

# Compute the perspective transformation matrix
matrix = cv2.getPerspectiveTransform(src_points, dst_points)

# Function to transform any point
def transform_point(px, py):
    point = np.array([[px, py]], dtype=np.float32)
    point = np.array([point])
    transformed_point = cv2.perspectiveTransform(point, matrix)
    return transformed_point[0][0]

# Example usage: Transform a pixel (px, py)
# px, py = 300, 300  # Replace with the pixel coordinates to transform
px, py = get_test_oject_coordinates()
print(f'test obj coordinates {px} {py}')

new_x, new_y = transform_point(px, py)
print(f"Transformed coordinates: ({new_x}, {new_y})")

# Camera intrinsic parameters (assumed or obtained from calibration)
focal_length = 80  # Example focal length in pixels
center = (240, 320)  # Principal point (usually at the image center)

camera_matrix = np.array([
    [focal_length, 0, center[0]],
    [0, focal_length, center[1]],
    [0, 0, 1]
], dtype=np.float32)

dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion for simplicity

# Solve for the rotation and translation vectors using solvePnP
object_points = np.array([
    [0, 0, 0],     # Lower-left corner in 3D (world coordinates)
    [W, 0, 0],     # Lower-right corner in 3D
    [W, H, 0],     # Upper-right corner in 3D
    [0, H, 0]      # Upper-left corner in 3D
], dtype=np.float32)

# Image points detected in the image (pixel coordinates)
image_points = np.array([src_points], dtype=np.float32)

# Estimate pose of the AprilTag (rotation and translation)
success, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)

if success:
    print(f"Rotation Vector:\n{rvec}")
    print(f"Translation Vector:\n{tvec}")

    # Project a 3D point (e.g., the center of the AprilTag) to the image plane
    point_3d = np.array([[W / 2, H / 2, 0]], dtype=np.float32)  # Center of the AprilTag
    point_2d, _ = cv2.projectPoints(point_3d, rvec, tvec, camera_matrix, dist_coeffs)
    projected_x, projected_y = point_2d.ravel()
    print(f"Projected coordinates in the image: ({projected_x:.2f}, {projected_y:.2f})")

    # Draw the projected point on the Cartesian coordinate system
    plt.figure(figsize=(8, 8))

    # Draw the Cartesian axes
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)

    # Draw the transformed square (Cartesian system boundaries)
    cartesian_square = np.array([[0, 0], [W, 0], [W, H], [0, H], [0, 0]])
    plt.plot(cartesian_square[:, 0], cartesian_square[:, 1], 'b-', label='Transformed Square')

    # Draw the transformed point
    plt.plot(new_x, new_y, 'ro', label=f'Transformed Point ({new_x:.2f}, {new_y:.2f})')

    # Draw the projected point from camera
    plt.plot(W / 2, H / 2, 'go', label=f'Projected Point ({W / 2:.2f}, {H / 2:.2f})')

    # Set labels and title
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.title('Point in Cartesian Coordinate System')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()
else:
    print("Could not solve PnP for the given points.")
