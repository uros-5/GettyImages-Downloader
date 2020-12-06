import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import urllib.request
from model.GettyImage import GettyImage

class Downloader(object):
    
    def __init__(self,models):
        self.search_details = models["SearchDetails"]
        self.getty_pictures = models["GettyPictures"]
        self.current_page = models["CurrentPage"]

    def start_download_all(self):
        self.thread_download = threading.Thread(target=self.__download_all)
        self.thread_download.start()
    
    def __download_all(self):
        while True:
            req = requests.get(self.search_details.url)
            self.stranica = BeautifulSoup(req.text,"html.parser")
            self.slike = self.stranica.findAll("figure", {"class": "gallery-mosaic-asset__figure"})

            if len(list(self.slike)) == 0:
                is_avaliable = self.not_available_url()
                if is_avaliable:
                    continue
                else:
                    self.getty_pictures.to_download = False
                    break
            
            elif len(list(self.slike)) > 0:
                for i in range(len(self.slike)):
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        if self.slike[i].find('img').has_attr('src'):
                            getty_image = GettyImage(self.slike[i])
                            self.getty_pictures.append(getty_image)
                            self.current_page.urls.append(getty_image.url)
            break
    
    def get_src(self,item):
        return str(item.find('img').__getitem__('src'))

    def not_available_url(self):
        notAvailable = self.stranica.findAll("h4",{"class":"gallery-no-assets__header"},"img")
        if len(list(notAvailable)) > 0:
            if notAvailable[0].text.startswith('Sorry') :
                return False
        else:
            return True
    