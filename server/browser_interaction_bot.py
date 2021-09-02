import sys
import random
import time
import json
import threading
import datetime
import _globals
import requests
from app_config import flaskServer
from utils import runJob

class BrowserInteractionBot():
    def __init__(self, sessionId, experimentName, config, seleniumTools):
        self.sessionId = sessionId
        self.experimentName = experimentName
        self.config = config
        self.seleniumTools = seleniumTools
        self.signedIn = False
        self.experimentType = self.config["experimentType"]
        topicConfigFile = './experiments/topics.json'
        try:
            f = open(topicConfigFile,)
            self.topicConfig = json.load(f)
        except:
            print("Couldn't open topic config:", sys.exc_info()[0])
            sys.exit()
        
        if self.experimentType == "topic":
            topicCategory = self.config["topicCategory"]
            if topicCategory in self.topicConfig:
                self.topics = self.topicConfig[topicCategory]
            else:
                print("Topic Category", topicCategory, "not in topics.json! Check you used the correct topic name.")
                sys.exit()

        elif self.experimentType == "ping-pong":
            # topicCategory is an array for ping pong
            topicCategories = self.config["topicCategory"]
            # just check if a topic does not exist
            for topicCategory in topicCategories:
                if topicCategory not in self.topicConfig:
                    print("Topic Category", topicCategory, "not in topics.json! Check you used the correct topic name.")
                    sys.exit()


            # take the first topicCategory
            self.currentTopicCategory = topicCategories[0]
            self.topics = self.topicConfig[topicCategories[0]]
            self.pingPongIterations = 0 # only used for ping pong experiements
    
    def sendData(self, data: dict):
        """function to send videoData objects to mongoDB"""
        status = requests.post(f"{flaskServer}browserInteraction", json=data)
    
    def getBrowserInteractionData(self):
        data: dict = {
            'topic': self.randomTopic,
            'config': self.config,
            'experimentName': self.experimentName,
            'timestamp':  datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S'),
            'sessionId': self.sessionId,
        }

        if self.experimentType == "ping-pong":
            data['pingPongTopicCategory'] = self.currentTopicCategory
            data['pingPongIteration'] = self.pingPongIterations
        
        return data

    def pingPongTopics(self):
        topicCategories = self.config["topicCategory"]
        topicCategoryIndex = topicCategories.index(self.currentTopicCategory)
        if topicCategoryIndex == len(topicCategories) - 1:
            newTopicCategoryIndex = 0 # reset if it hit the end of the array
        else:
            newTopicCategoryIndex = topicCategoryIndex + 1
        newTopicCategory = topicCategories[newTopicCategoryIndex]
        print("going from topic", self.currentTopicCategory, "to", newTopicCategory)
        self.currentTopicCategory = newTopicCategory
        self.topics = self.topicConfig[newTopicCategory]
        
    def getRandomTopic(self):
        randomTopic = random.choice(self.topics)
        print("Using topic", randomTopic)
        return randomTopic

    def buildSearchUrl(self):
        self.randomTopic = self.getRandomTopic()
        searchQuery = "+".join(self.randomTopic.split(" "))
        return f'https://www.youtube.com/results?search_query={searchQuery}'

    def hitSearchResultLink(self):
        element = self.seleniumTools.driver.find_element_by_css_selector("a#thumbnail")
        if self.config['clickVideo']:
            oldPage = self.seleniumTools.driver.find_element_by_tag_name('html')
            element.click()
            print("clicked new page")
        else:
            self.seleniumTools.driver.get(element.get_attribute('href'))
            print("go to new page")

    def likeVideo(self):
        likeType = self.config['likeType']
        result = False
        try:
            if likeType == 1:
                print('waiting')
                self.seleniumTools.waitForCssSelector(endpoint="ytd-video-primary-info-renderer #info", visibility=True)
                likeButton = self.seleniumTools.driver.find_element_by_css_selector("ytd-video-primary-info-renderer ytd-toggle-button-renderer:first-of-type")
                print(likeButton)
                if 'style-default-active' in likeButton.get_attribute('class').split():
                    print("already liked!")
                else:
                    likeButton.click()
                    print("liked it")
                result = True
            elif likeType == 0:
                self.seleniumTools.waitForCssSelector(endpoint="ytd-video-primary-info-renderer #info", visibility=True)
                dislikeButton = self.seleniumTools.driver.find_element_by_css_selector("ytd-video-primary-info-renderer ytd-toggle-button-renderer:last-of-type")
                if 'style-default-active' in dislikeButton.get_attribute('class').split():
                    print("already disliked!")
                else:
                    dislikeButton.click()
                    print("disliked it")
                result = True
            else:
                # likeVideo is null
                result = True
        except:
            print("liking video routine failed", sys.exc_info())
            result = False

        return result

    def subscribe(self):
        subscribe = self.config['subscribe']
        print(self.config['username'], self.config['password'], subscribe)
        if self.config['username'] and self.config['password'] and subscribe: # has to be user
            print("subscribing")
            try:  
                self.seleniumTools.waitForCssSelector(endpoint="ytd-video-primary-info-renderer #info", visibility=True)
                subscribeButton = self.seleniumTools.driver.find_element_by_css_selector("#subscribe-button.ytd-video-secondary-info-renderer")
                if subscribeButton.text == "SUBSCRIBE":
                    subscribeButton.click()
                    result = True
                    print("Successfully subscribed")
                else:
                    print("User already subscribed")
                    result = False
            except:
                print("subscribing to video routine failed", sys.exc_info())
        else:
            result = False

        return result

    def signIn(self):
        result = False
        username = self.config['username']
        password = self.config['password']
        try:
            if username and password:
                # Go to google login
                self.seleniumTools.driver.get('https://accounts.google.com/ServiceLogin/signinchooser')
                self.seleniumTools.waitForCssSelector(endpoint='#identifierId', visibility=True)
                
                # Enter username
                inputElement = self.seleniumTools.driver.find_element_by_css_selector('#identifierId')
                inputElement.send_keys(username)
                nextButton1 = self.seleniumTools.driver.find_element_by_css_selector('#identifierNext button')
                nextButton1.click()

                # Enter password 
                self.seleniumTools.waitForCssSelector(endpoint='input[type=\'password\']', visibility=True)
                passwordElement = self.seleniumTools.driver.find_element_by_css_selector('input[type=\'password\']')
                passwordElement.send_keys(password)
                nextButton2 = self.seleniumTools.driver.find_element_by_css_selector('#passwordNext button')
                oldPage = self.seleniumTools.driver.find_element_by_tag_name('html')
                nextButton2.click()
                # Check if new page loaded (page wont change if login fails)
                if self.seleniumTools.wait_for_page_load(oldPage):
                    print("Logged in successful")
                    result = True
                    self.signedIn = True
                else:
                    print("Could not log in")
                    result = False
            else:
                # user creds is null
                result = True
        except:
            print("Could not log in", sys.exc_info())

            result = False
        
        return result

    def getPositiveComment(self):
        return "I like this video!"

    def getNegativeComment(self):
        return "I don't like this video!"

    def comment(self):
        result = False
        username = self.config['username']
        password = self.config['password']
        commentType = self.config['comment']
        if commentType is not None:
            if username is None or password is None:
                print("You cannot comment without a username/password set")
                return result

            if commentType == 1:
                comment = self.getPositiveComment()
            elif commentType == 0:
                comment = self.getNegativeComment()
            else:
                return result
            try:
                # first check if page has commenting turned off
                message = self.seleniumTools.driver.find_element_by_css_selector("#message")
                if message:
                    if "Comments are turned off" in message.text:
                        print("Commenting is turned off in this video")
                        return result

                # need to scroll down page to open commenting
                if not self.scrolled:
                    self.seleniumTools.driver.execute_script("window.scrollTo(0, 500)") 
                    self.scrolled = True

                textareaSelector = "#placeholder-area.ytd-comment-simplebox-renderer"
                self.seleniumTools.waitForCssSelector(endpoint=textareaSelector, visibility=True)
                textarea = self.seleniumTools.driver.find_element_by_css_selector(textareaSelector)
                textarea.click()
                time.sleep(0.5)
                textarea_content = self.seleniumTools.driver.find_element_by_css_selector("#contenteditable-textarea [contenteditable=true]")
                textarea_content.send_keys(comment)

                submitButton = self.seleniumTools.driver.find_element_by_css_selector("#submit-button #button")
                submitButton.click()
                time.sleep(1)
                print("Commenting successful")
                result = True
            except:
                print("Commenting routine did not work: ", sys.exc_info())

        return result

    def report(self):
        result = False
        username = self.config['username']
        password = self.config['password']
        report = self.config['report']
        if report:
            if username and password:
                moreButtonSelector = "ytd-menu-renderer > yt-icon-button#button"
                self.seleniumTools.waitForCssSelector(endpoint=moreButtonSelector, visibility=True)
                moreButton = self.seleniumTools.driver.find_element_by_css_selector(moreButtonSelector)
                moreButton.click()
                time.sleep(0.5)
                reportButton = self.seleniumTools.driver.find_element_by_xpath("//ytd-menu-service-item-renderer[contains(text(), 'Report')]")
                reportButton.click()
                # just opens modal for now 
                # todo to complete form and actually report
                result = True
            else:
                print("You cannot report without a username/password set")

        return result

    def related(self):
        result = False
        related = self.config['related']
        if related is not None:
            def clickRelatedRoutine(i):
                print("clicking video", i+1, "of", related)
                print("waiting for section")
                watchNextSectionSelector = "#items.ytd-watch-next-secondary-results-renderer"
                self.seleniumTools.waitForCssSelector(endpoint=watchNextSectionSelector, visibility=True)
                firstVideoLinkSelector = "#items.ytd-watch-next-secondary-results-renderer a.yt-simple-endpoint:first-of-type"
                firstVideoLink = self.seleniumTools.driver.find_element_by_css_selector(firstVideoLinkSelector)
                
                oldPage = self.seleniumTools.driver.find_element_by_tag_name('html')
                print("clicking video link", firstVideoLink)
                firstVideoLink.click()
                time.sleep(1) # some buffer time before reruning
                # Check if new page loaded (page wont change if login fails)
                if i < related-1:
                    return clickRelatedRoutine(i+1)
                else:
                    print("Related video clicking finished")
                    return True
            try:
                result = clickRelatedRoutine(0)
            except:
                print("Related video routine did not work: ", sys.exc_info())

        return result

    def routine(self):
        print("Automating browser interactions")
        if not self.signedIn:
            if not self.signIn(): # if username and password set else be anon user
                sys.exit()

        self.seleniumTools.driver.get(self.buildSearchUrl())
        self.seleniumTools.waitForCssSelector(endpoint='.ytd-video-renderer', clickable=True)
        
        # clickVideo
        self.hitSearchResultLink() 

        # likeType
        self.likeVideo()

        # subscribe
        self.subscribe()
       
        # comment
        self.comment()

        # report
        self.report()

        # related
        self.related()

        self.sendData(data=self.getBrowserInteractionData())
        
        if self.experimentType == "ping-pong":
            self.pingPongIterations = self.pingPongIterations + 1
            if self.pingPongIterations == self.config['iterationsToBounce']:
                print("Bouncing topics")
                self.pingPongIterations = 0
                # go to next topic category in topicCategory array or reset to 0th index
                self.pingPongTopics() 

        print("Browser interactions finished") 
    
    def run(self):
        frequency = self.config["frequency"]   
        runJob(
            frequency,
            self.routine, 
            "Browser Interactions Bot waiting...", 
        )
