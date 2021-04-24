import math

def build_heightmap(normals):
    heights = [[0 for _ in range(len(normals[0]))] for _ in range(len(normals))]

    max_height = 0
    min_height = 0
    for y in range(1, len(normals)):
        for x in range(len(normals[0])):
            height_difference = math.cos(normals[y][x])
            heights[y][x] = height_difference
            # heights[y][x] = heights[y][x - 1] + height_difference

            if heights[y][x] > max_height:
                max_height = heights[y][x]

            if heights[y][x] < min_height:
                min_height = heights[y][x]

    print(max_height, min_height)

    heights = [[((px + min_height) / (max_height - min_height)) * 128 for px in column] for column in heights]
    return heights

if __name__ == "__main__":

    build_heightmap()

