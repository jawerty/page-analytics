#!/usr/bin/python
import atexit
import time
import sys
import json
import uuid
from threading import Thread
from selenium import webdriver

from browser_interaction_bot import BrowserInteractionBot
from recommended_content_bot import RecommendedContentBot
from selenium_tools import SeleniumTools

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from fake_useragent import UserAgent

import _globals
import app_config

class Experiment():
    def __init__(self, experimentName):
        self.experimentName = experimentName
        self.sessionId = str(uuid.uuid4())
        experimentConfigFile = f'./experiments/{experimentName}-experiment.json'
        try:
            f = open(experimentConfigFile,)
            self.config = json.load(f)
        except:
            print("Couldn't open experiment config:", sys.exc_info()[0])
            sys.exit()

        try:
            profile = webdriver.FirefoxProfile(app_config.firefoxProfile)
            profile.set_preference("dom.webdriver.enabled", False)
            profile.set_preference('useAutomationExtension', False)
            profile.update_preferences()
            desired = DesiredCapabilities.FIREFOX

            self.driver = webdriver.Firefox(firefox_profile=profile,
                                    desired_capabilities=desired,
                                    executable_path=app_config.geckodriverLocation)

        except:
            print("Couldn't connect selenium driver", sys.exc_info())
            sys.exit()
    
    def exit_handler(self):
        self.driver.quit()

    def run(self):
        sessionId = str(uuid.uuid4())

        self.seleniumTools = SeleniumTools(self.driver)
        self.browseBot = BrowserInteractionBot(self.sessionId, self.experimentName, self.config, self.seleniumTools)
        self.recBot = RecommendedContentBot(self.sessionId, self.experimentName, self.config, self.seleniumTools)
        thread1 = Thread(target=self.browseBot.run)
        thread2 = Thread(target=self.recBot.run)

        # run the two threads        
        thread1.start() 
        thread2.start()

        # join threads with main thread to merge execution on completion
        thread1.join()
        thread2.join()
        
        

if __name__ == "__main__":
    _globals.init()
    e = Experiment(sys.argv[1]) 
    e.run()
