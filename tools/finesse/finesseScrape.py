'''
Finesse Scraper
Version 0.1.0b
Authors: Joseph Langford
Release: 09/25/2018

Changelog:
0.1.0 Initial version.
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from time import sleep
from datetime import datetime
import sys, threading, os, errno, linecache

class Actions:

    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    })

    def __init__(self, user, passw, ext):
        self.user = user
        self.pw = passw
        self.ext = ext
        self.driver = self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        #self.driver.set_window_position(555,375)
        #self.driver.set_window_size(970,475)

    def getCaller(self):
        #INSIDE FINESSE GADGET 2 IFRAME
        data = {}
        self.driver.switch_to.frame('finesse_gadget_2')

        name = self.driver.find_element_by_xpath('//*[@id="UserNameAutoPop"]')
        data['name'] = name.get_attribute('value')

        luid = self.driver.find_element_by_xpath('//*[@id="IDNumberAutoPop"]')
        data['luid'] = luid.get_attribute('value')

        un = self.driver.find_element_by_xpath('//*[@id="Field5AutoPop"]')
        data['un'] = un.get_attribute('value')

        qu = self.driver.find_element_by_xpath('//*[@id="SkillQueueAutoPop"]')
        data['qu'] = qu.get_attribute('value')

        tik = self.driver.find_element_by_xpath('//*[@id="Field6AutoPop"]')
        data['tik'] = tik.get_attribute('value')

        uType = self.driver.find_element_by_xpath('//*[@id="Field8AutoPop"]')
        data['uType'] = uType.get_attribute('value')
        #//*[@id="ApplyCallVariables"]
        applyButton = self.driver.find_element_by_xpath('//*[@id="ApplyCallVariables"]')

        #TO SWITCH BACK
        self.driver.switch_to.parent_frame()

        return data

    def open(self):
        print('Opening Finesse...')
        self.driver.get('https://lufinesse01.phones.liberty.edu/')
        #self.driver.get('https://lufinesse01.phones.liberty.edu/desktop/container/j_security_check?locale=en_US')
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "j_username"))
            )

        except:
            self.driver.quit()

        un = self.driver.find_element_by_name('j_username')
        un.send_keys(self.user)

        pw = self.driver.find_element_by_name('j_password')
        pw.send_keys(self.pw)

        ext = self.driver.find_element_by_name('extension_login_user')
        ext.send_keys(self.ext)
        ext.send_keys(Keys.TAB)
        ext.send_keys(Keys.TAB)
        ext.send_keys(Keys.ENTER)


        try:
            #button = self.driver.find_element_by_id('signin-button')
            #button = self.driver.find_element_by_class_name('button')
            #button.click()

            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="state-text"]'))
            )

        except:
            print('Unable to autologin.  Please press Sign In...')
            sleep(5)
            #self.driver.quit()

        # state = self.driver.find_element_by_xpath('//*[@id="state-text"]')
        # sleep (2)
        # state.click()
        # x = self.driver.find_element_by_id('state-READY')
        # x.click()


    def getState(self):
        state = self.driver.find_element_by_xpath('//*[@id="state-text"]')
        s = state.text

        return s

    def waitForTalking(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                self.checkTalking()
            )

        except NoSuchElementException:
            return 'kill'

        finally:
            try:
                return self.getState()

            except NoSuchElementException:
                return 'kill'

    def answerPhone(self):
        try:
            self.driver.switch_to.frame('finesse_gadget_0')
            x = self.driver.find_element_by_xpath('//*[@id="dijit_form_Button_10_label"]')
            x.click()
            #TO SWITCH BACK
            self.driver.switch_to.parent_frame()
            return 'True'
        except (NoSuchElementException, NoSuchFrameException):
            return 'False'
        except ElementNotVisibleException:
            self.driver.switch_to.parent_frame()
            return 'ElementNotVisibleException'

    def hangup(self):
        try:
            self.driver.switch_to.frame('finesse_gadget_0')
            x = self.driver.find_element_by_xpath('//*[@id="dijit_form_Button_13_label"]')
            x.click()
            #TO SWITCH BACK
            self.driver.switch_to.parent_frame()
            return 'True'
        except (NoSuchElementException, NoSuchFrameException):
            return 'False'
        except ElementNotVisibleException:
            self.driver.switch_to.parent_frame()
            return 'ElementNotVisibleException'

    def dialNumber(self, number):
        try:
            self.driver.switch_to.frame('finesse_gadget_3')
            x = self.driver.find_element_by_xpath('//*[@id="Number"]')
            x.clear()
            x.send_keys(number)
            y = self.driver.find_element_by_xpath('//*[@id="DirectDialButton"]')
            y.click()
            #TO SWITCH BACK
            self.driver.switch_to.parent_frame()
            return 'True'
        except NoSuchElementException:
            return 'NoSuchElementException'
        except NoSuchFrameException:
            return 'NoSuchFrameException'
        except ElementNotVisibleException:
            self.driver.switch_to.parent_frame()
            return 'ElementNotVisibleException'

    def transferNumber(self, number):
        try:
            self.driver.switch_to.frame('finesse_gadget_0')
            x = self.driver.find_element_by_xpath('//*[@id="dijit_form_Button_6_label"]')
            x.click()
            y = self .driver.find_element_by_xpath('//*[@id="numberDisplay"]')
            y.clear()
            sleep(1)
            y.send_keys(number)
            sleep(1)
            z = self.driver.find_element_by_xpath('//*[@id="buttonCallId_label"]')
            z.click()
            #TO SWITCH BACK
            self.driver.switch_to.parent_frame()
            return 'True'
        except NoSuchElementException:
            return 'NoSuchElementException'
        except NoSuchFrameException:
            return 'NoSuchFrameException'
        except ElementNotVisibleException:
            self.driver.switch_to.parent_frame()
            return 'ElementNotVisibleException'


    def quit(self):
        self.driver.quit()

class NoInterface(Actions, threading.Thread):
    def __init__(self, user, passw, ext):
        threading.Thread.__init__(self)
        Actions.__init__(self, user, passw, ext)

        self.running = True
        self.call_logged = False

    def run(self):
        print('Starting Finesse service...')
        self.open()

        while self.getState() == "Not Ready":
            sleep(1)

        while self.running:
            try:
                w = self.waitForTalking()

            except socket_error as serr:
                if serr.errno != errno.ECONNREFUSED:
                    self.running = False

            except WebDriverException:
                    self.running = False

            if w == 'kill':
                self.running = False

            elif w == 'Talking':
                if self.call_logged:
                    pass

                else:
                    self.dump(self.getCaller())

                if self.call_logged == False:
                    self.call_logged = True

            else:
                if self.call_logged == True:
                    self.call_logged = False
            sleep(2)

    def dump(self, data):
            #data = (datetime.utcnow() , data)
            if os.path.exists(CALL):
                os.remove(CALL)

            try:
                with open(CALL, 'w+') as f:
                    if data['un'] != '':
                        f.write(data['un']+'\n')

                    elif data['luid'] != '':
                        f.write(data['luid']+'\n')

                    else:
                        f.write('ithelpdesk'+'\n')

                    f.close()
            except:
                raise

            try:
                with open(FINESSE_LOG, 'a+') as f:
                    #f.write(datetime.utcnow() + '\n' + str(data) + '\n')
                    t = str(datetime.utcnow())
                    f.write(t + '\n' + str(data) + '\n')
                    f.close()

            except:
                raise
