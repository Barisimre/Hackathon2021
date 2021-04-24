import cv2
import numpy as np



def green_screen(filename):

    image = cv2.imread(filename)
    image_copy = np.copy(image)
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
    kernel = np.ones((20,20),np.float32)/400
    image_copy = cv2.filter2D(image_copy,-1,kernel)
    plt.imshow(image_copy)

    lower_blue = np.array([0, 180, 0])
    upper_blue = np.array([180, 255, 180]) 

    mask = cv2.inRange(image_copy, lower_blue, upper_blue)
    mask2 = cv2.inRange(image, lower_blue, upper_blue)

    masked_image = np.copy(image)
    masked_image[mask != 0] = [255, 0, 0]
    more_masked = np.copy(masked_image)
    more_masked[mask2 != 0] = [255, 0, 0]
    res = np.zeros((len(more_masked), len(more_masked[0]), 1))

    for y in range(len(more_masked)):
        for x in range(len(more_masked[y])):
            test = tuple(np.array((255, 0, 0)))
            test1 = tuple(np.array(more_masked[y][x]))
            if test1 == test:
                res[y][x] = 1

    # This is basically a mask
    return res

    # return more_masked


a = green_screen('img/img_dump/a.jpeg')
plt.imshow(a)
plt.show()