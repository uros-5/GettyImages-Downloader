from urllib.request import urlopen
from PIL import Image, ImageTk
import io

class GettyImage(object):

    # u konstuktor ide self.slike[i]
    def __init__(self,result):
        self.url = self.get_src(result)
        self.image = 0
        
    def get_src(self,result):
        return str(result.find('img').__getitem__('src'))
    
    def __repr__(self):
        return self.url

    def save_photo(self):
        self.image = self.create_tk_image()

    def create_tk_image(self):
        image_url = urlopen(self.url)
        my_picture = io.BytesIO(image_url.read())
        im = Image.open(my_picture)
        width, height = im.size

        pil_img = Image.open(my_picture).resize((int(im.size[0]/2), int(im.size[1]/2)), Image.NONE)
        tk_img = ImageTk.PhotoImage(pil_img)
        pil_img.close()
        return tk_img

class Lista(list):

    def append(self,obj):
        if isinstance(obj,GettyImage):
            if not self.exist(obj):
                super(Lista,self).append(obj)

    def exist(self,obj):
        for i in self:
            if i.url == obj.url:
                return True
        return False