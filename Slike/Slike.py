import os
import shelve
class Slike(object):
    def __init__(self):

        if ('linkovi.dat.dat' not in os.listdir('ss/')):
            self.fajl = shelve.open('linkovi.dat','c')
            self.fajl.close()
    def provera(self,url,stranica):
        self.fajl = shelve.open('linkovi.dat','r')
        if(self.fajl.get(url)==None):
            self.fajl.close()
            return 'URL NOT FOUND'
        else:
            for i in self.fajl.get(url).keys():
                if (stranica==i):
                    self.fajl.close()
                    return True
            self.fajl.close()
            return 'PAGE NOT FOUND'

    def unos(self,url,stranica,brojStranica,provera='',podaci=[]):
        self.fajl = shelve.open('linkovi.dat', 'w')
        if(provera=='URL NOT FOUND'):
            self.fajl[url] = {}
            temp = self.fajl[url]
            for i in range(1,brojStranica+1):
                temp.setdefault(i,[])
            self.fajl[url] = temp
        elif(provera=='PAGE NOT FOUND'):
            # temp = self.fajl[url]
            self.fajl[url].setdefault(stranica,podaci)

        self.fajl.close()