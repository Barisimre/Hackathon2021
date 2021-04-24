from typing import List
import cv2 as cv
import os
from matplotlib import pyplot as plt
from height_map import build_heightmap
import numpy as np
import pickle


def transpose(matrix):
    return np.array([[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))])


os.chdir("   ")
image_names = os.listdir()


images = [cv.imread(img_name, 0) for img_name in image_names]

images = [transpose(img) for img in images]
images = np.array(images)

master_image = np.std(images, 0) * 5


for i in range(len(images)):

    master_image += images[i] / len(images)


kernel = np.ones((5, 5), np.float32) / 25
master_image = cv.filter2D(master_image, -1, kernel)

cv.imwrite("../HEIGHTMAP.png", master_image / 6.0)


plt.subplot(121)
plt.imshow(master_image, cmap='gray')
plt.show()