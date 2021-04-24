import cv2 as cv
from get_greenscreen import get_green_screen
from heightmap_to_mesh import get_stl
import matplotlib.pyplot as plt
from stlToGLTF import stl_to_gltf


def get_heightmap(image):
    
    return 
    


def image_to_gltf(filepath):

    image = cv.imread(filepath)
    heightmap = cv.imread(filepath, 0)
    background_pixels = get_green_screen(image)

    stl_path = get_stl(heightmap, background_pixels)

    gltf_path = "gltf/keyboard.gltf"

    stl_to_gltf(stl_path, gltf_path, True)

    
#a = image_to_gltf('img/img_dump/a.jpeg')
#plt.imshow(a, cmap='gray')
#plt.show()


image_to_gltf('img/img_dump/a.jpeg')