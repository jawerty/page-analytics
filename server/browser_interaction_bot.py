class BrowserInteractionBot():
    def __init__(self, config, seleniumTools):
        self.config = config
        self.seleniumTools = seleniumTools

    def run(self):
        print("Automating browser interactions")
        self.seleniumTools.createNewTab("http://youtube.com")
