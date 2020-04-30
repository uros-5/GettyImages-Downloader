# Projekat1 za predmet namenski racunarski sistemi
Klikom na `main.py` se pokrece aplikacija.
U glavni fajl uvozimo **tkinter** biblioteku sa svim klasama:
```python
from tkinter import *
import tkinter.constants as constants
```
Kao i klase  iz naseg package-a **GUIs** > modul  GettyFrame:
```python
from GUIs.GettyFrame import Root,GettyFrame,PicturesFrame
```
Zatim koristimo *Root* klasu koja ce drzati sve druge klase(tj. widgete kojima je roditelj klasa *Root*):
```python
root = Root()
```
Nakon podesavanja glavne klase,pozivamo metodu:
```python
root.mainloop()
```
i program prelazi u stanje u kome ceka korisnikove akcije.

---
**GettyFrame**.py sadrzi te tri klase koje ce se najvise koristiti.
Uvozimo sve biblioteke koje nam trebaju za rad aplikacije:
```python
from tkinter import *
import pyperclip
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
import tkinter.constants as constants
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import messagebox
import threading
from tkinter.ttk import Progressbar
import os
```
Kao i nase dve klase iz package-a Downloaders.GettyDownloader i Slike:
```python
from Downloaders.GettyDownloader import GettyDownloader
from Slike import Slike
```
Klasa *Root*:
Posto je to glavni ekran ova klasa mora da nasledjuje *Tk* iz tkinter biblioteke.
```python
class Root(Tk):
```
Zatim override-ujemo konstruktor te klase,gde koristimo i pack za layout:
```python
def __init__(self, *args, **kwargs):
    Tk.__init__(self, *args, **kwargs)
    container = Frame(self)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
```
Zatim kreiramo sve prozore(objekte) i dodajemo ih u recnik:
```python
self.prozori = {}
for frejm in (GettyFrame,PicturesFrame,BlankFrame):
    page_name = frejm.__name__
    frame = frejm(container, controller=self)
    self.prozori[page_name] = frame
    frame.grid(row=0, column=0, sticky="nsew")
```
Za prvi ekran koji ce biti vidljiv korisniku postavaljamo *GettyFrame* gde ce korisnik unositi podatke o slikama koje mu trebaju:
```python
self.resizable(False, False)
self.prebaci_frejm("GettyFrame")
self.geometry("746x256")
```
Promenljiva downloadProgress se koristi za vreme preuzimanja slika
```python
self.downloadProgress = 0
```
Metoda prebaci_frejm prima parametre:
- page_name - za Frame koji na koji ce da se prebaci
- urll - link koji bi trebalo da sadrzi stranicu sa svim slikama
- br - broj stranice za pretragu
```python
def prebaci_frejm(self, page_name,urll='',br=1):
        prozor = self.prozori[page_name]
```
Kako program ne bi freeze-ovao koristimo dva Thread-a:
```python
if urll != '':
    self.t1_set()
    self.t1_start()

    self.t2_set(urll,br)
    self.t2_start()
else:
   prozor.tkraise()
```
Prvi ce biti vidljiv korisniku i on sadrzi progress bar.
```python
def t1_set(self):
    self.geometry("746x256")
    self.update()
    prozor2 = self.prozori["BlankFrame"]
    prozor2.tkraise()
    prozor2.update()
    self.update()
    self.t1 = threading.Thread(target=prozor2.run_progressbar)
```
*BlankFrame* nakon pokretanja Thread-a,metoda je aktivna sve dok downloadProgress ne bude 100:
```python
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
```
U medjuvremenu drugi Thread preuzima slike i sa grid layout(umesto pack) ih postavlja na ekran.
```python
self.t2_set(urll,br)
self.t2_start()
```
```python
def t2_set(self,urll,br,dodajslike = False):
    prozor = self.prozori["PicturesFrame"]
    prozor.update()
```

---

## 1.
 U target stavljamo link i broj stranice
```python
self.t2 = threading.Thread(target=lambda var=urll, var2=br: prozor.dodajslike(var, var2))
```
U *GettyFrame* samo jednom postavljamo scrollbar gde ce biti smestene slike i footer sa opcijama:
```python
def create_widgets(self,url="",br=1):
    if(PicturesFrame.counter == 0):
        self.scrollbar_setup()
        PicturesFrame.counter+=1
        # manchester united
        self.footer_setup()
    self.controller.downloadProgress = 20
```
## 2.
Dodajemo slike (tj.dobijamo linkove):
```python
self.dodajslike(url,br)
```
Proveravamo da li se link vec nalazi u shelve fajl da ne bi preuzimali opet:
```python
podaci = self.slike.provera(url)
```
```python
if (podaci == 'URL NOT FOUND'):
    self.controller.downloadProgress = 35
    # preuzimanje slika
    self.urls = GettyDownloader.getListOfPhotos(self,url)
    # ukoliko je vracena lista
    if (str(type(self.urls)) != "<class 'str'>"):
        if (len(self.urls) > 0):
            # br stranice koja se trazi
            PicturesFrame.tr_br = br
            # frame mora sadrzati link da bi lakse odlazio na prethodne ili sledece stranice
            PicturesFrame.url0 = url
            # dobijena je lista 
            # ta lista sa slikama se unosi u shelve fajl
            self.slike.unos(url,self.urls)

            self.controller.downloadProgress = 40
            # drugi deo dodavanja slika na ekran
            self.dodajslike2(self.urls)

        elif (len(self.urls) == 0):
            # ako je vracena lista bez linkova znaci da ta stranica ne postoji
            # iako u bs4 postoji div sa takvim atributima,ukoliko su prazni onda nema
            # ni linka sa slikama
            self.controller.downloadProgress = 100
            messagebox.showinfo('Greska','Trazena stranica ne postoji.')
            self.controller.prebaci_frejm("GettyFrame")
            self.controller.geometry("746x256")
            self.update()
    else:
        # kada je vracen string to znaci da takva pretraga ima pogresne parametre
        self.controller.downloadProgress = 100
        messagebox.showinfo('Greska', 'Trazena stranica ne postoji.')
        self.controller.prebaci_frejm("GettyFrame")
        self.controller.geometry("746x256")
        self.update()
else:
    # ukoliko link postoji u shelve fajlu onda se prelazi na dodavanje na ekran
    PicturesFrame.tr_br = br
    PicturesFrame.url0 = url
    for i in self.frame.winfo_children():
        # uklanjanje prethodnih widgeta sa slikama
        i.destroy()
    self.controller.downloadProgress = 40

    self.dodajslike2(podaci)
    self.update()
```
## 3.
Dodajemo slike na ekran(to je i dalje drugi Thread)
```python
self.dodajslike2(podaci)
```
```python
def dodajslike2(self,podaci):
    ...
```
Koristimo jos vise Thread-ova da bi brze dodali slike na ekran.
```python
with ThreadPoolExecutor(max_workers=5) as executor:
    self.controller.downloadProgress = 60
```

```python
    ...
    #cuvano reference svake slike(PIL Images)
    PicturesFrame.allPictures.append(self.createTkImage(podaci[i]))
    ...
    #svaka slika se moze selektovati
    self.lbl1.bind("<Button-1>", lambda e, var=self.lbl1: self.za_download(var))
    self.lbl1.grid(row=row, column=column, sticky=W)
    column += 1
self.controller.geometry("1300x460")
self.controller.downloadProgress = 100
```