#!/usr/bin/python
import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('sample.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

directions=['n','ne','s']
for direction in directions:   
	template = cv2.imread(direction+'.png',0)
	w, h = template.shape[::-1]

	count=0 
	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.85
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
		cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
		count=count+1
	#cv2.imwrite('res.png',img_rgb)

	print 'dir', direction, count

	# Show blobs
	cv2.imshow("Keypoints", img_rgb)
	cv2.waitKey(0)

