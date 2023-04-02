from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    getProf(getDriver())

def getDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.ratemyprofessors.com/search/teachers?query=*&sid=1600")
    return driver

def getProf(pDriver):
    i = 1
    while True:
        try:
            show_more_button = WebDriverWait(pDriver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[4]/div[1]/div[1]/div[4]/button"))
            )
            show_more_button.click()
            time.sleep(2)
        except:
            pass

        try:
            ratingPath = "/html/body/div[2]/div/div/div[4]/div[1]/div[1]/div[3]/a[{}]/div/div[1]/div/div[2]".format(i)
            namePath = "/html/body/div[2]/div/div/div[4]/div[1]/div[1]/div[3]/a[{}]/div/div[2]/div[1]".format(i)
            rating = WebDriverWait(pDriver, 5).until(
                EC.presence_of_element_located((By.XPATH, ratingPath))
            )
            name = WebDriverWait(pDriver, 5).until(
                EC.presence_of_element_located((By.XPATH, namePath))
            )
            ratingVal = rating.text
            nameVal = name.text
            print(ratingVal, nameVal, sep="; ")
            i += 1
        except:
            break

main()
