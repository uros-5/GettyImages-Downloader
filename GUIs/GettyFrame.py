from tkinter import *
import pyperclip
from Downloaders.GettyDownloader import GettyDownloader
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
import tkinter.constants as constants
import re
from Slike import Slike
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import messagebox
import threading
from tkinter.ttk import Progressbar
class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.prozori = {}
        for frejm in (GettyFrame,PicturesFrame,BlankFrame):
            page_name = frejm.__name__
            frame = frejm(container, controller=self)
            self.prozori[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.resizable(False, False)
        self.pretraga = False
        self.downloadProgress = 0
        self.prebaci_frejm("GettyFrame")
        self.geometry("746x256")

    def prebaci_frejm(self, page_name,urll='',br=1):
        prozor = self.prozori[page_name]
        # self.update()
        if urll != '':

            self.t1_set()
            self.t1_start()

            self.t2_set(urll,br)
            self.t2_start()
            # t2.setDaemon(True)
            # glavni threadovi
            # prozor.create_widgets(urll,br)
        else:
            prozor.tkraise()

    def t1_set(self):
        self.geometry("746x256")
        self.update()
        prozor2 = self.prozori["BlankFrame"]
        prozor2.tkraise()
        prozor2.update()
        self.update()
        self.t1 = threading.Thread(target=prozor2.run_progressbar)
        
    def t1_get(self):
        return self.t1.is_alive()
    def t1_start(self):
        self.t1.start()

    def t2_set(self,urll,br,dodajslike = False):
        prozor = self.prozori["PicturesFrame"]
        prozor.update()
        if(dodajslike==False):
            self.t2 = threading.Thread(target=lambda var=urll, var2=br: prozor.create_widgets(var, var2))
        else:
            self.t2 = threading.Thread(target=lambda var=urll, var2=br: prozor.dodajslike(var, var2))
    def t2_get(self):
        return self.t2.is_alive()
    def t2_start(self):
        self.t2.start()


class BlankFrame(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller
        self.grid()
        self.lbl0 = Label(self, text="Pretraga..",font=("Courier", 44))
        self.lbl0.pack()
        self.progress_bar = Progressbar(self,orient="horizontal",length=286,mode="determinate")
        self.progress_bar.pack()
    def create_widgets(self):
        self.lbl0.pack()

    def run_progressbar(self):
        self.progress_bar["maximum"] = 100

        br = 0
        while (br < 101):
            self.update()
            br2 = self.controller.downloadProgress
            self.progress_bar.update()
            if (br != br2):
                # print(br2)
                br = br2
                time.sleep(0.05)
                self.progress_bar["value"] = br2
                self.progress_bar.update()
                self.update()
                if (br == 100):
                    self.stop_progressbar()
                    self.progress_bar["value"] = 0
                    self.controller.update()
                    self.controller.prebaci_frejm("PicturesFrame")
                    self.controller.update()
                    self.controller.downloadProgress = 0
                    break

    def stop_progressbar(self):
        self.progress_bar.stop()



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
        Label(self,text='Search',font=("Courier", 14)).grid(row=0,column=0,sticky=W)

        self.searchEntry = Entry(self,width=30)
        self.searchEntry.insert(END,'')
        self.searchEntry.grid(row=0,column=1,sticky=W)

        self.sortByVar = StringVar()
        self.sortByVar.set(None)
        Label(self, text='Sort by',bg='red',font=("Courier", 14)).grid(row=1, column=0, sticky=W)

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



        Label(self, text='Date range',font=("Courier", 14)).grid(row=2, column=0, sticky=W)

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

        Label(self, text='Orientation',font=("Courier", 14)).grid(row=4, column=0, sticky=W)

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
        Label(self, text='Image resolution',font=("Courier", 14)).grid(row=6, column=0, sticky=W)

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
        Button(self,text='SEARCH',font=("", 10),command=self.searchPictures).grid(row=8,column=0,sticky=W)
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
                self.controller.pretraga = True
                self.controller.prebaci_frejm('PicturesFrame',pyperclip.paste(),1)
                # self.controller.geometry("1300x460")
                time.sleep(0.5)
                

class PicturesFrame(Frame):
    allPictures = []
    counter = 0
    tr_br = 0
    url0 = ""
    za_download0 = []
    sablon = re.compile(r'(https:.*?)(&page=)?(\d{1,4})?(&sort=.*)')
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
        self.controller.downloadProgress = 20

        self.dodajslike(url,br)
    def scrollbar_setup(self):
        # za embed scrollbar-a moramo koristiti canvas u kome se nalazi frame
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#81cbf0")
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        # recnik = {'link0': ['slika1', 'slika2']}}

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)


    def footer_setup(self):
        self.btn_search = Button(self.controller, text='<-', font='Courier 15 bold',command=self.remove_gallery)
        self.btn_previous = Button(self.controller, text='<', font='Courier 15 bold',command=self.idi_nazad)
        self.btn_next = Button(self.controller, text='>', font='Courier 15 bold',command=self.idi_napred)
        self.btn_download = Button(self.controller, text='DOWNLOAD(0)', font='Courier 15 bold',
                                   command=self.download_zip)

        self.btn_search.pack(side=constants.LEFT, fill="both", expand=True)
        self.btn_previous.pack(side=constants.LEFT, fill="both", expand=True)
        self.btn_next.pack(side=constants.LEFT, fill="both", expand=True)
        self.btn_download.pack(side=constants.LEFT, fill="both", expand=True)


    def dodajslike(self,url,br):
        

        # Label(self,text='Ovde ce biti slike.').grid(row=0,column=0,sticky=W)
        if (url != ''):
            podaci = self.slike.provera(url)

            if (podaci == 'URL NOT FOUND'):
                self.controller.downloadProgress = 35
                # self.slike.unos()
                self.urls = GettyDownloader.getListOfPhotos(self,url)
                # self.imgs = []
                if (str(type(self.urls)) != "<class 'str'>"):
                    if (len(self.urls) > 0):
                        PicturesFrame.tr_br = br
                        PicturesFrame.url0 = url
                        # dobijena je lista
                        self.slike.unos(url,self.urls)

                        self.controller.downloadProgress = 40
                        self.dodajslike2(self.urls)

                    elif (len(self.urls) == 0):
                        self.controller.downloadProgress = 100
                        messagebox.showinfo('Greska','Trazena stranica ne postoji.')
                        self.controller.prebaci_frejm("GettyFrame")
                        self.controller.geometry("746x256")
                        self.update()


                else:
                    self.controller.downloadProgress = 100
                    messagebox.showinfo('Greska', 'Trazena stranica ne postoji.')
                    self.controller.prebaci_frejm("GettyFrame")
                    self.controller.geometry("746x256")
                    self.update()
            else:
                PicturesFrame.tr_br = br
                PicturesFrame.url0 = url
                for i in self.frame.winfo_children():
                    i.destroy()
                self.controller.downloadProgress = 40

                self.dodajslike2(podaci)

    def dodajslike2(self,podaci):
        row = 1
        column = 0
        PicturesFrame.allPictures = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            self.controller.downloadProgress = 60

            for i in range(len(podaci)):
                if (column == 4):
                    column = 0
                    row += 1
                PicturesFrame.allPictures.append(self.createTkImage(podaci[i]))
                self.lbl1 = Label(self.frame, image=PicturesFrame.allPictures[-1], borderwidth=2,
                                  relief="groove")
                self.lbl1['image'] = PicturesFrame.allPictures[-1]
                self.lbl1.lokacija = podaci[i]
                self.lbl1.selectedd = False
                self.lbl1.bind("<Button-1>", lambda e, var=self.lbl1: self.za_download(var))
                self.lbl1.grid(row=row, column=column, sticky=W)
                column += 1
                self.controller.downloadProgress = self.controller.downloadProgress + 0.5
            self.controller.geometry("1300x460")
            self.controller.downloadProgress = 100


    def idi_napred(self):
        
        podaci = PicturesFrame.sablon.findall(PicturesFrame.url0)
        br = 0
        urlnext = ""
        if (PicturesFrame.tr_br == 1):
            urlnext = podaci[0][0] + '&page='+str(PicturesFrame.tr_br+1)+ podaci[0][3]
        else:
            br = int(podaci[0][2])+1
            urlnext = podaci[0][0] + podaci[0][1] + str(br)+ podaci[0][3]
        for i in self.frame.winfo_children():
            i.destroy()
        

        self.controller.prebaci_frejm("PicturesFrame",urlnext,br)
        self.controller.geometry("746x256")
        self.controller.update()
        #
        # self.controller.t1_set()
        # self.controller.t1_start()
        # self.update()

        # self.controller.t2_set(urlnext,br,False)
        # self.controller.t2_start()

        # self.dodajslike(urlnext,br)

    def idi_nazad(self):
        podaci = PicturesFrame.sablon.findall(PicturesFrame.url0)
        br = 0
        if (PicturesFrame.tr_br==1):
            urlnext = podaci[0][0] + '&page=' + str(PicturesFrame.tr_br - 1) + podaci[0][3]
            self.remove_gallery()
        else:
            br = int(podaci[0][2]) - 1
            urlnext = podaci[0][0] + podaci[0][1] + str(br) + podaci[0][3]
            # self.dodajslike(urlnext, br)
            for i in self.frame.winfo_children():
                i.destroy()
            self.controller.prebaci_frejm("PicturesFrame", urlnext, br)
            self.controller.geometry("746x256")
            self.controller.update()
            # self.dodajslike(urlnext, br)

    def remove_gallery(self):
        for i in self.frame.winfo_children():
            i.destroy()
        self.controller.prebaci_frejm('GettyFrame')
        self.controller.geometry("746x256")

    def download_zip(self,):
        if(len(PicturesFrame.za_download0)>0):
            GettyDownloader.download_zip(self,PicturesFrame.za_download0)

            for i in self.frame.winfo_children():
                i.selectedd = False
                i['borderwidth'] = 2
                i['relief'] = 'groove'
            PicturesFrame.za_download0 = []
            self.btn_download['text'] = 'DOWNLOAD(0)'
            messagebox.showinfo('Poruka', 'Slike su uspesno preuzete.')
    # https://www.gettyimages.com/photos/manchester united?family=editorial&recency=last30days&orientations=vertical,&imagesize=xxlarge&sort=mostpopular

    def za_download(self,label1):
        # PicturesFrame.za_download0
        if (label1.selectedd == False):
            label1.selectedd = True
            PicturesFrame.za_download0.append(label1.lokacija)
            label1['borderwidth'] = 4
            label1['relief'] = 'solid'
        elif (label1.selectedd == True):
            label1.selectedd = False
            PicturesFrame.za_download0.remove(label1.lokacija)
            label1['borderwidth'] = 2
            label1['relief'] = 'groove'
        self.btn_download['text'] = 'DOWNLOAD('+str(len(PicturesFrame.za_download0))+')'

    def _on_mousewheel(self,event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def createTkImage(self,url):
        #najbitnija metoda
        image_url = urlopen(url)
        my_picture = io.BytesIO(image_url.read())
        im = Image.open(my_picture)
        width, height = im.size

        pil_img = Image.open(my_picture).resize((int(im.size[0]/2), int(im.size[1]/2)), Image.NONE)
        tk_img = ImageTk.PhotoImage(pil_img)
        pil_img.close()
        return tk_img
