import os
import shelve
from concurrent.futures import ThreadPoolExecutor, as_completed
class Slike(object):
    def __init__(self):
        if ('linkovi.dat.dat' not in os.listdir('Slike/')):
            self.fajl = shelve.open('Slike/linkovi.dat','c')
            self.fajl.close()
    def provera(self,url):
        self.fajl = shelve.open('Slike/linkovi.dat','r')
        if(self.fajl.get(url)==None):
            self.fajl.close()
            return 'URL NOT FOUND'
        else:
            lista = []
            for i in self.fajl.get(url):
                lista.append(i)
            self.fajl.close()
            return lista

    def unos(self,url,podaci=[]):
        self.fajl = shelve.open('Slike/linkovi.dat', 'w')
        self.fajl[url] = []
        temp = self.fajl[url]
        with ThreadPoolExecutor(max_workers=10) as executor:
            for i in podaci:
                temp.append(i)
        self.fajl[url] = temp
        self.fajl.close()
        # nesto.unos(url,1,self.tkimgs[-1],provera,self.tkimgs[0:-1])