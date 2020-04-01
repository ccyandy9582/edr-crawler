import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
import time
import ExportToExcel as ExportToExcel
import re
import os.path

ExportToExcel.isFileExist()
## chrome driver: https://chromedriver.chromium.org/downloads
## notice chrome version must match
driver = webdriver.Chrome()
driver.get("https://www.edr.hk/speciality/doctor/paediatrics")
urlList = []
doctorList = []

def findEmail(list):
    email = 'email not found'
    for i in list:
        if re.match(r"([A-Z0-9a-z]+@[A-Z0-9a-z]+\.[A-Za-z]{2,})", i.text):
            email = i.text
    return email

def findPhone(list):
    phone = 'not found'
    for i in list:
        if re.match(r"(^[0-9]{8})", i.text):
            phone = i.text
            break
    return phone
## #for select id, .for select class
## pages = driver.find_elements_by_css_selector(".paginate_button a")
while True:
    ## the sleep time must be here, otherwise the program will fast then
    ## the website update so that the driver always find the first page
    ## fuck waste my time
    doctorLinks = driver.find_elements_by_css_selector("#doctor-table .all a")
    urlList.clear()
    for doctorLink in doctorLinks:
        urlList.append(doctorLink.get_attribute("href"))
    for url in urlList:
        # driver.back() is back to the page that is you first time used in driver.get()
        # so i use new tab to solve it
        # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        driver.execute_script('''window.open("");''')
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.1)
        driver.get(url)
        h2List = driver.find_elements_by_tag_name('h2')
        pList = driver.find_elements_by_tag_name('p')
        otherInfoList = driver.find_elements_by_css_selector(".other-info p")

        chinName = driver.find_element_by_tag_name('h1').text
        engName = h2List[0].text
        chinAddress = pList[1].text
        engAddress = pList[2].text
        phone = findPhone(pList)
        email = findEmail(pList)
        
        doctorList.append([chinName, engName, chinAddress, engAddress, phone, email])
        # print(chinName, engName, chinAddress, engAddress, phone, email)
        # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 
        # driver.back()
        driver.execute_script('''window.close("");''')
        driver.switch_to.window(driver.window_handles[0])
        # driver.execute_script("window.history.go(-1)")
        time.sleep(0.1)
    try:
        a = driver.find_element_by_css_selector(".pagination li[class='paginate_button next']")
        # print(a.get_attribute('class'))
        nextPageBtn = driver.find_element_by_xpath("//a[contains(text(),'>')]")
        nextPageBtn.click()
        time.sleep(0.5)
    except:
        print("There is last page")
        break
driver.close()

ExportToExcel.writeToExcel(ExportToExcel.insert(doctorList))