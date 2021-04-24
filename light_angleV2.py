from typing import List
import cv2 as cv
import os
from matplotlib import pyplot as plt
from height_map import build_heightmap
import numpy as np
import pickle


def pixel_angle(angles, images, x, y):
    best_angle = (0, 0)
    brightest = 0


    if x > len(images[0][0]) - 1 or x < 1 or y > len(images[0]) or y < 1:
        return (0, 0)

    for i, a in enumerate(angles):
        img = images[i]
        area = img[y-1:y+2, x-1:x+2]
        # area = cropped
        # print("x", x, "y", y)
        # print("Area", area)
        brightness = np.mean(area)

        if brightness > brightest:
            brightest = brightness
            best_angle = a

    return best_angle


def normal_map(angles, images):
    normals = [[0 for x in range(len(images[0][0]))] for _ in range(len(images[0]))]
    print(f"Image dimensions: {len(images[0][0])} {len(images[0])}")

    for x in range(len(images[0][0])):
        print("column: ", x)
        for y in range(len(images[0])):
            normals[y][x] = pixel_angle(angles, images, x, y)

    return np.array(normals)


def transpose(matrix):
    return np.array([[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))])


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


def crop(img):
    return np.array(img[150:950, 350:650])


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result

def apply_green_screen_to_normals(normals, green_screen):
    for x in range(len(normals[0])):
        for y in range(len(normals)):
            if green_screen[y][x]:
                normals[y][x] = 90
    return normals


if __name__ == "__main__":
    TopImage = cv.imread('light_data/Top.jpg')
    LeftImage = cv.imread('light_data/Left.jpg')
    RightImage = cv.imread('light_data/Right.jpg')
    FrontImage = cv.imread('light_data/Front.jpg')


    images = [TopImage, LeftImage, RightImage, FrontImage]
    images = [img[1888:2283, 1223:2215] for img in images]
    images = [rotate_image(img, -5) for img in images]

    plt.imshow(images[0], cmap='gray')
    plt.show()
    # images = [cv.resize(img, (1000, 750)) for img in images]

    angles = [(0, 0), (-15, 0), (15, 0), (0, -15)]
    normals = normal_map(angles, images)
    print(normals)

    bla = [[r for r, _ in column] for column in normals]
    print(bla)


    hm = build_heightmap(normals)
    with open("normals", 'wb') as f:
        pickle.dump(normals, f)
    with open("height_map.txt", 'w') as f:
        for column in hm:
            f.write(str(column))

    plt.subplot(121)
    plt.imshow(hm, cmap='gray')
    plt.xticks([])
    plt.yticks([])
    plt.subplot(122)
    plt.imshow(bla, cmap='gray')
    plt.show()