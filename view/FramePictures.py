from easy_tk import EasyTkObject
from easy_tk.helpers import WindowScrollbar
from tkinter import *
import tkinter.constants as constants

class FramePictures(EasyTkObject):

    all_easy_photo_keys = ["LabelTkPicture"]

    def __init__(self,root_controller,root,widget):
        super(FramePictures,self).__init__()
        self.easy.add_complete_widget(root)
        self.easy.add_complete_widget(widget)
        self.controller = root_controller

        self.window_scrollbar = WindowScrollbar(self)
        self.import_methods({"set_scrollbar":self.window_scrollbar.set_scrollbar})
        self.import_variables({"left":constants.LEFT,
                                "next_page":lambda page="+":self.switch_page(page),
                                "previous_page":lambda page="-":self.switch_page(page),
                                "download":self.download_selected,
                                "go_to_frame_search":self.go_to_frame_search})
        self.init_rc_for_image()
        self.key_counter = 1
    
    def create_widgets(self):

        self.open_file("helpers_json/scrollbar.json")
        self.reading_from_json()

        self.open_file("view/json/FramePictures.json")
        self.reading_from_json()

    def set_models(self,models):
        self.search_details = models["SearchDetails"]
        self.current_page = models["CurrentPage"]
        self.getty_pictures = models["GettyPictures"]
        self.selected_pictures = models["SelectedPictures"]

    def tkraise(self):
        if self.search_details.can_search == 3:
            self.remove_all_photos()
            self.init_rc_for_image()
            self.getty_pictures.to_download = True
            self.get("Frame0").tkraise()
            self.controller.geometry = "1280x464"
            self.controller.download_for_page()
            self.current_page.original_page_url = self.search_details.url
            self.current_page.next_page()
    
    def init_rc_for_image(self):
        self.row = 0
        self.column = -1

    def add_picture(self,tk_image):
        self.open_file("view/json/TkPicture.json")
        self.reading_from_json()
        self.set_rc(tk_image)
        self.key_counter += 1
        self.get("root").update()
        self.getty_pictures.to_download = self.current_page.to_stop_loading()

    def get_last_picture(self):
        key = "LabelTkPicture"
        if self.key_counter == 1:
            return self.get(key)
        else:
            self.all_easy_photo_keys.append(f'{key}_{self.key_counter}')
            return self.get(f'{key}_{self.key_counter}')
    
    def set_rc(self,tk_image):
        picture = self.get_last_picture()
        if self.column < 3:
            self.column += 1
        else:
            self.row+=1
            self.column = 0
        """ picture["text"] = f'{self.row} and column:{self.column}' """
        picture['image'] = tk_image.image
        picture.bind("<Button-1>",lambda e,tk_image=tk_image,widget=picture: self.select_photo(tk_image,widget))
        picture.grid(row=self.row,column=self.column)
    
    def go_to_frame_search(self):
        self.getty_pictures.reset_all()
        self.controller.switch_window("FrameSearch")
        self.remove_all_photos()
        self.init_rc_for_image()
       

    def switch_page(self,page):
        self.remove_all_photos()
        self.init_rc_for_image()
        if page == "+":
            self.search_details.url = self.current_page.next_page()
        elif page == "-":
            self.search_details.url = self.current_page.previous_page()
        self.controller.download_for_page()
        print(self.search_details.url)


    def download_selected(self):
        self.selected_pictures.download()
        self.update_dl_btn()

    def remove_all_photos(self):
        widgets = self.easy.all_widgets
        for i in widgets:
            if i in self.all_easy_photo_keys:
                widgets[i].get().grid_remove()
                widgets[i].get().destroy()
        self.all_easy_photo_keys = []
    
    def select_photo(self,tk_image,widget):
        # ovo je deselect
        if tk_image.url in self.selected_pictures.pictures:
            self.selected_pictures.add_picture(tk_image.url,widget)
        # ovo je select
        else:
            self.selected_pictures.add_picture(tk_image.url,widget)
        self.update_dl_btn()

    def update_dl_btn(self):
        self.get("ButtonDownload")["text"] = f'DOWNLOAD({len(self.selected_pictures.pictures)})'