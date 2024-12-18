import cv2 as cv
cap = cv.VideoCapture("dev/video0")

# Set the video frame width and height (optional)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 990)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 540)

while True:
    ret,frame = cap.read()
    print(f'Ret: {ret}')
    cv.imshow('dddd',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()
cap.release()