#!/usr/bin/python
import atexit

import sys
import json
from threading import Thread
from selenium import webdriver

from browser_interaction_bot import BrowserInteractionBot
from recommended_content_bot import RecommendedContentBot
from selenium_tools import SeleniumTools
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

class Experiment():
    def __init__(self, experimentName):
        experimentConfigFile = f'./experiments/{experimentName}-experiment.json'
        try:
            f = open(experimentConfigFile,)
            self.config = json.load(f)
        except:
            print("Couldn't open experiment config:", sys.exc_info()[0])
            sys.exit()

        try:
            options = Options()
            # ua = UserAgent()
            # userAgent = ua.random
            # print(userAgent)
            # options.add_argument(f'user-agent={userAgent}')
            self.driver = webdriver.Chrome(options=options, executable_path="./chromedriver_v92")
            # atexit.register(self.exit_handler)

        except:
            print("Couldn't connect selenium driver", sys.exc_info())
            sys.exit()
    
    def exit_handler(self):
        self.driver.quit()

    def run(self):
        self.seleniumTools = SeleniumTools(self.driver)
        self.browseBot = BrowserInteractionBot(self.config, self.seleniumTools)
        self.recBot = RecommendedContentBot(self.config, self.seleniumTools)
        thread1 = Thread(target=self.browseBot.run)
        thread2 = Thread(target=self.recBot.run)

        # run the two threads
        thread1.start() 
        thread2.start()

        # join threads with main thread to merge execution on completion
        thread1.join()
        thread2.join()

e = Experiment(sys.argv[1]) 
e.run()