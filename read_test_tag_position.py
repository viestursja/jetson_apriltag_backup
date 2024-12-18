# this detects pixel coordinates of the corners

import apriltag
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# count number of frames for corner detaction lists
frame_count = 5

# id tags of corners (1 - 4) 5 is test object id
tag_id_list = [1, 2, 3, 4, 5]

# tag family 
tag_family = "tag16h5"

# size of field in centimeters
W = 49
H = 74

tag_1_list = []
tag_2_list = []
tag_3_list = []
tag_4_list = []
object = []

# Open video capture from the camera
cap = cv.VideoCapture('/dev/video0')

if not cap.isOpened():
    print("Error: Could not open video source.")
    quit()

# Set the video frame width and height (optional)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize the AprilTag detector with the desired tag family
options = apriltag.DetectorOptions(families=tag_family)
detector = apriltag.Detector(options)

# function to determine most common tuple in lists
def most_common(lst):
    return max(set(lst), key=lst.count)

# run frames to detect corners
for n in range(frame_count):
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from video source.")
        continue  
 
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)   
    results = detector.detect(img_gray)
    # print(results)

    if len(results) == 0:
        print('No tags detected')    

# read 4 corners (and test object)
    for result in results:
        if result.tag_id in tag_id_list:
            tag_id = int(result.tag_id)
            x, y = result.center
            (x, y) = int(x), int(y)
            tup = (x, y)
            if tag_id == tag_id_list[0]:
                tag_1_list.append(tup)
            elif tag_id == tag_id_list[1]:
                tag_2_list.append(tup)
            elif tag_id == tag_id_list[2]:
                tag_3_list.append(tup)
            elif tag_id == tag_id_list[3]:
                tag_4_list.append(tup)
            elif tag_id == tag_id_list[4]:
                object.append(tup)
            
if len(tag_1_list) < 3:
    print('Corner 1 is not readable')
    exit()
if len(tag_2_list) < 3:
    print('Corner 2 is not readable')
    exit()
if len(tag_3_list) < 3:
    print('Corner 3 is not readable')
    exit()
if len(tag_4_list) < 3:
    print('Corner 4 is not readable')
    exit()
if len(object) < 2:
    print('Object is not readable')

corner_1 = most_common(tag_1_list)
corner_2 = most_common(tag_2_list)
corner_3 = most_common(tag_3_list)
corner_4 = most_common(tag_4_list)

# defining the corner coordinates
dict_corners = {  

    "ll" : list(corner_1),
    "lr" : list(corner_2),
    "ur" : list(corner_4),
    "ul" : list(corner_3)
    
    }

object_coord = most_common(object)

print(f'Corner 1: {corner_1}, {len(tag_1_list)}')
print(f'Corner 2: {corner_2}, {len(tag_2_list)}')
print(f'Corner 3: {corner_3}, {len(tag_3_list)}')
print(f'Corner 4: {corner_4}, {len(tag_4_list)}')

print(f'Object: {list(object_coord)}')
print(dict_corners)

cap.release()
# cv.destroyAllWindows()

# corners_dict = {'ll': [51, 447], 'lr': [605, 443], 'ur': [453, 64], 'ul': [167, 63]}
corners_dict = dict_corners

src_points = np.array([
    corners_dict['ll'], 
    corners_dict['lr'], 
    corners_dict['ur'], 
    corners_dict['ul'] 

], dtype=np.float32
)

dst_points = np.array([
    [0, 0],     # Lower-left corner
    [W, 0],     # Lower-right corner
    [W, H],     # Upper-right corner
    [0, H]      # Upper-left corner
], dtype=np.float32)

matrix = cv.getPerspectiveTransform(src_points, dst_points)

def transform_point(px, py):
    point = np.array([[px, py]], dtype=np.float32)
    point = np.array([point])
    transformed_point = cv.perspectiveTransform(point, matrix)
    return transformed_point[0][0]

# px, py = 290, 256 # Replace with the pixel coordinates to transform

px = list(object_coord)[0]
py = list(object_coord)[1]

# calculate the coordinates in xy plot
new_x, new_y = transform_point(px, py)
print(f"Transformed coordinates: ({int(new_x)}, {int(new_y)})")

# ploting the test object in xy plane plot
plt.figure(figsize=(6, 10))
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
