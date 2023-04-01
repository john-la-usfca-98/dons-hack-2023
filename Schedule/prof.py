from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    rating = WebDriverWait(pDriver, 5).until(
        EC.presence_of_element_located(By.XPATH, "")
    )