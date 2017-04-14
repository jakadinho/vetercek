from PIL import Image
from functools import partial
import math
import collections
import os
import urllib

os.chdir("temp")

# colors used for different wind speed
#               0               5-10       10-15           15-20            20-25        25-30          30-35      35-40         crna           modra
colors = [(255, 255, 255),(0, 209, 140),(161, 230, 51),(230, 220, 51),(230, 176, 46),(240, 130, 41),(240, 0, 0),(221, 167, 241),(220, 0, 99),(31, 61, 250)]

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
            elif barva_zdej  == (0, 209, 140):
                brzina.append(10)
            elif barva_zdej  == (161, 230, 51):
                brzina.append(15)
            elif barva_zdej  == (230, 220, 51):
                brzina.append(20)
            elif barva_zdej  == (230, 176, 46):
                brzina.append(25)
            elif barva_zdej  == (240, 130, 41):
                brzina.append(30)
            elif barva_zdej  == (240, 0, 0):
                brzina.append(30)
            elif barva_zdej  == (220, 0, 99):
                brzina.append(35)    
            elif barva_zdej  == (0, 1, 1):
                pass  
            elif barva_zdej  == (31, 61, 250):
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


def aladin(danes, ura, kater):
    link ="http://prognoza.hr/aladinHR/web_uv10_"+kater+"_"+ura+".png"
    check=urllib.urlopen(link)
    urlcheck=check.getcode()
    if urlcheck == 200 :
        urllib.urlretrieve (link, ura+".png")

        img = Image.open(ura+".png")
        img = img.convert('RGB')
 
        #liznjan
        img_liz=img.crop((294, 391, 294+34, 391+24))
        hitrost_liz = compute_average_image_color(img_liz)
        #krk
        img_krk=img.crop((491, 307, 491+31, 307+34))
        hitrost_krk = compute_average_image_color(img_krk)
        #pre
        img_pre=img.crop((399, 183, 399+30, 183+23))
        hitrost_pre = compute_average_image_color(img_pre)
        #sav
        img_sav=img.crop((128, 127, 128+25, 127+18))
        hitrost_sav = compute_average_image_color(img_sav)
        #umag
        img_umag=img.crop((123, 155, 123+24, 155+25))
        hitrost_umag = compute_average_image_color(img_umag)
        #nov
        img_nov=img.crop((156, 268, 156+25, 268+26))
        hitrost_nov = compute_average_image_color(img_nov)
        #por
        img_por=img.crop((148, 122, 148+23, 122+18))
        hitrost_por = compute_average_image_color(img_por)
        #bar
        img_bar=img.crop((193, 51, 193+40, 51+22))
        hitrost_bar = compute_average_image_color(img_bar)
            
        print "cas: ", ura  
        print "hitrost liznjan: ", hitrost_liz  
        print "hitrost krk: ", hitrost_krk  
        print "hitrost preluka: ", hitrost_pre 
        print "hitrost savudrija: ", hitrost_sav
        print "hitrost umag: ", hitrost_umag
        print "hitrost novigrad: ", hitrost_nov
        print "hitrost portoroz: ", hitrost_por
        print "hitrost barcole: ", hitrost_bar
       
        mydata=[('cas',ura),('var','hr'),('liz',hitrost_liz),('krk',hitrost_krk),('pre',hitrost_pre),('sav',hitrost_sav),('umag',hitrost_umag),('nov',hitrost_nov),('por',hitrost_por),('bar',hitrost_bar)]    
        
        #send data to website
        from post import post
        post(mydata)
            

            
        return    

aladin(datum, "06", "SENJ")
aladin(datum, "09", "SENJ")
aladin(datum, "12", "SENJ")
aladin(datum, "15", "SENJ")
aladin(datum, "18", "SENJ")
aladin(datum, "21", "SENJ")
aladin(datum, "24", "SENJ")
aladin(datum, "27", "SENJ")
aladin(datum, "30", "SENJ")
aladin(datum, "33", "SENJ")
aladin(datum, "36", "SENJ")
aladin(datum, "39", "SENJ")
aladin(datum, "42", "SENJ")
aladin(datum, "45", "SENJ")
aladin(datum, "48", "SENJ")
aladin(datum, "51", "SENJ")
aladin(datum, "54", "SENJ")
aladin(datum, "57", "SENJ")
aladin(datum, "60", "SENJ")
aladin(datum, "63", "SENJ")
aladin(datum, "66", "SENJ")
aladin(datum, "69", "SENJ")
aladin(datum, "72", "SENJ")

filelist = [ f for f in os.listdir(".") if f.endswith(".gif") ]
for f in filelist:
    os.remove(f)
