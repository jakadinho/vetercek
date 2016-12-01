#!/usr/bin/python
import cv2
import numpy as np;

# load the image
image = cv2.imread('liz.jpg')
# find all the 'orange' shapes in the image
upper = np.array([80, 80, 80])
lower = np.array([0, 0, 0])

shapeMask = cv2.inRange(image, lower, upper)
new_file=open('filtered.jpg','wb')

#cv2.imshow("Keypoints", shapeMask)
#cv2.waitKey(0)

cv2.imwrite('filtered.jpg',shapeMask)
new_file.close()
