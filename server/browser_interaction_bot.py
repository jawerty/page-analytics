import random

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

    def run(self):
        print("Automating browser interactions")
        self.seleniumTools.createNewTab(self.buildSearchUrl())
        self.seleniumTools.waitForCssSelector('.ytd-video-renderer')
        print("got it")