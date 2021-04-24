import requests
import cv2
import numpy as np
  
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://130.89.88.108:8080//shot.jpg"
  
# While loop to continuously fetching data from the Url
while True:
    try:
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        x = int(len(img[0])/4)
        xs = int(x * 3)
        cv2.imshow("Android_cam", img[:, x:xs])
    except Exception as e:
        continue
  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()