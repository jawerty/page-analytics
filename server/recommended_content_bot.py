
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import threading
import _globals
import time
import datetime
from utils import runJob
from dataParser import Parser
from app_config import flaskServer

from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime

class RecommendedContentBot():
    def __init__(self, sessionId, experimentName, config, seleniumTools):
        self.sessionId = sessionId
        self.experimentName = experimentName
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

    def sendVideoData(self, data: list):
        """function to send videoData objects to mongoDB"""
        data: dict = {'data': data}
        status = requests.post(f"{flaskServer}video", json=data)
    
    def sendAdData(self, data: list):
        """function to send videoData objects to mongoDB"""
        data: dict = {'data': data}
        status = requests.post(f"{flaskServer}ad", json=data)
            
    def routine(self):
        """function to run recommended bot"""
        print("Fetching recommended content")
        self.seleniumTools.driver.get("https://youtube.com")
        if self.seleniumTools.waitForCssSelector(".style-scope.ytd-video-meta-block", visibility=True):
            recommendedMetadata = self.seleniumTools.getMetadataForRecommendedVideos()                
            
            links = self.findHrefs()[0:8]
            videoDataMap = {}
            for i, link in enumerate(links):
                data = self.collectVideoData(videoLink=link, videoNumber=i)
                data['sessionId'] = self.sessionId
                data['experimentName'] = self.experimentName

                parsed_url = urlparse(link)
                videoId = parse_qs(parsed_url.query)['v'][0]

                data['videoId'] = videoId
                videoDataMap[data['videoId']] = data
                        
            if recommendedMetadata is not None:
                recommendedVideos = recommendedMetadata["videos"]
                recommendedAds = recommendedMetadata["ads"]

                if len(recommendedVideos) > 0:
                    for recommendedMetadataVideo in recommendedVideos:
                        if recommendedMetadataVideo['videoId'] in videoDataMap:
                            videoData = videoDataMap[recommendedMetadataVideo['videoId']].copy()
                            videoData.update(recommendedMetadataVideo)
                            videoDataMap[recommendedMetadataVideo['videoId']] = videoData
                            print("got video metadata")

                if len(recommendedAds) > 0:
                    now: datetime = datetime.now()
                    def setMoreData(ad):
                        ad['sessionId'] = self.sessionId
                        ad['experimentName'] = self.experimentName
                        ad['timestamp']: str = now.strftime('%Y/%m/%dT%H:%M:%S') 
                        print("got ad metadata")
                        return ad

                    recommendedAds = list(map(setMoreData, recommendedAds))
                    self.sendAdData(data=recommendedAds)
                    
            videoData = list(videoDataMap.values())
            self.sendVideoData(data=videoData)
            

        print("RecommendedContentBot finished")

        
    def run(self):
        frequency = 300 
        runJob(
            frequency,
            self.routine, 
            "Recommended bot waiting..." 
        )