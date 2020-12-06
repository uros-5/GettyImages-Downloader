import threading
import time
class ImageAdder(object):
    def __init__(self,models,easy):
        self.getty_images = models["GettyPictures"]
        self.current_page = models["CurrentPage"]
        self.easy = easy

    def init_cols_and_rows(self):
        self.row = 0
        self.column = 0
    
    def start_save_all(self):
        self.thread_download = threading.Thread(target=self.__all)
        self.thread_download.start()

    def __all(self):
        images = {}
        while self.getty_images.to_dl():
            images = self.getty_images
            try:
                for tk_image in images:
                    if tk_image.image == 0:
                        tk_image.save_photo()
                        self.easy.add_picture(tk_image)
                        self.current_page.remove_url(tk_image.url)
                    else:
                        if tk_image.url in self.current_page.urls:
                            self.easy.add_picture(tk_image)
                            self.current_page.remove_url(tk_image.url)
            except Exception as e:
                continue
        self.getty_images.to_download = True
        self.current_page.urls = []