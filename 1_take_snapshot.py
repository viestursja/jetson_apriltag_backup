import cv2
import subprocess

# disable autofokus
subprocess.run(["v4l2-ctl --set-ctrl=focus_automatic_continuous=0"], shell=True, capture_output=True, text=True)

# capture image
img = cv2.VideoCapture('/dev/video0')
img.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
img.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

focus_value = 100
focus_string = 'v4l2-ctl --set-ctrl=focus_absolute=' + str(focus_value)

while True:

    # set focus value
    subprocess.run([focus_string], shell=True, capture_output=True, text=True)
    # result_focus_auto = subprocess.run(["v4l2-ctl --get-ctrl=focus_automatic_continuous"], shell=True, capture_output=True, text=True)
    # result_focus_value = subprocess.run(["v4l2-ctl --get-ctrl=focus_absolute"], shell=True, capture_output=True, text=True)
    # print(f'2_Focus auto: {result_focus_auto.stdout}Focus is set to: {result_focus_value.stdout}')

    ok, image = img.read()

    # cv2.imshow('test', image)
    image_path = 'captured_image_z3' + '.jpg'    
    
    counter = counter + 1
    if counter == 20:        
        result_focus = subprocess.run(["v4l2-ctl --get-ctrl=focus_absolute"], shell=True, capture_output=True, text=True)
        cv2.imwrite(image_path, image)
        print(f'Photo saved in {image_path}; Final focus value : {result_focus.stdout}')
        break
    






 