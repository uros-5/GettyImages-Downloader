class CurrentPage(object):

    urls = []
    __page_number = 0
    original_page_url = ""
    url = ""
    
    @property
    def page_number(self):
        return self.__page_number
    
    @page_number.setter
    def page_number(self,operation):
        if operation == "+":
            self.__page_number += 1
        elif operation == "-":
            self.__page_number -= 1
        self.url = self.original_page_url
        self.url += f'&page={self.__page_number}'
        
    def reset_page_number(self):
        self.__page_number = 0

    def get_page_url(self):
        return self.url

    def next_page(self):
        self.page_number = "+"
        return self.url
    
    def previous_page(self):
        self.page_number = "-"
        return self.url

    def get_current_page(self):
        self.page_number = "="
        return self.url

    def remove_url(self,url):
        index = self.urls.index(url)
        del self.urls[index]