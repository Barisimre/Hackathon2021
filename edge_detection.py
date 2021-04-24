import cv2 as cv
from matplotlib import pyplot as plt

src_folder = "img/keyboard_daan/"
dest_folder = "edge_detection/"

threshold = 20

def get_bounds(img):
    width = len(img[0])
    height = len(img)

    print(width, height)

    low_x = 0
    low_y = 0
    high_x = width
    high_y = height


    # Low bound
    for x in range(0, width):
        for y in range(0, height):
            if img[y][x] < threshold:
                break
        else:
            continue
        low_x = x
        break
    for y in range(0, height):
        for x in range(0, width):
            if img[y][x] < threshold:
                break
        else:
            continue
        low_y = y
        break

    # High bound
    for x in range(width - 1, -1, -1):
        for y in range(0, height):
            if img[y][x] < threshold:
                break
        else:
            continue
        high_x = x
        break
    for y in range(height - 1, -1, -1):
        for x in range(0, width):
            if img[y][x] < threshold:
                break
        else:
            continue
        high_y = y
        break
    return (low_x, low_y), (high_x, high_y)


def crop(img):
    (low_x, low_y), (high_x, high_y) = get_bounds(img)
    print("Bounds", low_x, low_y, high_x, high_y)
    return img[low_y:high_y, low_x:high_x]


def edge_detection(img):
    return cv.Canny(img, 100, 200)






if __name__ == "__main__":

    img1 = cv.imread(src_folder + "keyboard1.jpg", 0)
    img2 = cv.imread(src_folder + "keyboard2.jpg", 0)
    #
    # for x in range(len(img1[0])):
    #     for y in range(len(img1)):
    #         img1[y][x] = 100 if img1[y][x] > threshold else 0



    plt.subplot(121)
    plt.imshow(edge_detection(crop(img2)), cmap = 'gray')
    plt.title('Original Image')
    plt.xticks([])
    plt.yticks([])
    plt.subplot(122)
    plt.imshow(edge_detection(crop(img1)), cmap = 'gray')
    plt.title('Edge Image')
    plt.xticks([])
    plt.yticks([])
    plt.show()
    print("done")