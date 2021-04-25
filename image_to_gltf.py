import cv2 as cv
from get_greenscreen import get_green_screen
from heightmap_to_mesh import get_stl
import matplotlib.pyplot as plt
from stlToGLTF import stl_to_gltf
import math
import os
import numpy as np
from tqdm import tqdm
import random
from myGLTFCreator import create_gltf_file
import cv2 as cv


def get_heightmap():

    print('Get height map')
    
    os.chdir("img/img_dump")
    image_names = os.listdir()

    images = np.array([cv.imread(img_name, 0) for img_name in tqdm(image_names)])
    images = [img[350:800, 440:1500] for img in images]
    master_image = np.median(images, 0) + (np.std(images, 0) * 9)


    # kernel = np.ones((3, 3), np.float32) / 9
    # master_image = cv.filter2D(master_image, -1, kernel)

    master_image = cv.blur(master_image, (5, 5)) * 1.5
    master_image = np.cbrt(master_image * 250000) * 4
    # master_image = n
    master_image = -master_image
    plt.imshow(master_image, cmap='gray')
    plt.show()
    print('Done getting height map')

    green_screen_names = random.sample(image_names[:(len(image_names) // 4)], 20)
    images = np.array([cv.imread(img_name) for img_name in tqdm(green_screen_names)])
    images = [img[350:800, 440:1500] for img in images]
    screens = np.array([get_green_screen(img) for img in tqdm(images)])
    mask = screens[0]

    os.chdir('../../')
    cv.imwrite("texture_source.png", images[0])

    for i in tqdm(range(1, len(screens))):
        mask += screens[i]

    return master_image, mask, "texture_source.png"


def image_to_gltf(filepath):

    heightmap, background_pixels, texture_file_location = get_heightmap()


    print('Make stl')

    faces = get_stl(heightmap, background_pixels)

    img = cv.imread(texture_file_location)
    dims = (len(img[0]), len(img))
    print("Dims: ", dims[0], dims[1])

    gltf_path = "gltf/keyboard.gltf"

    print('Make gltf')

    create_gltf_file(faces, "test.bin","test.gltf", texture_file_location, dims)
    #stl_to_gltf(stl_path, gltf_path, True)

    return heightmap


image_to_gltf('img/origin.png')