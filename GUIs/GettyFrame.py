from tkinter import *
import pyperclip
from Downloaders import GettyDownloader,IStockDownloader
class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.windows = {}
        for F in (GettyFrame,PicturesFrame):
            page_name = F.__name__
            frame = F(container, controller=self)
            self.windows[page_name] = frame


            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("GettyFrame")

    def show_frame(self, page_name,urll=''):
        window = self.windows[page_name]
        window.tkraise()
        if urll != '':
            window.create_widgets(urll)

class GettyFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.config(bg="#81cbf0")
        self.controller = controller
        self.grid(row=0,column=0,sticky=W)
        self.create_widgets()

    def create_widgets(self):

        """"
        search keywords
        sort by
        date range
        orientation
        imageresolution
        locations
        """
        Label(self,text='Search').grid(row=0,column=0,sticky=W)

        self.searchEntry = Entry(self,width=30)
        self.searchEntry.grid(row=0,column=1,sticky=W)

        self.sortByVar = StringVar()
        self.sortByVar.set(None)
        Label(self, text='Sort by',bg='red').grid(row=1, column=0, sticky=W)

        Radiobutton(self,text='best match',value='best',variable=self.sortByVar,command=self.getSort).grid(
            row=1,column = 1,sticky=W
        )
        Radiobutton(self, text='newest', value='newest', variable=self.sortByVar, command=self.getSort).grid(
            row=1, column=2, sticky=W
        )
        Radiobutton(self, text='oldest', value='oldest', variable=self.sortByVar, command=self.getSort).grid(
            row=1, column=3, sticky=W
        )
        Radiobutton(self, text='most popular', value='mostpopular', variable=self.sortByVar, command=self.getSort).grid(
            row=1, column=4, sticky=W
        )



        Label(self, text='Date range').grid(row=2, column=0, sticky=W)

        self.rangeVar = StringVar()
        self.rangeVar.set(None)

        Radiobutton(self, text='Any date', value='anydate', variable=self.rangeVar, command=self.getRange).grid(
            row=2, column=1, sticky=W
        )
        Radiobutton(self, text='last 24 hours', value='last24hours', variable=self.rangeVar, command=self.getRange).grid(
            row=2, column=2, sticky=W
        )
        Radiobutton(self, text='last 48 hours', value='last48hours', variable=self.rangeVar, command=self.getRange).grid(
            row=2, column=3, sticky=W
        )
        Radiobutton(self, text='last 72 hours', value='last72hours', variable=self.rangeVar, command=self.getRange).grid(
            row=2, column=4, sticky=W
        )
        Radiobutton(self, text='last 7 days', value='last7days', variable=self.rangeVar, command=self.getRange).grid(
            row=3, column=1, sticky=W
        )
        Radiobutton(self, text='last 30 days', value='last30days', variable=self.rangeVar, command=self.getRange).grid(
            row=3, column=2, sticky=W
        )
        Radiobutton(self, text='last 12 months', value='last12months', variable=self.rangeVar, command=self.getRange).grid(
            row=3, column=3, sticky=W
        )

        Label(self, text='Orientation').grid(row=4, column=0, sticky=W)

        self.orVertical = BooleanVar()
        self.orHorizontal = BooleanVar()
        self.orSquare = BooleanVar()
        self.orPanoramicHorizontal = BooleanVar()
        Checkbutton(self,
                    text="vertical",
                    variable= self.orVertical,
                    command=self.getOrientation
                    ).grid(row=4, column=1, sticky=W)
        Checkbutton(self,
                    text="horizontal",
                    variable=self.orHorizontal,
                    command=self.getOrientation
                    ).grid(row=4, column=2, sticky=W)
        Checkbutton(self,
                    text="square",
                    variable=self.orSquare,
                    command=self.getOrientation
                    ).grid(row=5, column=1, sticky=W)

        self.imgRes = StringVar()
        self.imgRes.set(None)
        Label(self, text='Image resolution').grid(row=6, column=0, sticky=W)

        Radiobutton(self, text='All', value=' ', variable=self.imgRes,
                    command=self.getResolution).grid(
            row=7, column=0, sticky=W
        )

        Radiobutton(self, text='12 MP and larger', value='xlarge', variable=self.imgRes, command=self.getResolution).grid(
            row=7, column=1, sticky=W
        )
        Radiobutton(self, text='16 MP and larger', value='xxlarge', variable=self.imgRes,
                    command=self.getResolution).grid(
            row=7, column=2, sticky=W
        )
        Radiobutton(self, text='21 MP and larger', value='xxxlarge', variable=self.imgRes,
                    command=self.getResolution).grid(
            row=7, column=3, sticky=W
        )
        Button(self,text='SEARCH',command=self.searchPictures).grid(row=8,column=0,sticky=W)
        for i in GettyFrame.winfo_children(self):
            if(str(i) =='.!frame.!gettyframe.!entry'):
                i.config(bg="#c8e9fa")
            else:
                i.config(bg="#81cbf0")
    def getSearchEntry(self):
        return self.searchEntry.get()
    def getSort(self):
        return self.sortByVar.get()
    def getRange(self):
        return self.rangeVar.get()
    def getOrientation(self):
        orientation = ""
        if self.orVertical.get():
            orientation += 'vertical'+','
        if self.orHorizontal.get():
            orientation+= 'horizontal'+','
        if self.orSquare.get():
            orientation+= 'square'+','
        if self.orPanoramicHorizontal.get():
            orientation+= 'panaromicHorizontal'
        return orientation
    def getResolution(self):
        return self.imgRes.get()
    def searchPictures(self):
        if not self.getSearchEntry().isspace():
            if self.getSearchEntry() != '':
                print('ukucano je')
                url = 'https://www.gettyimages.com/photos/'
                url+= self.getSearchEntry()+'?family=editorial'
                if self.getSort() != 'None':
                    url+= '&sort='+self.getSort()
                if self.getRange() != 'None':
                    url+= '&recency='+self.getRange()
                if self.getOrientation() != '':
                    url+= '&orientations=' + self.getOrientation()
                if self.getResolution() != 'None':
                    url+= '&imagesize=' + self.getResolution()
                pyperclip.copy(url)
                self.controller.show_frame('PicturesFrame',pyperclip.paste())


class PicturesFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.grid()
        # self.create_widgets()
    def create_widgets(self,url=""):
        print('hejjjj')
        scrollbar = Scrollbar(self, width=50)
        scrollbar.pack(side=RIGHT, fill=Y, expand=False)

        self.canvas = Canvas(self, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        row=0
        column=0
        # Label(self,text='Ovde ce biti slike.').grid(row=0,column=0,sticky=W)
        if (url!=''):
            linkovi = GettyDownloader.getListOfPhotos(url)
            if (str(type(linkovi))!="<class 'str'>"):
                if (len(linkovi)>0):
                    for i in range(len(linkovi)):
                        if (column==4):
                            column=0
                            row+=1
                        Label(self, text='SLIKA'+str(i)).grid(row=row, column=column, sticky=W)
                        column+=1


            else:
                Label(self, text='Ovde nece biti slike.').grid(row=1, column=0, sticky=W)



