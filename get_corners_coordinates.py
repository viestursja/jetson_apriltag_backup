# used as library for object_identificateion_on_base_plane.py

import apriltag
import cv2 as cv
# import numpy as np

# count number of frames for corner detaction lists
frame_count = 30

# id tags of corners (1 - 4) 5 is test object id
tag_id_list = [1, 2, 3, 4]

# tag family 
tag_family = "tag16h5"

# size of field in centimeters
W = 49
H = 74

tag_1_list = []
tag_2_list = []
tag_3_list = []
tag_4_list = []

def get_corner_coordinates():
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
    print(dict_corners)
    return dict_corners

# get_corner_coordinates()