import math
import pickle
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv


def build_heightmap(normals):
    heights = [[0 for _ in range(len(normals[0]))] for _ in range(len(normals))]
    height_differences = [[(math.sin(x / 180 * 3.1415), math.sin(y / 180 * 3.1415)) for (x, y) in columns] for columns in normals]

    bla = [[r for r, _ in column] for column in height_differences]

    plt.imshow(bla, cmap = 'gray')
    plt.show()
    # height_differences = np.array([row - np.mean(row) for row in height_differences])
    # for row in height_differences:
    #     row -= np.mean(row)
    #     print("Fixed numbers", np.mean(row), sum(row))
    # for row in height_differences:
    #     print("Should be 0", np.mean(row), sum(row))


    max_height = 0
    min_height = 0
    for y in range(1, len(normals)):
        for x in range(1, len(normals[0])):
            #print(normals[y][x])
            height_difference = height_differences[y][x][0]
            if y == 204:
                print(height_difference)

            heights[y][x] = (heights[y][x - 1]) * 0.99 + height_difference
            # heights[y][x] -= (x / 3000)
            # heights[y][x] += (y / 800)

            if heights[y][x] > max_height:
                max_height = heights[y][x]

            if heights[y][x] < min_height:
                min_height = heights[y][x]
    # heights = [[max(-1, min(1, x)) for x in col] for col in heights]

    # print(max_height, min_height)

    # heights = [[((px + min_height) / (max_height - min_height)) * 128 for px in column] for column in heights]
    return np.array(heights)


if __name__ == "__main__":
    with open("normals", "rb") as f:
        normals = pickle.load(f)

    normals = [[px - (index / 80) for index, px in enumerate(col)] for col in normals]

    # kernel = np.ones((5, 5), np.float32) / 25
    # normals = cv.filter2D(normals, -1, kernel)




    print("corrected normal: ", np.mean(normals))


    hm = build_heightmap(normals)

    bla = [[r for r, _ in column] for column in normals]



    plt.subplot(121)
    plt.imshow(hm, cmap='gray')
    plt.title('Original Image')
    plt.xticks([])
    plt.yticks([])
    plt.subplot(122)
    plt.imshow(bla, cmap = 'gray')
    plt.title('Edge Image')
    plt.show()
