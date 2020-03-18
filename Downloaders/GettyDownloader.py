from selenium import webdriver
import base64
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
driver = webdriver.Firefox()

def getListOfPhotos(url):
    driver.get(url)
    while(True):
        try:
            slike = driver.find_elements_by_xpath("//figure[contains(@class,'gallery-mosaic')]//img")
            if (len(slike)==0):
                notAvailable = driver.find_elements_by_xpath("//h4[contains(@class,'gallery-no')]")
                if (len(notAvailable)>0):
                    print('to je to.')
                    return 'NO'
                else:
                    continue
            elif(len(slike)>0):
                slike2 = []
                for i in range(len(slike)):
                    # slike2.append(i.get_attribute('src'))
                    image_url = urlopen(slike[i].get_attribute('src'))
                    my_picture = io.BytesIO(image_url.read())
                    pil_img = Image.open(my_picture).resize((152, 152), Image.NONE)
                    tk_img = ImageTk.PhotoImage(pil_img)
                    slike2.append(tk_img)
                return slike2

            break
        except:
            continue