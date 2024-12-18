# detects corner tag coordinates, library used in 'object_identification_on_base_plane.py'

import apriltag
import cv2 as cv
import json

def identify_corner_coordinates():
    print('Identifing the corner coordinates .....')
    print('---------------------------------------')

    # read image
    img = cv.imread('captured_image_z3.jpg')
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # detect tags
    options = apriltag.DetectorOptions(families="tag16h5")
    detector = apriltag.Detector(options)
    results = detector.detect(img_gray)

    # print(results)

    if len(results) == 0:
        print('No tags detected')
        quit()
    # print(f'Results: {results}')
    # print(f'Center coordinates: {results[0].center}')

    if len != 4:
        print(f'Incorrect number of tags: {len(results)}')
        # should exit here

    coordinates = {}
    # five tags case - sample
    coordinates_keys = ['ll', 'lr', 'ul', 'ur', 'sample']

    i = 0
    for corner in results:    
        x, y = corner.center
        x, y = int(x), int(y)
        coordinates.update({f'{coordinates_keys[i]}' : [x, y]})
        i = i + 1
        # print(f'Point: {x} {y}')
        cv.circle(img, (x, y), 5, (0, 0, 255), -1)
    print(f'Coordinates of tags: {coordinates}')
    
    # save coordinates in json
    with open("corners_coordinates.json", "w") as json_file:
        json.dump(coordinates, json_file, indent=4)

    print('Corner coordinates idetified and saved')
    print('---------------------------------------')

    # show image
    # while True:
    #     resized = cv.resize(img, (640, 480))
    #     cv.imshow('test', resized)    
    #     key = cv.waitKey(1) & 0xFF

    #     if key == ord('q'):
    #         print('q is pressed')   
    #         cv.destroyAllWindows()
    #         quit()
    

# identify_corner_coordinates()
if __name__ == "__main__":
    identify_corner_coordinates()