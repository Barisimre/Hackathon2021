from typing import List
import cv2 as cv
import os
from matplotlib import pyplot as plt
from height_map import build_heightmap
import numpy as np
import pickle

def pixel_angle(angles: List[float], images, x, y):
    best_angle = 0
    brightest = 0
    for i, a in enumerate(angles):
        img = images[i]
        if img[y][x] > brightest:
            best_angle = a
            brightest = img[y][x]
    return best_angle


def partial_normal_map(angles, images):
    normals = [[0 for x in range(len(images[0][0]))] for _ in range(len(images[0]))]
    print(f"Image dimensions: {len(images[0][0])} {len(images[0])}")

    for x in range(len(images[0][0])):
        print("column: ", x)
        for y in range(len(images[0])):
            normals[y][x] = pixel_angle(angles, images, x, y)

    return normals


def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


# def normal_map(x_angles, y_angles, images):
#     x_normals = partial_normal_map(x_angles, images)
#     y_normals = partial_normal_map(y_angles, list(map(transpose, images))
#
#     normals = [[(x_normals[y][x], y_normals[y][x]) for x in range(len(images[0][0]))] for y in range(len(images[0]))]
#     return normals


def detect_greenscreen_pixels(color_imgs):
    pxs = [[False for _ in range(len(color_imgs[0][0]))] for _ in range(len(color_imgs[0]))]

    for index, i in enumerate(color_imgs):
        if (index != 45) != 0:
            continue
        print("Collecting gs from image", index)
        for y in range(len(i)):
            for x in range(len(i[0])):
                b, g, r = i[y][x]
                if g > 70 and b < 70 and r > 70: # and r < 104 and b < 70:
                    pxs[y][x] = True
    return pxs


def apply_green_screen_to_normals(normals, green_screen):
    for x in range(len(normals[0])):
        for y in range(len(normals)):
            if green_screen[y][x]:
                normals[y][x] = 90
    return normals



if __name__ == "__main__":
    os.chdir("img/img_dump")
    image_names = os.listdir()

    color_images = [cv.imread(img_name, 3) for img_name in image_names]
    print("Color images loaded")
    print(color_images[45][700][700])
    try:
        with open("../green_screen", "rb") as f:
            green_screen_pixels = pickle.load(f)
    except:
        green_screen_pixels = transpose(detect_greenscreen_pixels(color_images))
        with open("../green_screen", "wb") as f:
            pickle.dump(green_screen_pixels, f)

    green_screen_pixels = transpose(detect_greenscreen_pixels(color_images))
    print("Green screen pixels loaded")

    green_screen_picture = [[255 if px else 0 for px in column] for column in green_screen_pixels]
    green_screen_picture[3][3] = 255
    plt.imshow(green_screen_picture, cmap='gray')
    plt.title('Original Image')
    plt.show()

    kernel = np.ones((5, 5), np.float32) / 25

    images = [cv.imread(img_name, 0) for img_name in image_names]
    # images = [transpose(cv.filter2D(img, -1, kernel)) for img in images]
    images = [transpose(img) for img in images]

    angles = [45 + (90 / (len(image_names) - 1)) * i for i in range(len(image_names))]

    normals = partial_normal_map(angles, images)
    normals = apply_green_screen_to_normals(normals, green_screen_pixels)

    hm = build_heightmap(normals)
    with open("../normals.txt", 'w') as f:
        for column in normals:
            f.write(str(column))
    with open("../height_map.txt", 'w') as f:
        for column in hm:
            f.write(str(column))


    plt.subplot(121)
    plt.imshow(hm, cmap='gray')
    plt.title('Original Image')
    plt.xticks([])
    plt.yticks([])
    plt.subplot(122)
    plt.imshow(normals, cmap = 'gray')
    plt.title('Edge Image')
    plt.show()