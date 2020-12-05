import os
import urllib.request

class SelectedPictures(object):

    pictures = []
    widgets = []

    def add_picture(self,url,widget):
        if url not in self.pictures:
            widget['borderwidth'] = 5
            widget['relief'] = 'groove'
            widget["highlightcolor"] = "black"
            self.pictures.append(url)
            self.widgets.append(widget)
        else:
            widget['borderwidth'] = 0
            widget['relief'] = 'groove'
            del self.pictures[self.pictures.index(url)]
            del self.widgets[self.widgets.index(widget)]

    def download(self):
        if len(self.pictures) > 0:
            folder = self.create_folder()
            self.save_all_photos(folder)
        self.remove_all()

    def save_all_photos(self,folder):
        for i in range(len(self.pictures)):
            print(i)
            urllib.request.urlretrieve(self.pictures[i],f'{folder}/{i}.jpg')

    def create_folder(self):
        counter = 0
        while(True):
            imefoldera = 'download_getty_pictures'+str(counter)
            if(imefoldera not in os.listdir(os.getcwd())):
                os.mkdir(imefoldera)
                return imefoldera
            counter += 1
                
    def remove_all(self):
        for widget in self.widgets:
            widget['borderwidth'] = 0
            widget['relief'] = 'groove'
        self.widgets = []
        self.pictures = []