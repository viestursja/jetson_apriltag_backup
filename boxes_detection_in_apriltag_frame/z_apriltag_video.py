# just to test aprilTags in live video
# define cam
# define tag type


import apriltag
import cv2 as cv
import time
import subprocess

# Open video capture from the camera
cap = cv.VideoCapture('/dev/video0')

if not cap.isOpened():
    print("Error: Could not open video source.")
    quit()

# Set the video frame width and height (optional)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

# cap.set(cv.CAP_PROP_FRAME_WIDTH, 1240)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 675)

# Initialize the AprilTag detector with the desired tag family
# options = apriltag.DetectorOptions(families="tag16h5")
options = apriltag.DetectorOptions(families="tag16h5")
detector = apriltag.Detector(options)

time_start = time.time()

while True:
    # Capture a frame from the camera
    result_focus = subprocess.run(["v4l2-ctl --get-ctrl=focus_absolute"], shell=True, capture_output=True, text=True)
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from video source.")
        continue  # Skip to the next iteration if frame capture failed

    # Convert the frame to grayscale
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # small_img_gray = cv.resize(img_gray, (640, 480))
    # img_gray = cv.GaussianBlur(img_gray, (5, 5), 0)

    # Detect AprilTags in the grayscale image
    results = detector.detect(img_gray)

    if len(results) == 0:
        print('No tags detected')

    # Draw detected tags on the original frame
    for result in results:
        x, y = result.center
        x, y = int(x), int(y)
        # print(f'Result tag id:{result.tag_id})

        print(f'Point: {result.tag_id} {x} {y}')
        cv.circle(frame, (x, y), 5, (0, 0, 255), -1)

    # Resize the frame for display (optional)
    # resized = cv.resize(frame, (1280, 960))
    cv.imshow('AprilTag Detection', frame)
    time_end = time.time()
    frame_rate = 1 /(time_end - time_start)
    print(int(frame_rate))
    time_start = time.time()
    print(f'Focus value: {result_focus.stdout}')
    

    # Exit if 'q' is pressed
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        print('q is pressed')
        break

# Release the video capture and close windows
cap.release()
cv.destroyAllWindows()
