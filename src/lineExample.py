# Rhys Read
# camControl main.py

import numpy as np
import cv2

img = np.zeros((512, 512, 3), np.uint8)

# Draw a diagonal blue line with a thickness of 5 px
# Args as follows: image, pos1, pos2, color, thickness
img = cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 2)

cv2.imshow("window", img)
cv2.waitKey(0)
