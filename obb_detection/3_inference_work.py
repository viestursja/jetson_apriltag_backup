from ultralytics import YOLO
import cv2 as cv
import torch
import numpy as np
import matplotlib.pyplot as plt

model_path = 'best.pt'
image_path = 'captured_image_0.jpg'


model = YOLO(model_path)
results = model(image_path, imgsz=640, iou=0.4, conf=.9, verbose=True)

bbox = results[0].obb.xywhr
box_coordinates = bbox.cpu().numpy()

print(f'Results box coordinates: {box_coordinates}')

img = cv.imread(image_path)
height, width, _ = img.shape
height

def draw_rotated_bbox(image, bbox):
    bbox = bbox.cpu().numpy()
    cx, cy, w, h, angle = bbox
    rect = ((int(cx),int(cy)), (int(w), int(h)), (angle * 180 / np.pi) )
    # print(rect)

    box = cv.boxPoints(rect)
    box = box.astype(int)
    cv.drawContours(img, [box], 0, (0, 255, 0), 1)

for bbox in results[0].obb.xywhr:
    draw_rotated_bbox(img, bbox)

cv.imshow('box', img)

    # Wait for key press
key = cv.waitKey(1) & 0xFF

if key == ord('q'):  # Press 'q' to quit
    print("Exiting...")
    

cv.destroyAllWindows()