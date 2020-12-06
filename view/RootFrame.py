from easy_tk import EasyTkObject
from model import factory_models
from view.FrameSearch import FrameSearch
from view.FramePictures import FramePictures
from controller import Downloader
from controller import ImageAdder

class Root(EasyTkObject):
    
    def __init__(self):
        super(Root,self).__init__()
        self.create_root()
        widget = self.set_container()
        root = self.get_easy_root()
        self.set_all_frames(root,widget)
    
    def set_container(self):
        self.add_just_one("view/json/frame_container.json", "FrameContainer")
        child = self.get("FrameContainer", False)
        master = self.easy.create_master(child.obj)
        self.easy.all_masters.setdefault("FrameContainer", master)
        return {"TkChild": child, "TkMaster": master, "name": "FrameContainer"}

    def get_easy_root(self):
        child = self.get("root", False)
        master = self.easy.create_master(child.get())
        return {"TkChild": child, "TkMaster": master, "name": "root"}

    def set_all_frames(self,root,widget):
        self.windows = {}
        models = factory_models()

        for window in (FrameSearch,FramePictures):
            self.page_name = window.__name__
            window = window(self,root,widget)
            self.windows[self.page_name] = window
            window.create_widgets()
            window.set_models(models)

        self.easy.widgets_on_screen()
        self.image_adder = ImageAdder(models,self.windows["FramePictures"])
        self.downloader = Downloader(models)

        self.switch_window("FrameSearch")
        self.root.resizable(False,False)

    def switch_window(self,window_name):
        self.windows[window_name].tkraise()
        self.resize_screen()
        self.root.update()
        
    def download_for_page(self):
        self.downloader.start_download_all()
        self.image_adder.start_save_all()
    
    def resize_screen(self):
        self.root.geometry(self.geometry)

    def kill_threads(self):
        self.downloader.thread_download._stop()
        self.image_adder.thread_download._stop()