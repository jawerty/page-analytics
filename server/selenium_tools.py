class SeleniumTools():
    def __init__(self, driver):
        self.driver = driver

    def createNewTab(self, url):
        self.driver.execute_script(f'window.open("{url}","_blank");')
