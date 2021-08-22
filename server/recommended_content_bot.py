
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import threading
import _globals
import time
from utils import runTimer

class RecommendedContentBot():
    def __init__(self, config, seleniumTools):
        self.config = config
        self.seleniumTools = seleniumTools

    def findHrefs(self) -> list:
        """function to find hrefs of recommended videos"""
        eles: list = self.seleniumTools.driver.find_elements_by_css_selector('#content ytd-rich-grid-renderer #video-title-link')
        links: list = []
        for ele in eles:
            links.append(ele.get_attribute('href'))
        return links


    def collectVideoData(self, videoLink: str) -> dict:

        r =  requests.get(videoLink)
        soup = BeautifulSoup(r.content, 'html.parser')
        keywords = soup.find('meta', {'name':'keywords'})['content']
        # continue to find logic
        # xpath to find the beautiful to find script tags with ytInitalData
        # remove var, get script content then json dump
        """//script[contains(text(),"ytInitialData")] -- bs4 equivalence 
            soup(text=re.compile(r' ytInitialData')):
            .split("var ytInitialData = ")[1]
            remove semicolon from the string
            json.loads everything"""
        return keywords


    def routine(self):
        print("Fetching recommended content")
        self.seleniumTools.driver.get("https://youtube.com")
        if self.seleniumTools.waitForCssSelector(".style-scope.ytd-video-meta-block", visibility=True):
            links = self.findHrefs()[0:8]
            videoData = self.collectVideoData(videoLink=links[0])
        print("RecommendedContentBot finished")

        
    def run(self):
        frequency = 600 
        runTimer(
            frequency=frequency, 
            waitingMessage="Recommended bot waiting...", 
            callback=self.routine
        )