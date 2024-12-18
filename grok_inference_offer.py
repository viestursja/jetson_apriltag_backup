# this code was offered by grok
# identifies center, corners, id, draws it on picture


import cv2
import apriltag
import numpy as np

# Initialize video capture from USB camera (assuming it's the first camera, index 0)
cap = cv2.VideoCapture('/dev/video0')

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create an AprilTag detector
options = apriltag.DetectorOptions(families="tag16h5")
detector = apriltag.Detector(options)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert the frame to grayscale for AprilTag detection (since AprilTags are black and white)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags in the image
    tags = detector.detect(gray)
    print(f'Tags: {tags}')

    # Draw detection results on the frame
    for tag in tags:
        # Get the center of the tag
        center = tag.center
        cv2.circle(frame, (int(center[0]), int(center[1])), 5, (0, 255, 0), -1)

        # Draw the corners of the tag
        corners = tag.corners
        corners = corners.astype(int)
        cv2.polylines(frame, [corners], True, (255, 0, 0), 1)

        # Get the ID of the tag and display it
        tag_id = tag.tag_id
        cv2.putText(frame, f"ID: {tag_id}", (int(center[0]), int(center[1]) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


    # Display the resulting frame
    cv2.imshow('AprilTag Detection', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()