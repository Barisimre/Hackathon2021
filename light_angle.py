from typing import List
import cv2 as cv
import os
from matplotlib import pyplot as plt
from height_map import build_heightmap
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


if __name__ == "__main__":
    os.chdir("img/img_dump")
    image_names = os.listdir()
    images = [cv.imread(img_name, 0) for img_name in image_names]
    images = [transpose(img) for img in images]
    angles = [45 + (90 / (len(image_names) - 1)) * i for i in range(len(image_names))]

    normals = partial_normal_map(angles, images)
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