import requests
import cv2
import numpy as np
import time
import copy
import os
import glob


def get_video(seconds, ip):

    print('Cleaning the folder')
    files = glob.glob('img/img_dump/*.png', recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print('Could not remove the files')

    print('Folder cleaned')



    print('Started to get video')
    print('Waiting for camera...')

    while True:
        try:
            url = f"http://{ip}:8080//shot.jpg"
            hacky_image = requests.get(url)
        except Exception as e:
            continue
        break
    print('Connected to camera')

    video = []
    arr = []
    raw = []
    start = time.time()
    print("Capturing images")
    while time.time() - start < seconds:
        img_resp = requests.get(url)
        raw.append(img_resp)

    print("Processing images")

    for r in raw:

        img_arr = np.array(bytearray(r.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        x = int(len(img[0])/4)
        xs = int(x * 3)
        # cropped = img[: , x:xs]
        video.append((img, time.time()))

    for v in video:
        cv2.imwrite(f"img/img_dump/{v[1]}.png", v[0])

    print(f'Done, {len(video)} images are in the folder')


# get_video(7)