from PIL import Image
from functools import partial
import math
import collections
import os
import urllib
from dir import direction

os.chdir("temp")

# colors used for different wind speed
#               0-5               5-10       10-15           15-20              20-25        25-30            30-35            35-40         black
colors = [(245, 245, 245),(205, 224, 218),(119, 199, 172),(120, 187, 194),(120, 173, 213),(160, 173, 221),(200, 173, 227),(221, 167, 241),(0, 1, 1)]

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
            
            if barva_zdej  == (245, 245, 245):
                brzina.append(0)
            elif barva_zdej  == (205, 224, 218):
                brzina.append(10)
            elif barva_zdej  == (119, 199, 172):
                brzina.append(15)
            elif barva_zdej  == (120, 187, 194):
                brzina.append(20)
            elif barva_zdej  == (120, 173, 213):
                brzina.append(25)
            elif barva_zdej  == (160, 173, 221):
                brzina.append(30)
            elif barva_zdej  == (200, 173, 227):
                brzina.append(30)
            elif barva_zdej  == (221, 167, 241):
                brzina.append(35)    
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

if timesaving == 0 and ura > 3 and ura < 15:
    am_pm='00'
elif timesaving == 1 and ura > 4 and ura < 16:
    am_pm='00'
else:
    am_pm='12'

print am_pm 
    


def aladin(danes, ura, kater):
    
    link = "http://meteo.arso.gov.si/uploads/probase/www/model/aladin/field/ad_"+danes+"-"+am_pm+"00_"+kater+ura+".png"
    check=urllib.urlopen(link)
    urlcheck=check.getcode()
    if urlcheck == 200 :
        urllib.urlretrieve (link, ura+".png")
        
        img = Image.open(ura+".png")
        img = img.convert('RGB')
 
        #istra
        if kater == "vm-va10m_hr-w_" :   
            #liznjan
            img_liz=img.crop((198, 411, 57+198, 52+411))
            hitrost_liz = compute_average_image_color(img_liz)
            img_liz.save('liz.png')
            dir_liz=direction('liz')

            #krk
            img_krk=img.crop((453, 304, 54+453, 38+304))
            hitrost_krk = compute_average_image_color(img_krk)
            img_krk.save('krk.png')
            dir_krk=direction('krk')

            #pre
            img_pre=img.crop((337, 121, 62+337, 45+121))
            hitrost_pre = compute_average_image_color(img_pre)
            img_pre.save('pre.png')
            dir_pre=direction('pre')

            #sav
            img_sav=img.crop((19, 41, 19+21, 41+30))
            hitrost_sav = compute_average_image_color(img_sav)
            img_sav.save('sav.png')
            dir_sav=direction('sav')

            #umag
            img_umag=img.crop((24, 72, 24+26, 28+72))
            hitrost_umag = compute_average_image_color(img_umag)
            img_umag.save('umag.png')
            dir_umag=direction('umag')

             #nov
            img_nov=img.crop((33, 135, 33+23, 135+22))
            hitrost_nov = compute_average_image_color(img_nov)
            img_nov.save('nov.png')
            dir_nov=direction('nov')

            mydata=[('cas',ura),('var','slo_istra'),('slo_liz',hitrost_liz),('slo_krk',hitrost_krk),('slo_pre',hitrost_pre),('slo_sav',hitrost_sav),('slo_umag',hitrost_umag),('slo_nov',hitrost_nov),('smer_liz',dir_liz),('smer_krk',dir_krk),('smer_pre',dir_pre),('smer_sav',dir_sav),('smer_umag',dir_umag),('smer_nov',dir_nov)]   
  

            #print mydata
        
        #primorska
        elif kater == "vm-va10m_si-sw_" :   
            #MJ
            img_mj=img.crop((142, 159, 142+25, 159+20))
            hitrost_mj = compute_average_image_color(img_mj)    
            img_mj.save('mj.png')
            dir_mj=direction('mj')

            #barcole
            img_bar=img.crop((204, 184, 204+42, 184+36))
            hitrost_bar = compute_average_image_color(img_bar)    
            img_bar.save('bar.png')
            dir_bar=direction('bar')

            #portoroz
            img_por=img.crop((154, 308, 154+26, 308+38))
            hitrost_por = compute_average_image_color(img_por)
            img_por.save('por.png')
            dir_por=direction('por')

            mydata=[('cas',ura),('var','slo_pri'),('slo_mj',hitrost_mj),('slo_bar',hitrost_bar),('slo_por',hitrost_por),('smer_mj',dir_mj),('smer_bar',dir_bar),('smer_por',dir_por)]    
            #print mydata
        
       
		#send data to website
        from post import post
        post(mydata)

            
        return    

#aladin(datum, "006", "vm-va10m_hr-w_")
#aladin(datum, "009", "vm-va10m_hr-w_")
#aladin(datum, "012", "vm-va10m_hr-w_")
#aladin(datum, "015", "vm-va10m_hr-w_")
aladin(datum, "018", "vm-va10m_hr-w_")
#aladin(datum, "021", "vm-va10m_hr-w_")
#aladin(datum, "024", "vm-va10m_hr-w_")
#aladin(datum, "027", "vm-va10m_hr-w_")
#aladin(datum, "030", "vm-va10m_hr-w_")
#aladin(datum, "033", "vm-va10m_hr-w_")
#aladin(datum, "036", "vm-va10m_hr-w_")
#aladin(datum, "039", "vm-va10m_hr-w_")
#aladin(datum, "042", "vm-va10m_hr-w_")
#aladin(datum, "045", "vm-va10m_hr-w_")


#aladin(datum, "006", "vm-va10m_si-sw_")
#aladin(datum, "009", "vm-va10m_si-sw_")
#aladin(datum, "012", "vm-va10m_si-sw_")
#aladin(datum, "015", "vm-va10m_si-sw_")
#aladin(datum, "018", "vm-va10m_si-sw_")
#aladin(datum, "021", "vm-va10m_si-sw_")
#aladin(datum, "024", "vm-va10m_si-sw_")
#aladin(datum, "027", "vm-va10m_si-sw_")
#aladin(datum, "030", "vm-va10m_si-sw_")
#aladin(datum, "033", "vm-va10m_si-sw_")
#aladin(datum, "036", "vm-va10m_si-sw_")
#aladin(datum, "039", "vm-va10m_si-sw_")
#aladin(datum, "042", "vm-va10m_si-sw_")
#aladin(datum, "045", "vm-va10m_si-sw_")

#filelist = [ f for f in os.listdir(".") if f.endswith(".png") ]
#for f in filelist:
#    os.remove(f)
