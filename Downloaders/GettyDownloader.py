from selenium import webdriver

driver = webdriver.Firefox()

def getListOfPhotos(url):
    driver.get(url)
    while(True):
        try:
            slike = driver.find_elements_by_xpath("//figure[contains(@class,'gallery-mosaic')]//img")
            if (len(slike)==0):
                notAvailable = driver.find_elements_by_xpath("//h4[contains(@class,'gallery-no')]")
                if (len(notAvailable)>0):
                    print('to je to.')
                    return 'NO'
                else:
                    continue
            elif(len(slike)>0):
                slike2 = []
                for i in slike:
                    slike2.append(i.get_attribute('src'))
                return slike2

            break
        except:
            continue
