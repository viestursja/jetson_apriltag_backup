from ultralytics import YOLO
import cv2 as cv
# import torch
import numpy as np
import matplotlib.pyplot as plt
import json

print('Starting inference work......')
print('-----------------------------')

model_path = 'best.pt'
image_path = 'captured_image_z3.jpg'


model = YOLO(model_path)
results = model(image_path, imgsz=640, iou=0.4, conf=.9, verbose=True)

bbox = results[0].obb.xywhr

print(f'bbox: {bbox}')
print('----------------------------')
box_coordinates = bbox.cpu().numpy()

# box_coordinates = box_coordinates.astype(int)

print(f'Results box coordinates: {box_coordinates}')

# write box coordibate in json
box_coordinates_list = box_coordinates.tolist()
json_data = {f"box_{i}": box_coordinates_list[i] for i in range(len(box_coordinates_list))}
json_string = json.dumps(json_data, indent=4)
with open("box_coordinates.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

img = cv.imread(image_path)
height, width, _ = img.shape
height



# draw the boxes
def draw_rotated_bbox(image, bbox, label):
    bbox = bbox.cpu().numpy()
    cx, cy, w, h, angle = bbox
    rect = ((int(cx),int(cy)), (int(w), int(h)), (angle * 180 / np.pi) )
    # print(rect)
    box = cv.boxPoints(rect)
    box = box.astype(int)
    cv.drawContours(img, [box], 0, (0, 255, 0), 1)
    text_position = (int(cx - w / 2), int(cy - h / 2 - 5))  # Adjust text above bbox
    cv.putText(img, label, text_position, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)

for label, bbox in enumerate(results[0].obb.xywhr):    
    draw_rotated_bbox(img, bbox, str(label))


cv.imwrite('image_with_detected_boxes.jpg', img)
print('Image saved as image_with_detected_boxes.jpg')

# show image
# while True:
#     # resized = cv.resize(img, (640, 480))
#     cv.imshow('test', img)    
#     key = cv.waitKey(1) & 0xFF

#     if key == ord('q'):

#         print('q is pressed')   
#         cv.destroyAllWindows()
#         quit()

    

