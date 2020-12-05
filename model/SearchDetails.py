class SearchDetails(object):
    

    def __init__(self):
        self.init_variables()
        
    
    def init_variables(self):
        self.can_search = 0
        self.entry = ""
        self.datum_range = "None"
        self.is_vertical = False
        self.is_horizontal = False
        self.is_square = False
        self.orientation = ""
        self.resolution = ""
        self.sort = ""
        self.url = ""


    def set_url(self):
        self.url = "https://www.gettyimages.com/photos/"
        self.url += self.entry + "?family=editorial"
        if self.datum_range != 'None':
            self.url += '&recency='+self.datum_range + self.getOrientation()
        if self.resolution != 'None':
            self.url += '&imagesize=' + self.resolution
        if self.sort != 'None':
            self.url += '&sort='+self.sort
        if self.sort == 'None':
            self.url += '&sort=mostpopular'
        self.can_search += 1
        print(self.url)
    
    def getOrientation(self):
        orientation = ""
        if self.is_vertical:
            orientation += 'vertical'+','
        if self.is_horizontal:
            orientation+= 'horizontal'+','
        if self.is_square:
            orientation+= 'square'+','
        return orientation

    def is_entry_space(self):
        if not self.entry.isspace():
            self.can_search += 1
    
    def is_entry_not_blank(self):
        if self.entry != "":
            self.can_search += 1
    
    def search(self):
        self.can_search = 0
        for i in [self.is_entry_space,self.is_entry_not_blank,self.set_url]:
            previous_counter = self.can_search
            i()
            if self.can_search <= previous_counter:
                print(self.can_search)
                break