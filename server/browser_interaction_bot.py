import sys
import random
import time

class BrowserInteractionBot():
    def __init__(self, config, seleniumTools):
        self.config = config
        self.seleniumTools = seleniumTools

    def getRandomTopic(self):
        print(random.choice(self.config['topics']))
        return random.choice(self.config['topics'])

    def buildSearchUrl(self):
        searchQuery = "+".join(self.getRandomTopic().split(" "))
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
                likeButton.click()
                print("liked it")
                result = True
            elif likeType == 0:
                self.seleniumTools.waitForCssSelector(endpoint="ytd-video-primary-info-renderer #info", visibility=True)
                dislikeButton = self.seleniumTools.driver.find_element_by_css_selector("ytd-video-primary-info-renderer ytd-toggle-button-renderer:last-of-type")
                dislikeButton.click()
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

    def run(self):
        self.seleniumTools.createNewTab("data:;")

        print("Automating browser interactions")
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
       