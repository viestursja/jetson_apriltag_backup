# used as library for object_identificateion_on_base_plane.py

import apriltag
import cv2 as cv
import matplotlib.pyplot as plt
# import numpy as np

# count number of frames for corner detaction lists
frame_count = 5

# id tags of corners (1 - 4) 5 is test object id
tag_id_list = [5]

# tag family 
tag_family = "tag16h5"

object = []

def get_test_oject_coordinates():
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
                    object.append(tup)            

    if len(object) < 2:
        print('Object is not readable')

    object_coord = most_common(object)
    print(object_coord)
    return object_coord[0], object_coord[1]

# read_test_oject_coordinates()