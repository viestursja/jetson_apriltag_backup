# set framereate by subprocess and commandline

import subprocess

# Set video device
video_device = "/dev/video0"

# Construct the command as a list
command = [
    "gst-launch-1.0",
    "v4l2src",
    f"device={video_device}",
    "!",
    "video/x-raw,framerate=30/1",
    "!",
    "autovideosink",
]

# Run the command
subprocess.run(command)
