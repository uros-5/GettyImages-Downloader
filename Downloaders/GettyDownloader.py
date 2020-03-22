from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup

class GettyDownloader():
    def getListOfPhotos(self,url):
        self.urls = []
        while(True):
            try:
                req = requests.get(
                    'https://www.gettyimages.com/photos/manchester-united-fc?family=editorial&phrase=manchester%20united%20fc&sort=mostpopular')
                stranica = BeautifulSoup(req.text,"html.parser")
                slike = stranica.findAll("figure", {"class": "gallery-mosaic-asset__figure"}, "img")

                if (len(list(slike)) == 0):
                    notAvailable = stranica.findAll("h4",{"class":"gallery-no-assets__header"})
                    if (len(list(notAvailable)) > 0):
                        if(notAvailable[0].text.startswith('Sorry')):
                            print('to je to.')
                            return 'NO'
                    else:
                        continue
                elif(len(list(slike)) > 0):
                    self.slike2 = []
                    for i in range(len(slike)):
                        with ThreadPoolExecutor(max_workers=5) as executor:
                            self.slike2.append(str(slike[i].find('img').__getitem__('src')))
                    return self.slike2

                break
            except Exception as e:

                continue