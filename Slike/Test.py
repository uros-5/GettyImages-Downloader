import dill
import os
import shelve
from concurrent.futures import ThreadPoolExecutor, as_completed
def kreiraj():
    if('linkovi.dill' not in os.listdir('.')):
        fajl = open('linkovi.dill','wb')
        dill_fajl = dill.dump({},fajl)
        fajl.close()


def provera( url, stranica):
    fajl = shelve.open('Slike/linkovi.dat', 'rb')
    if (fajl.get(url) == None):
        fajl.close()
        return 'URL NOT FOUND'
    else:
        for i in fajl.get(url).keys():
            if (stranica == i):
                fajl.close()
                # treba dalje nastaviti pretragu da se vide da li su tu podaci
                return 'OK'
        fajl.close()
        return 'NUMBER NOT FOUND'


kreiraj()
