from tkinter import *
import pyperclip
import base64
from Downloaders.GettyDownloader import GettyDownloader
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
import shelve
import tkinter.constants as constants
import re
from Slike import Slike
class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.prozori = {}
        for frejm in (GettyFrame,PicturesFrame):
            page_name = frejm.__name__
            frame = frejm(container, controller=self)
            self.prozori[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.prebaci_frejm("GettyFrame")

    def prebaci_frejm(self, page_name,urll='',br=1):
        prozor = self.prozori[page_name]
        prozor.tkraise()
        if urll != '':
            prozor.create_widgets(urll,br)

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
        self.searchEntry.insert(END,'manchester united')
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
                url = 'https://www.gettyimages.com/photos/'
                url+= self.getSearchEntry()+'?family=editorial'
                if self.getRange() != 'None':
                    url+= '&recency='+self.getRange()
                if self.getOrientation() != '':
                    url+= '&orientations=' + self.getOrientation()
                if self.getResolution() != 'None':
                    url+= '&imagesize=' + self.getResolution()
                if self.getSort() != 'None':
                    url+= '&sort='+self.getSort()
                if self.getSort() == 'None':
                    url+= '&sort=mostpopular'

                pyperclip.copy(url)
                self.controller.prebaci_frejm('PicturesFrame',pyperclip.paste(),1)


class PicturesFrame(Frame):
    allPictures = []
    counter = 0
    tr_br = 0
    url0 = ""
    # &page=tr_br&sort=
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.slike = Slike.Slike()


    def create_widgets(self,url="",br=1):
        if(PicturesFrame.counter == 0):
            self.scrollbar_setup()
            PicturesFrame.counter+=1
            # manchester united
            self.footer_setup()
        self.dodajslike(url,br)
    def idi_nazad(self):

        sablon = re.compile(r'(https:.*?)(&page=)?(\d{1,4})?(&sort=.*)')
        podaci = sablon.findall(PicturesFrame.url0)
        br = 0
        print(podaci)
        if (PicturesFrame.tr_br==1):
            urlnext = podaci[0][0] + '&page=' + str(PicturesFrame.tr_br - 1) + podaci[0][3]
            self.remove_gallery()
        else:
            br = int(podaci[0][2]) - 1
            urlnext = podaci[0][0] + podaci[0][1] + str(br) + podaci[0][3]

        for i in self.frame.winfo_children():
            i.destroy()
        self.dodajslike(urlnext,br)
    def idi_napred(self):
        sablon = re.compile(r'(https:.*?)(&page=)?(\d{1,4})?(&sort=.*)')
        podaci = sablon.findall(PicturesFrame.url0)
        br = 0
        print(podaci)
        urlnext = ""
        if (PicturesFrame.tr_br == 1):
            urlnext = podaci[0][0] + '&page='+str(PicturesFrame.tr_br+1)+ podaci[0][3]
        else:
            br = int(podaci[0][2])+1
            urlnext = podaci[0][0] + podaci[0][1] + str(br)+ podaci[0][3]
        for i in self.frame.winfo_children():
            i.destroy()
        self.dodajslike(urlnext,br)

    def scrollbar_setup(self):
        # za embed scrollbar-a moramo koristiti canvas u kome se nalazi frame
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#81cbf0")
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        # recnik = {'link0': {1: ['a', 'b']}}

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
    def remove_gallery(self):
        for i in self.frame.winfo_children():
            i.destroy()
        self.controller.prebaci_frejm('GettyFrame')
        self.controller.geometry("628x256")

    # https://www.gettyimages.com/photos/manchester united?family=editorial&recency=last30days&orientations=vertical,&imagesize=xxlarge&sort=mostpopular
    def footer_setup(self):
        self.btn_search = Button(self.controller, text='<-', font='Courier 15 bold',command=self.remove_gallery)
        self.btn_previous = Button(self.controller, text='<', font='Courier 15 bold',command=self.idi_nazad)
        self.btn_next = Button(self.controller, text='>', font='Courier 15 bold',command=self.idi_napred)
        self.btn_download = Button(self.controller, text='DOWNLOAD:', font='Courier 15 bold')

        self.btn_search.pack(side=constants.LEFT, fill="both", expand=True)
        self.btn_previous.pack(side=constants.LEFT, fill="both", expand=True)
        self.btn_next.pack(side=constants.LEFT, fill="both", expand=True)
        self.btn_download.pack(side=constants.LEFT, fill="both", expand=True)
    def dodajslike2(self,podaci):
        row = 1
        column = 0
        for i in range(len(podaci)):
            if (column == 4):
                column = 0
                row += 1
            PicturesFrame.allPictures.append(self.createTkImage(podaci[i]))
            self.lbl1 = Label(self.frame, image=PicturesFrame.allPictures[-1], borderwidth=2,
                              relief="groove")
            self.lbl1['image'] = PicturesFrame.allPictures[-1]
            self.lbl1.grid(row=row, column=column, sticky=W)
            column += 1
    def dodajslike(self,url,br):

        # Label(self,text='Ovde ce biti slike.').grid(row=0,column=0,sticky=W)
        if (url != ''):
            podaci = self.slike.provera(url)
            if (podaci == 'URL NOT FOUND'):

                # self.slike.unos()
                self.urls = GettyDownloader.getListOfPhotos(self,url)
                # self.imgs = []
                if (str(type(self.urls)) != "<class 'str'>"):
                    if (len(self.urls) > 0):
                        PicturesFrame.tr_br = br
                        PicturesFrame.url0 = url
                        # dobijena je lista
                        self.slike.unos(url,self.urls)
                        self.controller.geometry("1300x460")
                        self.dodajslike2(self.urls)


                else:
                    Label(self.frame, text='Trenutna stranica nije dostupna.').grid(row=1, column=0, sticky=W)
            else:
                PicturesFrame.tr_br = br
                PicturesFrame.url0 = url
                self.controller.geometry("1300x460")
                self.dodajslike2(podaci)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def createTkImage(self,url):
        image_url = urlopen(url)
        my_picture = io.BytesIO(image_url.read())
        im = Image.open(my_picture)
        width, height = im.size

        pil_img = Image.open(my_picture).resize((int(im.size[0]/2), int(im.size[1]/2)), Image.NONE)
        tk_img = ImageTk.PhotoImage(pil_img)
        pil_img.close()
        return tk_img
# https://www.gettyimages.com/photos/manchester united bayern?family=editorial&sort=mostpopular&recency=anydate&orientations=vertical,