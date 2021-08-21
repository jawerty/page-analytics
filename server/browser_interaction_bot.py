import sys
import random
import time
import threading

class BrowserInteractionBot():
    def __init__(self, config, seleniumTools):
        self.config = config
        self.seleniumTools = seleniumTools
        self.scrolled = False

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
            print("Clicked new page")
        else:
            self.seleniumTools.driver.get(element.get_attribute('href'))
            print("Went to new page (without clicking)")

    def likeVideo(self):
        likeType = self.config['likeType']
        result = False
        try:
            if likeType == 1:
                print('waiting')
                self.seleniumTools.waitForCssSelector(endpoint="ytd-video-primary-info-renderer #info", visibility=True)
                likeButton = self.seleniumTools.driver.find_element_by_css_selector("ytd-video-primary-info-renderer ytd-toggle-button-renderer:first-of-type")
                
                if 'style-default-active' in likeButton.get_attribute('class').split():
                    print('Video already liked!')
                else:
                    likeButton.click()
                    print("Video liked")
                result = True
            elif likeType == 0:
                self.seleniumTools.waitForCssSelector(endpoint="ytd-video-primary-info-renderer #info", visibility=True)
                dislikeButton = self.seleniumTools.driver.find_element_by_css_selector("ytd-video-primary-info-renderer ytd-toggle-button-renderer:last-of-type")
                if 'style-default-active' in dislikeButton.get_attribute('class').split():
                    print('Video already disliked!')
                else:
                    dislikeButton.click()
                    print("Video disliked")
                result = True
            else:
                # likeVideo is null
                result = True
        except:
            print("Liking video routine failed", sys.exc_info())
            result = False

        return result

    def subscribe(self):
        result = False
        subscribe = self.config['subscribe']
        if subscribe: # has to be user
            username = self.config['username'] 
            password = self.config['password'] 
            if username is not None or password is not None:
                print("You must set username and password to subscribe")
                return result
           
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
                print("Subscribing to video routine failed", sys.exc_info())
        
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
        self.seleniumTools.createNewTab("data:;")

        print("Automating browser interactions")
        if not self.signIn(): # if username and password set and successfully logged in else be anon user
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

        print("Browser interactions finished") 
    
    def run(self):
        frequency = self.config["frequency"]   
        def runTimer(): 
            threading.Timer(frequency, runTimer).start()        
            self.routine() #runs immediately as well

        runTimer()