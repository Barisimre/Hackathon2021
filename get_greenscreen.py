import cv2 as cv2
import numpy as np


def get_green_screen(image):

    COLOR = [255, 0, 0]

    image_copy = np.copy(image)
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
    kernel = np.ones((20,20),np.float32)/400
    image_copy = cv2.filter2D(image_copy,-1,kernel)

    lower_blue = np.array([0, 180, 0])
    upper_blue = np.array([180, 255, 180]) 

    mask = cv2.inRange(image_copy, lower_blue, upper_blue)

    mask2 = cv2.inRange(image, lower_blue, upper_blue)

    masked_image = np.copy(image)
    masked_image[mask != 0] = COLOR
    twice_masked = np.copy(masked_image)
    twice_masked[mask2 != 0] = COLOR


    is_background = np.zeros((len(twice_masked), len(twice_masked[0]), 1))


    for y in range(len(twice_masked)):
        for x in range(len(twice_masked[y])):
            if tuple(twice_masked[y][x]) == tuple(COLOR):
                is_background[y][x] = 1

    return is_background
