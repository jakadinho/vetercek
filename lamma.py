from PIL import Image
from functools import partial
import math
import collections
import os
import urllib
from dir import direction2
import numpy as np


os.chdir("temp")

# colors used for different wind speed
colors = [(245, 255, 255),(150,210,250),(80,165,245),(18,81,166),(0,210,120),(0,160,0),(225,20,0),(165,0,0),(255,0,255),(255,170,255),(255,150,0),(249,100,1),(19, 19, 19),(208, 208, 208)]

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
            

            if barva_zdej  == (245,255,255):
                brzina.append(1)
            elif barva_zdej  == (150,210,250):
                brzina.append(3)
            elif barva_zdej  == (80,165,245):
                brzina.append(6)
            elif barva_zdej  == (18,81,166):
                brzina.append(10)
            elif barva_zdej  == (0,210,120):
                brzina.append(16)
            elif barva_zdej  == (0,160,0):
                brzina.append(21)
            elif barva_zdej  == (225,20,0):
                brzina.append(27)    
            elif barva_zdej  == (165,0,0):
                brzina.append(33) 
            elif barva_zdej  == (255,0,255):
                brzina.append(40) 
            elif barva_zdej  == (255,170,255):
                brzina.append(47)
            elif barva_zdej  == (255,150,0):
                brzina.append(55)    
            elif barva_zdej  == (249,100,1):
                brzina.append(63) 
            elif barva_zdej  == (19, 19, 19):
                pass   
            elif barva_zdej  == (208, 208, 208):
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

if timesaving == 0 and ura > 3 and ura < 15:
    am_pm='00'
elif timesaving == 1 and ura > 4 and ura < 16:
    am_pm='00'
else:
    am_pm='12'





if am_pm == '00':
    my_list=np.arange(7, 49, 3)

else :
    my_list=np.arange(7, 49, 3)

    

for list in my_list:
    ura=list-1

    link = "http://www.lamma.rete.toscana.it/models/ventoemare/wind10m_T_web_"+str(list)+".png"
    check=urllib.urlopen(link)
    urlcheck=check.getcode()
    if urlcheck == 200 :
        urllib.urlretrieve (link, str(ura)+".png")

        img = Image.open(str(ura)+".png")
        img = img.convert('RGB')
 
         #liznjan
        img_liz=img.crop((455, 302, 455+13, 302+8))
        hitrost_liz = round(compute_average_image_color(img_liz))

        #krk
        img_krk=img.crop((590, 253, 590+9, 253+5))
        hitrost_krk = round(compute_average_image_color(img_krk))        

        #preluka
        img_pre=img.crop((530, 165, 530+12, 165+4))
        hitrost_pre = round(compute_average_image_color(img_pre))        

        #savudrija
        img_sav=img.crop((336, 114, 336+8, 114+7))
        hitrost_sav = round(compute_average_image_color(img_sav))        

        #umag
        img_umag=img.crop((338, 139, 338+7, 139+6))
        hitrost_umag = round(compute_average_image_color(img_umag))        

        #novigrad
        img_nov=img.crop((345, 166, 345+5, 166+6))
        hitrost_nov = round(compute_average_image_color(img_nov))          
 
         #portoroz
        img_por=img.crop((355, 116, 355+6, 116+6))
        hitrost_por = round(compute_average_image_color(img_por))     

        #mj
        img_mj=img.crop((348, 47, 348+7, 47+5))
        hitrost_mj = round(compute_average_image_color(img_mj)) 

        #bar
        img_bar=img.crop((390, 68, 390+6, 68+6))
        hitrost_bar = round(compute_average_image_color(img_bar)) 
        
        
        mydata=[('cas',ura),('var','lamma'),('liz',hitrost_liz),('krk',hitrost_krk),('pre',hitrost_pre),('sav',hitrost_sav),('umag',hitrost_umag),('nov',hitrost_nov),('por',hitrost_por),('mj',hitrost_mj),('bar',hitrost_bar)]    
        
        from post import post
        post(mydata)
        print mydata
        

#filelist = [ f for f in os.listdir(".") if f.endswith(".png") ]
#for f in filelist:
#    os.remove(f)
        
