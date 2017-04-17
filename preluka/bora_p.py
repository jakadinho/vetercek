from PIL import Image
from functools import partial
import math
import collections
import os
import urllib
import numpy as np


os.chdir("temp")

# colors used for different wind speed
colors = [(255, 255, 255),(181,201,255),(99,112,247),(0,150,150),(99,255,0),(198,255,51),(255,160,0),(255,25,0),(0, 1, 1)]

def distance(color1, color2):
    return math.sqrt(sum([(e1-e2)**2 for e1, e2 in zip(color1, color2)]))

def best_match(sample, colors):
    by_distance = sorted(colors, key=lambda c: distance(c, sample))
    return by_distance[0]


def compute_average_image_color(img):
    width, height = img.size

    brzina = []

    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x,y))
            rgb = (r, g, b)
            barva_zdej = best_match(rgb,colors)
            
            if barva_zdej  == (255, 255, 255):
                brzina.append(0)
            elif barva_zdej  == (181,201,255):
                brzina.append(0.1)
            elif barva_zdej  == (99,112,247):
                brzina.append(2)
            elif barva_zdej  == (0,150,150):
                brzina.append(5)
            elif barva_zdej  == (99,255,0):
                brzina.append(10)
            elif barva_zdej  == (198,255,51):
                brzina.append(20)
            elif barva_zdej  == (255,160,0):
                brzina.append(3)
            elif barva_zdej  == (255,25,0):
                brzina.append(50)    
            elif barva_zdej  == (0, 1, 1):
                pass   
 

               
    counter=collections.Counter(brzina)
    naj=counter.most_common(2)
    
    if len(naj)  > 1:
        hitrost=((naj[0][0]*naj[0][1])+(naj[1][0]*naj[1][1]))/((naj[0][1])+(naj[1][1]))
    else:
        hitrost = naj[0][0]
    return (hitrost)

import datetime
today = datetime.date.today()
datum = today.strftime('%Y%m%d')

#glede na UTC cas
import time
ura = int(time.strftime("%H"))
timesaving=time.localtime()[8]

if timesaving == 0 and ura > 0 and ura < 15:
    am_pm='00'
elif timesaving == 1 and ura > 1 and ura < 16:
    am_pm='00'
else:
    am_pm='12'


danes = datetime.date.today()
danes1 = datetime.date.today() + datetime.timedelta(days=1)
danes2 = datetime.date.today() + datetime.timedelta(days=2)
danes3 = datetime.date.today() + datetime.timedelta(days=3)
danes4 = datetime.date.today() + datetime.timedelta(days=4)
danes5 = datetime.date.today() + datetime.timedelta(days=5)
danes6 = datetime.date.today() + datetime.timedelta(days=6)
datum1 = danes.strftime('%Y_%m_%d_')
datum2 = danes1.strftime('%Y_%m_%d_')
datum3 = danes2.strftime('%Y_%m_%d_')
datum4 = danes3.strftime('%Y_%m_%d_')
datum5 = danes4.strftime('%Y_%m_%d_')
datum6 = danes5.strftime('%Y_%m_%d_')
datum7 = danes6.strftime('%Y_%m_%d_')

if timesaving == 0:
    ura1='01'
    ura2='04'
    ura3='07'
    ura4='10'
    ura5='13'
    ura6='16'
    ura7='19'
    ura8='22'

else:
    ura1='02'
    ura2='05'
    ura3='08'
    ura4='11'
    ura5='14'
    ura6='17'
    ura7='20'
    ura8='23'


my_list = []

if am_pm == '00':
    my_list.extend([datum2+ura1,datum2+ura2,datum2+ura3])

else :
    my_list.extend([datum2+ura1,datum2+ura2,datum2+ura3])

#test    
#my_list=[datum1+ura7]



ura=-3    
for list in my_list:
    ura=ura+3    
    link = "http://bora.gekom.hr/png_wrf/Kvarner/clflo_"+list+".png"


    check=urllib.urlopen(link)
    urlcheck=check.getcode()
    if urlcheck == 200 :
        urllib.urlretrieve (link, str(ura)+".png")

        img = Image.open(str(ura)+".png")
        img = img.convert('RGB')
 
     

        #preluka
        img_pre=img.crop((163, 63, 92+84, 63+71))
        hitrost_pre = round(compute_average_image_color(img_pre))        


        
        mydata=[('cas',ura),('var','bora_p'),('pre',hitrost_pre)]    
        
        from post import post
        post(mydata)
        print mydata
        

filelist = [ f for f in os.listdir(".") if f.endswith(".png") ]
for f in filelist:
    os.remove(f)
