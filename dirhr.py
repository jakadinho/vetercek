#!/usr/bin/python
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import matplotlib.path as mplPath
from math import atan2, degrees, pi

def area(p):
    return 0.5 * abs(sum(x0*y1 - x1*y0
                         for ((x0, y0), (x1, y1)) in segments(p)))


def direction2(img):

	height, width, channels = img.shape 
	img = cv2.resize(img, (width*8, height*8))                    
	img = cv2.medianBlur(img,9)
	imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


	ret,th1 = cv2.threshold(imgray,100,255,cv2.THRESH_BINARY)
	edged=cv2.Canny(th1,150,200)
	#return edged



	(img2,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


	kot=[]
	up_c=0
	down_c=0



	for c in cnts:
		area = cv2.contourArea(c)
		#print area
		cv2.drawContours(img,[c],0,(0,255,0),1)
		if area > 500 and area < 1750 and len(c) > 5:	
			#cv2.drawContours(img,[c],0,(0,255,0),1)
			(x,y),radius = cv2.minEnclosingCircle(c)
			center = (int(x),int(y))

			ellipse = cv2.fitEllipse(c)
			(x,y),(MA,ma),angle = cv2.fitEllipse(c)
			cv2.ellipse(img,ellipse,(0,255,0),1)
			#cv2.imshow('img',img)
			#cv2.waitKey(0)
			rect = cv2.minAreaRect(c)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			#print box
			cv2.drawContours(img,[box],0,(0,0,255),1)


			a= math.hypot(box[1][0] - box[0][0], box[1][1] - box[0][1])
			b= math.hypot(box[3][0] - box[0][0], box[3][1] - box[0][1])


			if a>b : 
				xos=(box[0][0]+box[1][0])/2
				yos=(box[0][1]+box[1][1])/2
				xos2=(box[2][0]+box[3][0])/2
				yos2=(box[2][1]+box[3][1])/2

				xosa=(box[1][0]+box[2][0])/2
				yosa=(box[1][1]+box[2][1])/2
				xos2a=(box[0][0]+box[3][0])/2
				yos2a=(box[0][1]+box[3][1])/2


				bbPath = mplPath.Path(np.array([[box[0][0], box[0][1]],[xos, yos],[xos2, yos2],[box[3][0], box[3][1]]]))
				bbPath2 = mplPath.Path(np.array([[box[1][0], box[1][1]], [xos, yos], [xos2, yos2],[box[2][0], box[2][1]]]))

				#pol=np.array([[box[1][0], box[1][1]], [xos, yos], [xos2, yos2],[box[2][0], box[2][1]]])
				#cv2.drawContours(img,[pol],0,(0,0,255),1)


			else: 	
				xos=(box[1][0]+box[2][0])/2
				yos=(box[1][1]+box[2][1])/2
				xos2=(box[0][0]+box[3][0])/2
				yos2=(box[0][1]+box[3][1])/2

				xosa=(box[0][0]+box[1][0])/2
				yosa=(box[0][1]+box[1][1])/2
				xos2a=(box[2][0]+box[3][0])/2
				yos2a=(box[2][1]+box[3][1])/2


				
				bbPath = mplPath.Path(np.array([[box[0][0], box[0][1]],[box[1][0], box[1][1]], [xos, yos], [xos2, yos2]]))
				bbPath2 = mplPath.Path(np.array([[box[3][0], box[3][1]],[box[2][0], box[2][1]], [xos, yos], [xos2, yos2]]))

				#pol=np.array([[box[3][0], box[3][1]],[box[2][0], box[2][1]], [xos, yos], [xos2, yos2]])
				#cv2.drawContours(img,[pol],0,(0,0,255),1)

			r = 5 # accuracy
			dots_down=[]
			dots_up=[]
			for dot in c:
				#print bbPath
				result= bbPath.contains_point((dot[0][0], dot[0][1]),radius=r) or bbPath.contains_point((dot[0][0], dot[0][1]),radius=-r)
				result2= bbPath2.contains_point((dot[0][0], dot[0][1]),radius=r) or bbPath2.contains_point((dot[0][0], dot[0][1]),radius=-r)			

				if result == True : 	
					nov = [dot[0][0], dot[0][1]]
					dots_down.append(nov)

				if result2 == True : 
					nov = [dot[0][0], dot[0][1]]
					dots_up.append(nov)
					cv2.circle(img, (dot[0][0],dot[0][1]), 2, (255, 0, 0), -1)
					#print nov

			#if contour is closed
			#if cv2.isContourConvex(c):
			down=np.array(dots_down)
			up=np.array(dots_up)
			#area_down = cv2.contourArea(down)
			#area_up = cv2.contourArea(up)


			area_up = cv2.contourArea(np.array(up).reshape((-1,1,2)).astype(np.int32))
			area_down = cv2.contourArea(np.array(down).reshape((-1,1,2)).astype(np.int32))

			#else:
			#area_down = 20
			#area_up = 1	
				#print 'not convex'			



			#print area_up
			#print area_down
			#print area_up
			#print angle

			if area_up > area_down:
				up_c=up_c+1
				#kot.append(round(angle,-1)) 	
				#print 'UP'
				#print round(degs,-1)
				#print round(angle,-1)
				kot.append(round(angle,-1))


			else:
				down_c=down_c+1
				#kot.append(round(angle,-1)) 
				down_c=down_c+1
				#print 'DOWN'
				kot.append(round(angle,-1)) 	


			cv2.drawContours(img, [c], -1, (0, 255, 255), 1)
			cv2.circle(img, center, 1, (125, 125, 0), -1)

	#pokazi
	#cv2.imshow('img',img)
	#cv2.waitKey(0)



	d = {}
	if kot:
		for elm in kot:
			d[elm] = d.get(elm, 0) + 1
		counts = [(j,i) for i,j in d.items()]
		count, angle = max(counts)

		#preracunaj kot
		if down_c > up_c and angle > 90:
			#print 'up'
			angle =180+angle
		elif up_c > down_c and angle < 90:
			angle =180+angle



		if angle >= 337.5 and angle <= 360:
			smer = 'N'
		elif angle >=0 and angle <22.5:
			smer = 'N'
		elif angle >=22.5 and angle <67.5:
			smer = 'NE'
		elif angle >=67.5 and angle <112.5:
			smer = 'E'
		elif angle >=112.5 and angle <157.5:
			smer = 'SE'
		elif angle >=157.5 and angle <202.5:
			smer = 'S'
		elif angle >=202.5 and angle <247.5:
			smer = 'SW'
		elif angle >=247.5 and angle <292.5:
			smer = 'W'
		elif angle >=292.5 and angle <337.5:
			smer = 'NW'
		else:
			smer=0

		return smer
		#print smer
		#print angle




	#cv2.imshow('img',img)
	#cv2.waitKey(0)



