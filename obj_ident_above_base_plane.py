import cv2
import numpy as np
import matplotlib.pyplot as plt
from get_corners_coordinates import get_corner_coordinates
from get_test_object_coordinates import get_test_oject_coordinates

# Base plane dimensions
# size of field in centimeters
W = 49
H = 74

# Camera intrinsic parameters (assumed or obtained from calibration)
focal_length = 900 # Example focal length in pixels
center = (320, 240)  # Principal point (usually at the image center)

# Coordinates of the corners of the base plane in the camera image
corners_dict = get_corner_coordinates()

src_points = np.array([
    corners_dict['ll'],  # Lower-left corner
    corners_dict['lr'],  # Lower-right corner
    corners_dict['ur'],  # Upper-right corner
    corners_dict['ul']   # Upper-left corner
], dtype=np.float32)

# Physical coordinates in the desired Cartesian system for the base plane
object_points = np.array([
    [0, 0, 0],     # Lower-left corner in 3D (world coordinates)
    [W, 0, 0],     # Lower-right corner in 3D
    [W, H, 0],     # Upper-right corner in 3D
    [0, H, 0]      # Upper-left corner in 3D
], dtype=np.float32)

camera_matrix = np.array([
    [focal_length, 0, center[0]],
    [0, focal_length, center[1]],
    [0, 0, 1]
], dtype=np.float32)

dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion for simplicity

# points in Cortesian xy system
dst_points = np.array([
    [0, 0],     # Lower-left corner
    [W, 0],     # Lower-right corner
    [W, H],     # Upper-right corner
    [0, H]      # Upper-left corner
], dtype=np.float32)

# perspective trabsformation
matrix = cv2.getPerspectiveTransform(src_points, dst_points)

def transform_point(px, py):
    point = np.array([[px, py]], dtype=np.float32)
    point = np.array([point])
    transformed_point = cv2.perspectiveTransform(point, matrix)
    return transformed_point[0][0]


# Estimate pose of the base plane (rotation and translation)
success, rvec, tvec = cv2.solvePnP(object_points, src_points, camera_matrix, dist_coeffs)

if success:
    print(f"Rotation Vector:\n{rvec}")
    print(f"Translation Vector:\n{tvec}")

    # Project a test tag point in the image to the base plane
    px, py = get_test_oject_coordinates() 
    image_point = np.array([[px, py]], dtype=np.float32)
    image_point_h = np.array([[px, py, 1]], dtype=np.float32).T  # Homogeneous coordinates
    new_x, new_y = transform_point(px, py)

    # Compute the inverse of the camera projection matrix
    rot_matrix, _ = cv2.Rodrigues(rvec)
    proj_matrix = np.hstack((rot_matrix, tvec))
    inv_proj_matrix = np.linalg.pinv(camera_matrix @ proj_matrix)

    # Calculate the 3D coordinates of the point projected on the base plane (z = 0)
    world_point_h = inv_proj_matrix @ image_point_h
    world_point = world_point_h[:3] / world_point_h[3]
    projected_x, projected_y = float(world_point[0]), float(world_point[1])

    print(f"Projected coordinates on the base plane: ({projected_x:.2f}, {projected_y:.2f})")

    # Draw the projected point on the Cartesian coordinate system
    plt.figure(figsize=(8, 8))

    # Draw the Cartesian axes
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)

    # Draw the base plane (Cartesian system boundaries)
    cartesian_plane = np.array([[0, 0], [W, 0], [W, H], [0, H], [0, 0]])
    plt.plot(cartesian_plane[:, 0], cartesian_plane[:, 1], 'b-', label='Base Plane')

    # Draw the projected point from camera
    plt.plot(projected_x, projected_y, 'ro', label=f'Projected Point ({projected_x:.2f}, {projected_y:.2f})')
    plt.plot(new_x, new_y, 'gx', label=f'Original Point ({new_x:.2f}, {new_y:.2f})')

    # Set labels and title
    plt.xlabel('X Axis (cm)')
    plt.ylabel('Y Axis (cm)')
    plt.title('Projection of Test Tag on Base Plane')
    plt.legend()

    plt.grid(True)
    plt.axis('equal')
    plt.show()
else:
    print("Could not solve PnP for the given points.")