import cv2

img = cv2.VideoCapture(0)
img.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
img.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print(f'size of img::{img.__sizeof__}' )

counter = 0

# if 0 waits any key press
while True:
    ok, image = img.read()

    cv2.imshow('test', image)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        image_path = 'captured_image_' + str(counter) + '.jpg'
        cv2.imwrite(image_path, image)
        counter = counter + 1
        print('c is pressed')
    elif key == ord('q'):
        print('q is pressed')
        break