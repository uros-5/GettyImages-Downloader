import os
import shelve
from concurrent.futures import ThreadPoolExecutor, as_completed
class Slike(object):
    def __init__(self):
        if ('linkovi.dat.dat' not in os.listdir('Slike/')):
            self.fajl = shelve.open('Slike/linkovi.dat','c')
            self.fajl.close()
    def provera(self,url,stranica):
        self.fajl = shelve.open('Slike/linkovi.dat','r')
        if(self.fajl.get(url)==None):
            self.fajl.close()
            return 'URL NOT FOUND'
        else:
            for i in self.fajl.get(url).keys():
                if (stranica==i):
                    if(len(self.fajl.get(url)[stranica])==0):
                        #treba dalje nastaviti pretragu da se vide da li su tu podaci
                        self.fajl.close()
                        return 'OK BUT 0'
                    else:
                        return 'OK'
            self.fajl.close()
            return 'NUMBER NOT FOUND'

    def unos(self,url,stranica,provera='',podaci=[]):
        self.fajl = shelve.open('Slike/linkovi.dat', 'w')
        if(provera=='URL NOT FOUND'):
            self.fajl[url] = {}
            temp = self.fajl[url]
            temp.setdefault(stranica,[])
            with ThreadPoolExecutor(max_workers=10) as executor:
                for i in podaci:
                    temp[stranica].append(i)
            self.fajl[url] = temp
            self.fajl.close()
        elif(provera=='NUMBER NOT FOUND'):
            # temp = self.fajl[url]
            self.fajl[url].setdefault(stranica,podaci)

        self.fajl.close()
        # nesto.unos(url,1,self.tkimgs[-1],provera,self.tkimgs[0:-1])