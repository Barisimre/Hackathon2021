import cv2 as cv
from get_greenscreen import get_green_screen
from heightmap_to_mesh import get_stl
import matplotlib.pyplot as plt
from stlToGLTF import stl_to_gltf
import math
import os
import numpy as np
from tqdm import tqdm


def transpose(matrix):
    return np.array([[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))])

def get_heightmap():

    print('Get height map')
    
    os.chdir("img/img_dump")
    image_names = os.listdir()

    images = [cv.imread(img_name, 0) for img_name in tqdm(image_names)]
    master_image = np.median(images, 0) + (np.std(images, 0) * 9)


    # kernel = np.ones((3, 3), np.float32) / 9
    # master_image = cv.filter2D(master_image, -1, kernel)
    master_image = cv.blur(master_image, (5, 5))
    master_image = np.cbrt(master_image) * 150
    master_image = -master_image
    plt.imshow(master_image, cmap='gray')
    plt.show()
    print('Done getting height map')


    return master_image, cv.imread(image_names[0])


def image_to_gltf(filepath):

    heightmap, image = get_heightmap()
    os.chdir('../../')

    background_pixels = get_green_screen(image)

    print('Make stl')

    stl_path = get_stl(heightmap, background_pixels)

    gltf_path = "gltf/keyboard.gltf"

    print('Make gltf')

    stl_to_gltf(stl_path, gltf_path, True)

    return heightmap


image_to_gltf('img/origin.png')