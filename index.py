import selenium.webdriver as webdriver
import time
## chrome driver: https://chromedriver.chromium.org/downloads
## notice chrome version must match
driver = webdriver.Chrome()
driver.get("https://www.edr.hk/speciality/doctor/paediatrics")
urlList = []
## #for select id, .for select class
## pages = driver.find_elements_by_css_selector(".paginate_button a")
while True:
    ## the sleep time must be here, otherwise the program will fast then
    ## the website update so that the driver always find the first page
    ## fuck waste my time
    doctorLinks = driver.find_elements_by_css_selector("#doctor-table .all a")
    for doctorLink in doctorLinks:
        urlList.append(doctorLink.get_attribute("href"))
    for url in urlList:
        driver.get(url)
        h2List = driver.find_elements_by_tag_name('h2')
        pList = driver.find_elements_by_tag_name('p')
        otherInfoList = driver.find_elements_by_css_selector(".other-info p")

        chinName = driver.find_element_by_tag_name('h1').text
        engName = h2List[0].text
        chinAddress = pList[1].text
        engAddress = pList[2].text
        phone = pList[4].text
        try:
            email = otherInfoList[5].text
        except:
            pass
            email = "email not exist"

        print(chinName, engName, chinAddress, engAddress, phone, email)
        driver.back()
    time.sleep(0.5)
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