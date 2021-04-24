from record import get_video
from imageToFlatMesh import gen_models
import os
import glob


# How long should the capture take in seconds (0 if no capture)
SECONDS = 10
# Run Floris lib
FLORIS = True

# Capture
get_video(SECONDS)

# Run floris

if FLORIS:
	gen_models()

