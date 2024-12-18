import cv2

img = cv2.VideoCapture(0)

# defines output size of img, FPS depends on it
img.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
img.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)



counter = 0

# if 0 waits any key press
while True:
    ok, image = img.read()

    cv2.imshow('test', image)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        image_path = 'captured_image_' + str(counter) + '.jpg'
        cv2.imwrite(image_path, image)
        print(f'size of img::{image.shape}' )
        counter = counter + 1
        print('c is pressed')
    elif key == ord('q'):
        print('q is pressed')
        break