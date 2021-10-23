import uuid
import sys
import json
import app_config
from selenium import webdriver
from selenium_tools import SeleniumTools

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TopicGenerator():
    def __init__(self, topicCount, topicListLimit):
        self.topicCount = int(topicCount)
        self.topicListLimit = int(topicListLimit)

    def getTrendingTopics(self):
        googleTrendsUrl = "https://trends.google.com/trends/trendingsearches/daily?geo=US"
        self.seleniumTools = SeleniumTools(self.driver)
        self.seleniumTools.driver.get(googleTrendsUrl)
        
        self.seleniumTools.waitForCssSelector(endpoint=".feed-item .title", clickable=True)
        feedTitles = self.seleniumTools.driver.find_elements_by_css_selector(".feed-item .title")
        if len(feedTitles) < self.topicCount:
            def loadAndFetchMoreFeedTitles():
                self.seleniumTools.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
                loadMoreButton = self.seleniumTools.driver.find_element_by_css_selector(".feed-load-more-button")
                loadMoreButton.click()
                self.seleniumTools.waitForCssSelector(endpoint=".feed-load-more-button", clickable=True)
                feedTitles = self.seleniumTools.driver.find_elements_by_css_selector(".feed-item .title")
                if len(feedTitles) < self.topicCount:
                    return loadAndFetchMoreFeedTitles()
                else:
                    return feedTitles
            feedTitles = loadAndFetchMoreFeedTitles()

        titlesToScrape = feedTitles[0:self.topicCount]
        topics = [x.text for x in titlesToScrape]
        print("Topic Categories", topics, len(topics))
        return topics

    def generateTopicsListsForTopics(self, topics):
        topicListLimit = self.topicListLimit
        topicLists = {} # topic to list 

        def getTopicArray(topicList, linkCache, i):
            print("getting more topics: current topic count", len(topicList))
            try:
                metaKeywords = self.seleniumTools.driver.find_element_by_css_selector("meta[name='keywords']")
                keywordString = metaKeywords.get_attribute('content')
                if keywordString:
                    print("adding topics to list", keywordString)
                    for newTopic in keywordString.split(', '):
                        newTopic = newTopic.lower()
                        if newTopic not in topicList:
                            topicList.append(newTopic)
                
                if len(topicList) > topicListLimit:
                    return topicList

                watchNextSectionSelector = "#items.ytd-watch-next-secondary-results-renderer"
                self.seleniumTools.waitForCssSelector(endpoint=watchNextSectionSelector, visibility=True)
                self.seleniumTools.waitForCssSelector(endpoint='ytd-compact-video-renderer', visibility=True)
                videoLinkSelector = "#items.ytd-watch-next-secondary-results-renderer a.yt-simple-endpoint"
                videoLinks = self.seleniumTools.driver.find_elements_by_css_selector(videoLinkSelector)
                allCached = True
                for videoLink in videoLinks: 
                    href = videoLink.get_attribute('href')
                    print("got href", href)
                    if href in linkCache: # don't go to the same link for a single topic
                        continue

                    allCached = False
                    linkCache.append(href)

                    if href:
                        break
                
                if allCached:
                    # just get the topic list so far
                    return topicList

                print("Going to link", href)
                self.seleniumTools.driver.get(href)
                return getTopicArray(topicList, linkCache, i+1)
            except:
                print("Topic Generator failed halfway", sys.exc_info())
                return topicList

        for topic in topics:
            print("getting topic list for", topic)
            self.seleniumTools.driver.get(f'https://www.youtube.com/results?search_query={topic}')
            self.seleniumTools.waitForCssSelector(endpoint='.ytd-video-renderer', clickable=True)
            elements = self.seleniumTools.driver.find_elements_by_css_selector("a#thumbnail")
            
            for element in elements:
                url = element.get_attribute('href')
                if not url:
                    continue
                self.seleniumTools.driver.get(url)
                topicList = getTopicArray([topic.lower()], [], 0)
                topicLists[topic] = topicList[0:topicListLimit] # may be an excess
                break

        return topicLists
    
    def saveTopicLists(self, topicLists):
        fileId = str(uuid.uuid4())
        filename = f'./topics-{fileId}.json'
        with open(filename, 'w+') as outfile:
            json.dump(topicLists, outfile, indent=4)

        return filename

    def setupDriver(self):
        profile = webdriver.FirefoxProfile(app_config.firefoxProfile)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
            
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        self.driver = webdriver.Firefox(firefox_profile=profile,
            desired_capabilities=desired,
            executable_path=app_config.geckodriverLocation)

    def run(self):
        self.setupDriver()
        topics = self.getTrendingTopics()
        topicLists = self.generateTopicsListsForTopics(topics)
        filename = self.saveTopicLists(topicLists)
        print(filename, "saved")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        topicCount = sys.argv[1]
        topicListLimit = sys.argv[2]
    else:
        print("Please run with proper arguments: python3 topic_generator.py <topic categories count> <topic list limit>")
        sys.exit(1)
    
    t = TopicGenerator(topicCount, topicListLimit)
    t.run()