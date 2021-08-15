from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumTools():
    def __init__(self, driver):
        self.driver = driver

    def createNewTab(self, url):
        self.driver.execute_script(f'window.open("{url}","_blank");')
        newTabIndex = len(self.driver.window_handles)-1
        newTab = self.driver.window_handles[newTabIndex]
        self.driver.switch_to_window(newTab)
        
    def waitForYoutubeSearchResults(self):
        print("waiting")
        response = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "yt-simple-endpoint")))
        print("got it")