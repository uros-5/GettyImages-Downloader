from easy_tk import EasyTkObject
from tkinter import StringVar,BooleanVar,Checkbutton,END

class FrameSearch(EasyTkObject):
    

    def __init__(self,root_controller,root,widget):
        super(FrameSearch,self).__init__()
        self.easy.add_complete_widget(root)
        self.easy.add_complete_widget(widget)
        self.controller = root_controller
        self.init_variables_and_methods()
        
        self.import_variables(
            {"sort_by_var":self.sort_by_var,"sort_by_range":self.sort_by_range,
            "or_vertical":self.or_vertical,"or_horizontal":self.or_horizontal,
            "or_square":self.or_square,"img_res":self.img_res,"search_btn":self.search_btn})
        self.import_modules([Checkbutton,])

    def init_variables_and_methods(self):
        self.sort_by_var = StringVar()
        self.sort_by_var.set(None)

        self.sort_by_range = StringVar()
        self.sort_by_range.set(None)

        self.or_vertical = BooleanVar()
        self.or_horizontal = BooleanVar()
        self.or_square = BooleanVar()
        self.orPanoramicHorizontal = BooleanVar()

        self.img_res = StringVar()
        self.img_res.set(None)

    def create_widgets(self):
        self.open_file("view/json/FrameSearch.json")
        self.reading_from_json()
        self.get("EntrySearch").insert(END,'manchester united')
    
    def tkraise(self):
        """ print(self.get("FrameSearch")) """
        self.controller.geometry = "1280x250"
        self.get("FrameSearch").tkraise()  
    
    def set_models(self,models):
        self.search_details = models["SearchDetails"]
        self.current_page = models["CurrentPage"]
        self.getty_pictures = models["GettyPictures"]
        self.selected_pictures = models["SelectedPictures"]
    
    def search_btn(self):
        self.search_details.entry = self.get("EntrySearch").get()
        self.search_details.sort = self.sort_by_var.get()
        self.search_details.datum_range = self.sort_by_range.get()
        self.search_details.is_vertical = self.or_vertical.get()
        self.search_details.is_horizontal = self.or_horizontal.get()
        self.search_details.is_square = self.or_square.get()
        self.search_details.resolution = self.img_res.get()
        self.search_details.search()
        self.controller.switch_window("FramePictures")

    def reset_search(self):
        self.getty_pictures.reset_all()
        self.current_page.original_page_url = ""
        self.current_page.reset_page_number()