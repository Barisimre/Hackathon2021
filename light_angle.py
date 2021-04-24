from typing import List


def pixel_angle(angles: List[float], images, x, y):
    best_angle = 0
    brightest = 0
    for a in angles:
        for img in images:
            if img[x, y] > brightest:
                best_angle = a
    return best_angle


def partial_normal_map(angles, images):
    normals = [[0 for x in range(len(images[0][0]))] for _ in range(len(images[0]))]

    for x in range(len(images[0][0])):
        for y in range(len(images[0])):
            normals[y][x] = pixel_angle(angles, images, x, y)

    return normals


def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def normal_map(x_angles, y_angles, images):
    x_normals = partial_normal_map(x_angles, images)
    y_normals = partial_normal_map(y_angles, list(map(transpose, images))

    normals = [[(x_normals[y][x], y_normals[y][x]) for x in range(len(images[0][0]))] for y in range(len(images[0]))]
    return normals

def  