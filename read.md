## Camera Properties

[Manual USB camera settings in Linux](https://www.kurokesu.com/main/2016/01/16/manual-usb-camera-settings-in-linux/)

> Šajā lapā ir neprecīzi parametrii - nolasīt jaunus ar komandrindu zemāk

## Camera Controls

`v4l2-ctl --list-devices`
`v4l2-ctl -d /dev/video0 --list-ctrls`

`v4l2-ctl --list-formats` : YUYV, MJPG
`v4l2-ctl --list-formats-ext' : 
`v4l2-ctl -d /dev/video0 --get-fmt-video` : frame size



## Subprocess

```python
import subprocess
result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)
print(result.stdout)
```

## Logitech C920 Controls 

```bash


User Controls

                     brightness 0x00980900 (int)    : min=-64 max=64 step=1 default=0 value=0
                       contrast 0x00980901 (int)    : min=0 max=64 step=1 default=32 value=32
                     saturation 0x00980902 (int)    : min=0 max=128 step=1 default=56 value=56
                            hue 0x00980903 (int)    : min=-40 max=40 step=1 default=0 value=0
        white_balance_automatic 0x0098090c (bool)   : default=1 value=1
                          gamma 0x00980910 (int)    : min=72 max=500 step=1 default=100 value=100
                           gain 0x00980913 (int)    : min=0 max=100 step=1 default=0 value=0
           power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=1 value=1 (50 Hz)
      white_balance_temperature 0x0098091a (int)    : min=2800 max=6500 step=1 default=4600 value=4600 flags=inactive
                      sharpness 0x0098091b (int)    : min=0 max=6 step=1 default=3 value=4
         backlight_compensation 0x0098091c (int)    : min=0 max=2 step=1 default=1 value=1

Camera Controls

                  auto_exposure 0x009a0901 (menu)   : min=0 max=3 default=3 value=3 (Aperture Priority Mode)
         exposure_time_absolute 0x009a0902 (int)    : min=1 max=5000 step=1 default=156 value=156 flags=inactive
     exposure_dynamic_framerate 0x009a0903 (bool)   : default=0 value=1
                   pan_absolute 0x009a0908 (int)    : min=-36000 max=36000 step=0 default=0 value=0
                  tilt_absolute 0x009a0909 (int)    : min=-36000 max=36000 step=0 default=0 value=0
                 focus_absolute 0x009a090a (int)    : min=1 max=1023 step=1 default=140 value=160 flags=inactive
     focus_automatic_continuous 0x009a090c (bool)   : default=1 value=1
                  zoom_absolute 0x009a090d (int)    : min=0 max=9 step=0 default=0 value=0


```

## [cv2.GetPerspectiveTransform()](https://theailearner.com/tag/cv2-getperspectivetransform/)


# Process

## 1. Take snapshot

> Uzņem kadru: `1_take_snapshot.py`

> Output: `captured_image_z3.jpg` 

## 2. Apriltag - Identify tags

> Atgriež April tag stūru pix koordinātes. `apriltag_identify_tags.py`

> Output: `corners_coordinates.json`

## 3. Inference work

> Identificē kastītītes. `3_inference_work.py`

> Output: `box_coordinates.jpg`

## 4. Object identification on base plane

> Pārnes kastīšu koordinātes CNC plaknē. `object_identification_on_base_plane.py`

> 

