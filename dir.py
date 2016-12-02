#!/usr/bin/python
import cv2
import numpy as np
from matplotlib import pyplot as plt


def direction(img):
	img_rgb = cv2.imread(img+'.png')
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	all_dir=[]

	directions=[('n','n'),('s','s'),('se','se1'),('w','w1'),('ne','ne1','ne2','ne3')]
	#directions=['ne']
	for directions2 in directions:
		smer =directions2[0]
		count=0 

		for direction in directions2:
		
			template = cv2.imread(direction+'.png',0)
			w, h = template.shape[::-1]

			res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
			threshold = 0.80
			loc = np.where( res >= threshold)
			for pt in zip(*loc[::-1]):
				cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
				count=count+1
			#cv2.imshow("Results", img_rgb)
			#cv2.waitKey(0)

		#print smer, count
		all_dir.append([smer, count])


	cv2.imshow("Results", img_rgb)
	cv2.waitKey(0)
	most_common=sorted(all_dir,key=lambda x: x[1], reverse=True)

	if most_common[0][1] > 0 :   
		return most_common[0][0]
	else :
		return ' '
	
