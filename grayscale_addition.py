from typing import List
import cv2 as cv
import os
from matplotlib import pyplot as plt
from height_map import build_heightmap
import numpy as np
import pickle


LeftImage = cv.imread('light_data/Left.jpg', 0)
RightImage = cv.imread('light_data/Right.jpg', 0)

images = [LeftImage, RightImage]
images = [img[1888:2283, 1223:2215] for img in images]

result = images[0] / 2.0 + images[1] / 2.0

plt.imshow(result, cmap='gray')
plt.show()