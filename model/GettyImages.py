import time
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
from model.GettyImage import GettyImage

class GettyImages(list):
    to_download = True

    def append(self,obj):
        if isinstance(obj,GettyImage):
            if not self.exist(obj):
                super(GettyImages,self).append(obj)

    def exist(self,obj):
        for i in self:
            if i.url == obj.url:
                return True
        return False

    def to_dl(self):
        if self.to_download == True:
            return True
        else:
            return False

    def get_tk_image(self,url):
        return self.index()

    def reset_all(self):
        self.to_download = False



    