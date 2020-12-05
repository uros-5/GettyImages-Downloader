import threading
import time
class ImageAdder(object):
    def __init__(self,models,easy):
        self.getty_pictures = models["GettyPictures"]
        self.current_page = models["CurrentPage"]
        self.easy = easy

    def init_cols_and_rows(self):
        self.row = 0
        self.column = 0
    
    def start_save_all(self):
        self.thread_download = threading.Thread(target=self.__all)
        self.thread_download.start()

    def __all(self):
        urls = {}
        while self.getty_pictures.to_dl() and self.getty_pictures.not_saved():
            urls = self.getty_pictures.photo_urls
            try:
                for url in urls:
                    if urls[url] == 0:
                        self.getty_pictures.save_photo(url)
                        self.easy.add_picture(url)
                        self.current_page.remove_url(url)
                    if not self.getty_pictures.to_dl():
                        break
                    else:
                        if url in self.current_page.urls:
                            self.easy.add_picture(url)
                            self.current_page.remove_url(url)

            except Exception as e:
                continue

        self.getty_pictures.reset_all()
        self.current_page.urls = []