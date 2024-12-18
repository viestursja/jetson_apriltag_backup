import apriltag
import cv2 as cv

img = cv.imread('captured_image_1.jpg')
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
options = apriltag.DetectorOptions(families="tag16h5")
detector = apriltag.Detector(options)
results = detector.detect(img_gray)

print(results)

if len(results) == 0:
    print('No tags detected')
    quit()
print(f'Results: {results}')
print(f'Center coordinates: {results[0].center}')



for corner in results:
    x, y = corner.center
    x, y = int(x), int(y)

    print(f'Point: {x} {y}')
    cv.circle(img, (x, y), 5, (0, 0, 255), -1)
    

while True:
    resized = cv.resize(img, (640, 480))
    cv.imshow('test', resized)    
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        print('q is pressed')   
        cv.destroyAllWindows()
        quit()
   

