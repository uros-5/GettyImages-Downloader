from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import urllib.request
class GettyDownloader():
    def getListOfPhotos(self,url):
        self.urls = []
        while(True):
            try:
                req = requests.get(url)
                stranica = BeautifulSoup(req.text,"html.parser")
                slike = stranica.findAll("figure", {"class": "gallery-mosaic-asset__figure"})

                if (len(list(slike)) == 0):
                    notAvailable = stranica.findAll("h4",{"class":"gallery-no-assets__header"},"img")
                    if (len(list(notAvailable)) > 0):
                        if(notAvailable[0].text.startswith('Sorry')):
                            return 'NO'
                    else:
                        continue
                elif(len(list(slike)) > 0):
                    self.slike2 = []
                    # if()
                    for i in range(len(slike)):
                        with ThreadPoolExecutor(max_workers=5) as executor:
                            if(slike[i].find('img').has_attr('src')):
                                self.slike2.append(str(slike[i].find('img').__getitem__('src')))
                    return self.slike2

                break
            except Exception as e:
                continue
    def download_zip(self,podaci):
        zipFajl = ''
        imefajla=''
        brojac = 0
        imefoldera = ""
        while(True):
            imefoldera = 'download_GettyImages'+str(brojac)
            if(imefoldera not in os.listdir('Slike/')):
                os.mkdir('Slike/'+imefoldera)
                break
            brojac+=1
        for i in range(len(podaci)):
            url = podaci[i]
            podatak = urllib.request.urlretrieve(url, "Slike/"+imefoldera+"/Slika_"+str(i)+".jpg")
        return "Slike\\"+imefoldera