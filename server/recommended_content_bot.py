
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class RecommendedContentBot():
    def __init__(self, config, seleniumTools):
        self.config = config
        self.seleniumTools = seleniumTools

    def getRecommendedvideoData(self):
        data = WebDriverWait(self.seleniumTools.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#video-detail")))
        print(data)



    def run(self):
        print("Fetching recommended content")
        self.seleniumTools.createNewTab(url="http://youtube.com")
        self.getRecommendedvideoData()
