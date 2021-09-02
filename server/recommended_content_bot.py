
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import threading
import _globals
import time
from utils import runJob
from dataParser import Parser
from app_config import flaskServer

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

    def collectVideoData(self, videoLink: str, videoNumber: int) -> dict:
        """function to find video data per recommended video"""
        r =  requests.get(videoLink)
        soup = BeautifulSoup(r.content, 'html.parser')
        data = Parser(soup=soup, videoNumber=videoNumber).collect()

        return data

    def sendData(self, data: list):
        """function to send videoData objects to mongoDB"""
        data: dict = {'data': data}
        status = requests.post(f"{flaskServer}video", json=data)
        
    def routine(self):
        """function to run recommended bot"""
        print("Fetching recommended content")
        self.seleniumTools.driver.get("https://youtube.com")
        if self.seleniumTools.waitForCssSelector(".style-scope.ytd-video-meta-block", visibility=True):
            links = self.findHrefs()[0:8]
            videoData = []
            for i, link in enumerate(links):
                data = self.collectVideoData(videoLink=link, videoNumber=i)
                videoData.append(data)
            self.sendData(data=videoData)
        print("RecommendedContentBot finished")

        
    def run(self):
        frequency = 600 
        runJob(
            frequency,
            self.routine, 
            "Recommended bot waiting..." 
        )