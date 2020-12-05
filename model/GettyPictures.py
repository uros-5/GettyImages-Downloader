import time
from urllib.request import urlopen
from PIL import Image, ImageTk
import io

class GettyPicutes(object):
    photo_urls = {}
    counter = 0
    saved_photos_counter = 0
    to_download = True

    def save_photo(self,key,value=0):
        if key not in self.photo_urls:
            self.photo_urls[key] = value
        elif key in self.photo_urls and value == 1:
            self.saved_photos_counter += 1
            return None
        elif key in self.photo_urls and self.photo_urls[key] != 0:
            self.saved_photos_counter += 1
            return None
        else:
            self.photo_urls[key] = self.create_tk_image(key)
            self.saved_photos_counter += 1

    def to_dl(self):
        if self.to_download == True:
            return True
        else:
            return False

    def not_saved(self):
        if self.saved_photos_counter == 0:
            return True
        if self.saved_photos_counter < self.counter and self.counter >= 0:
            return True
        
        else:
            return False
    
    def create_tk_image(self,url):
        image_url = urlopen(url)
        my_picture = io.BytesIO(image_url.read())
        im = Image.open(my_picture)
        width, height = im.size

        pil_img = Image.open(my_picture).resize((int(im.size[0]/2), int(im.size[1]/2)), Image.NONE)
        tk_img = ImageTk.PhotoImage(pil_img)
        pil_img.close()
        return tk_img

    def get_tk_image(self,url):
        return self.photo_urls[url]

    def reset_all(self):
        self.counter = 0
        self.saved_photos_counter = 0
        self.to_download = False



    