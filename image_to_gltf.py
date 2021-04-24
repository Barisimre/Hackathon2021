import cv2 as cv
from get_greenscreen import get_green_screen
from heightmap_to_mesh import get_stl
import matplotlib.pyplot as plt
from stlToGLTF import stl_to_gltf
import math
import os
import numpy as np
from tqdm import tqdm



def get_heightmap():

    print('Get height map')
    
    os.chdir("img/img_dump")
    image_names = os.listdir()


    images = [cv.imread(img_name, 0) for img_name in image_names]

    images = np.array(images)

    master_image = np.std(images, 0) * 5


    for i in tqdm(range(len(images))):

        master_image += images[i] / len(images)


    kernel = np.ones((5, 5), np.float32) / 25
    master_image = cv.filter2D(master_image, -1, kernel)

    print('Done getting height map')


    return master_image, cv.imread(image_names[0])


def image_to_gltf(filepath):

    heightmap, image = get_heightmap()
    os.chdir('../../')

    heightmap = [[(px * 10000) ** (1/2) for px in col] for col in heightmap]
    background_pixels = get_green_screen(image)

    print('Make stl')

    stl_path = get_stl(heightmap, background_pixels)

    gltf_path = "gltf/keyboard.gltf"

    print('Make gltf')

    stl_to_gltf(stl_path, gltf_path, True)

    return heightmap


image_to_gltf('img/origin.png')