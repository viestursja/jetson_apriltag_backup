import cv2 as cv
import time
import subprocess

# Use OpenCV to capture frames from GStreamer pipeline
pipeline = (
    "/dev/video0"
)
subprocess.run(["v4l2-ctl --set-ctrl=brightness=0"], shell=True, capture_output=True, text=True)
img = cv.VideoCapture(pipeline)

if not img.isOpened():
    print("Error: Could not open video source.")
    quit()

time_start = time.time()

while True:
    subprocess.run(["v4l2-ctl --set-ctrl=brightness=0"], shell=True, capture_output=True, text=True)
    ok, image = img.read()
    # resized = cv.resize(img, (640, 480))
    cv.imshow('test', image)    
    time_end = time.time()
    frame_rate = 1 / (time_end - time_start)
    print(int(frame_rate))
    # result_sharpness = subprocess.run(["v4l2-ctl --get-ctrl=sharpness"], shell=True, capture_output=True, text=True)
    # print(f'Sharpness: {result_sharpness.stdout}')
    # result_brightness = subprocess.run(["v4l2-ctl --get-ctrl=brightness"], shell=True, capture_output=True, text=True)
    # print(f'Brightness: {result_brightness.stdout}')


    time_start = time.time()     
    
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        print('q is pressed')   
        cv.destroyAllWindows()
        quit()






