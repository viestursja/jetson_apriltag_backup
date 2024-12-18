import cv2 as cv
import time

# Use OpenCV to capture frames from GStreamer pipeline
# pipeline = ('v4l2src device="/dev/video0" ! video/x-raw ! appsink')

#runs with 9 fps
pipeline = ('autovideosrc ! videoconvert ! appsink')

#runs at 9 fps
# pipeline = ('autovideosrc ! video/x-raw, framerate=5/1 ! videoconvert ! appsink')

#runs at 1 fps
# pipeline = ('v4l2src device="/dev/video0" ! video/x-raw, framerate=30/1 ! videoconvert ! video/x-raw ! appsink')

pipeline = '/dev/video0'

img = cv.VideoCapture(pipeline)


# this shows 1 fps
# img = cv.VideoCapture("v4l2src device=/dev/video0 ! image/jpeg, format=MJPG ! jpegdec !  appsink", cv.CAP_GSTREAMER)


# img = cv.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=BGR ! appsink drop=1", cv.CAP_GSTREAMER)
# img = cv.VideoCapture('/dev/video0')

# img.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('m','j','p','g'))
# img.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M','J','P','G'))

if not img.isOpened():
    print("Error: Could not open video source.")
    quit()

time_start = time.time()

while True:
    ok, image = img.read()
    if not ok:
        print("Error: Could not read frame.")
        break
    
    cv.imshow('test', image)    

    time_end = time.time()
    frame_rate = 1 / (time_end - time_start)
    print(f"Frame Rate: {int(frame_rate)} fps")
    time_start = time.time()     
    
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        print('q is pressed')   
        cv.destroyAllWindows()
        img.release()
        quit()
