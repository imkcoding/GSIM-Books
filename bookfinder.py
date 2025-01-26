from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
os.system('clear')
#booksRead = input("What books that you've read do you like (seperate books by commas): ")
booksRead = "moby dick, hamlet, farrenheit 451, romeo and juliet"
booksReadList = booksRead.split(",")

linkList = []
for i in range(0, len(booksReadList)):
    linkList.append(f"https://gun.opals.pausd.org/bin/index#/recDetail?kw0={booksReadList[i]}&sf0=1016&recType=&pSize=20&pNum=1&sortAttr=0&sortOrder=0&op=search&boolop0=")

# we needs books so we dont suggest books they already read
readBooks = []
# keyterms is just authors + subjects
keyterms = []

for link in linkList:
    driver = webdriver.Safari()
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "footerLinks")))
        driverPageSource = driver.page_source
    finally:
        driver.quit()

    unfilteredSoup = BeautifulSoup(driverPageSource, features="html.parser")

    filteredTitleSoup = unfilteredSoup.find('b', {'ng-bind-html': "rec['titleFull']|oplHilightWords:hiliWords"}).get_text()
    readBooks.append(filteredTitleSoup)
    
    filteredAuthorSoup = unfilteredSoup.find('div', {'ng-switch-when': 'author'})
    portionedAuthorSoup = filteredAuthorSoup.find("span").get_text()
    deconstructedAuthorSoup = portionedAuthorSoup.split(",")
    reconstructedAuthorSoup = f"{deconstructedAuthorSoup[-1]} {deconstructedAuthorSoup[0]}"
    keyterms.append(reconstructedAuthorSoup)

    filteredSubjectSoup = unfilteredSoup.find_all('span', {'ng-bind-html': 'v.item|oplHilightWords:hiliWords'})
    for portion in filteredSubjectSoup:
        portionedSubjectSoup = portion.get_text().rstrip('.')
        keyterms.append(portionedSubjectSoup)
    

allSuggestedBooks = []
SuggestedBookImages = {}
for keyterm in keyterms:
    link = f"https://gun.opals.pausd.org/bin/index#/search?kw0={keyterm}&sf0=1016&recType=&pSize=20&pNum=1&sortAttr=0&sortOrder=0&op=search&boolop0="
    
    driver = webdriver.Safari()
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "footerLinks")))
        driverPageSource = driver.page_source
    finally:
        driver.quit()
    
    unfilteredSoup = BeautifulSoup(driverPageSource, features="html.parser")
    filteredTitleSoup = unfilteredSoup.find_all('span', {'ng-bind-html': "rec.titleFull|oplHilightWords:hiliWords"})
    filteredImageSoup = unfilteredSoup.find_all('img', {'alt' : "Card image"})
    #print(filteredImageSoup)
    for i in range(0, len(filteredTitleSoup)):
        portionedTitleSoup = filteredTitleSoup[i]
        portionedImageSoup = str(filteredImageSoup[i])
        #print(portionedImageSoup)
        portionedTitleSoup = portionedTitleSoup.get_text()
        allSuggestedBooks.append(portionedTitleSoup)
        if "src" in portionedImageSoup:
            deconstructedImageSoup = portionedImageSoup.split('src="')
            deconstructedImageSoup = deconstructedImageSoup[-1].split('"')[0]
            SuggestedBookImages[portionedTitleSoup] = deconstructedImageSoup
    


suggestedBooks = {}
for book in allSuggestedBooks:
    if book in readBooks:
        suggestedBooks[book] = 0
        del suggestedBooks[book]
    elif book in suggestedBooks:
        suggestedBooks[book] += 1
    else:
        suggestedBooks[book] = 1

sortedSuggestedBooks = dict(sorted(suggestedBooks.items(), key=lambda item: item[1], reverse=True))

# print(booksReadList)
# print(linkList)
# print(readBooks)
# print(keyterms)
# print(allSuggestedBooks)
# print(suggestedBooks)
#print(sortedSuggestedBooks)
#print(SuggestedBookImages)
i = 0
for book in sortedSuggestedBooks:
    print(book)
    i += 1
    if i == 20:
        break
