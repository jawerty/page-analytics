import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class SeleniumTools():
    def __init__(self, driver):
        self.driver = driver

    def createNewTab(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
        newTabIndex = len(self.driver.window_handles)-1
        newTab = self.driver.window_handles[newTabIndex]
        self.driver.switch_to_window(newTab)
    
    def waitForXPath(self, endpoint: str):
        try:
            response = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, f'{endpoint}')))
            result = True
        except:
            print(sys.exc_info())
            result = False

        return result

    def waitForCssSelector(self, endpoint: str, clickable: bool =  False, visibility: bool = False, seconds: int = 30 ) -> bool:
        try:
            if clickable:
                response = WebDriverWait(self.driver, seconds).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'{endpoint}')))
                result = True
            elif visibility:
                response = WebDriverWait(self.driver, seconds).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'{endpoint}')))
                result = True
            else:
                print('Choose Selector Type: clickable | visibility')
                result = False
        except:
            print(sys.exc_info())
            result = False

        return result

    def wait_for_page_load(self, oldPage, timeout=30):
        result = True
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.staleness_of(oldPage)
            )
        
        except:
            print(sys.exc_info())
            result = False

        return result

    def setAttribute(self, element, attrName, attrValue):
        try:
            self.driver.execute_script(f'arguments[0].setAttribute(\'{attrName}\',arguments[1])',element, attrValue)
            result = True
        except:
            result = False

        return result

    def getAdPlacementData(self):
        try:
            findScript = "function _e_x_p_() { try { result = window.ytcfg.data_.SBOX_SETTINGS.SEARCHBOX_COMPONENT.__dataHost.parentComponent.__data.data.playerResponse.adPlacements; } catch (e) { result = null; } return result; }; return _e_x_p_();"
            adPlacements = WebDriverWait(self.driver, 5).until(lambda driver: driver.execute_script(findScript))
        except:
            print("Could not get any adPlacements", sys.exc_info())
            return None
            
        # print(adPlacements)
        adPlacementData = []
        for adPlacement in adPlacements:
            try:
                adCompanyDomain = adPlacement["adPlacementRenderer"]["renderer"]["instreamVideoAdRenderer"]["playerOverlay"]["instreamAdPlayerOverlayRenderer"]["visitAdvertiserRenderer"]["buttonRenderer"]["text"]["runs"][0]
                if 'text' in adCompanyDomain:
                    adPlacementData.append({ "adDomain": adCompanyDomain['text'] })
            except:
                print("Could not find ad domain")

        return adPlacementData