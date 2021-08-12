
class RecommendedContentBot():
    def __init__(self, config, seleniumTools):
        self.config = config
        self.seleniumTools = seleniumTools

    def run(self):
        print("Fetching recommended content")
