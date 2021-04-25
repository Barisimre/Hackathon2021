from record import get_video
from settings import *
from image_to_gltf import image_to_gltf


# Capture
get_video(RECORDING_TIME, CAM_IP)
image_to_gltf()

