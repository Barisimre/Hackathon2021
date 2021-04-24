from record import get_video
from image_to_mesh import gen_models
import os
import glob


# How long should the capture take in seconds (0 if no capture)
SECONDS = 3
CAM_IP = "130.89.137.189"
# Run Floris lib
FLORIS = False

# Capture
get_video(SECONDS, CAM_IP)

# Run floris

if FLORIS:
	gen_models()

