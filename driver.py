from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

class Driver:
    
    def __init__(self):
        #settings
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--log-level=OFF")
        options.add_argument("disable-infobars")
        options.add_argument('--hide-scrollbars')
        options.add_argument('--disable-web-security')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.binary_location = "C:\Program Files\BraveSoftware\Brave-Browser\Application\\brave.exe"
        options.add_extension('Extansions/proxy.zip')
        options.add_extension('Extansions/anticaptcha-plugin_v0.56.zip')


        #driver
        self.driver = webdriver.Chrome("chromedriver.exe", options=options)
        # caution from temporary ban
        self.caution = False 
    
    def wait_for_elem(self, time, elem,by = By.CLASS_NAME):
        WebDriverWait(self.driver, time).until(EC.presence_of_element_located((by, elem)))

    def wait_for_elems(self, time, elems, by = By.CLASS_NAME):
        WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located((by, elems)))
    
    def click(self, elem, i=-1, by=By.CLASS_NAME):
        if(i==-1):
            self.driver.find_element(by, elem).click()
        else:
            self.driver.find_elements(by, elem)[i].click()

    def send_keys(self, elem, keys, i=-1, by = By.CLASS_NAME):
        if(i==-1):
            self.driver.find_element(by, elem).send_keys(keys)
        else:
            self.driver.find_elements(by, elem)[i].send_keys(keys)
    
    # Wait for loading icon to disapear + sleep for about [time] seconds
    def WAIT(self, time=1):
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loaderIcon")))
        sleep(time)

    # Get text from web element in place [i]
    def text(self, elem, by=By.CLASS_NAME, i=-1):
        if(i==-1):
            return self.driver.find_element(by, elem).text
        else:
            return self.driver.find_elements(by, elem)[i].text