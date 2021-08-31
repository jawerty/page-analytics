import re

class Parser:
    """object to parse video data from beautiful soup 
        - internal class for recommendation bot"""
    def __init__(self, soup: object, videoNumber: int):

        self.soup: object = soup
        self.videoNumber: int = videoNumber
        self.response: dict = {}

    def findVideoNumber(self):
        """function to label video number"""
        self.response['video_timeline_number']: int = self.videoNumber

    def findTitle(self):
        """function to label video title"""
        response = self.soup.select('title')[0].text
        response = re.sub(r' - YouTube$', '', response)
        self.response['video_title']: str = response

    def findKeywords(self):
        """function to scrape keywords"""
        self.response['keywords']: list = self.soup.find('meta', {'name': 'keywords'})['content'].split(', ')
        self.response['keyword_count']: int = len(self.response['keywords'])


    def collect(self) -> dict:
        """function to run full collection"""
        self.findVideoNumber()
        self.findTitle()
        self.findKeywords()
        return self.response