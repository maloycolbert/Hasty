'''
Argos Scraper
Version 2.5.0b
Authors: Joseph Langford
Maintainer: Colbert Maloy
Release: 4/6/2017

Changelog:
1.0 Initial version.
1.1 Correction to Finesse Login.
1.2 Correction to Chromium window placement.
1.3 Correction to Argos webViewer login.
1.4 Added Finesse functionality pickup/hangup/dial/transfer
1.5 Updated Chromedriver to 2.33.  pip install -U selenium & pip install -U chromedriver
2.0 Removed ServiceNow and Finesse functions. Finesse functions have been moved to a separate file
2.5 Updated Chromdriver, Argos updated; updated references and 2-d array

Helper.search() returns an 2d array with the following scheme:

The top right field, for users with an AD account
[0][0] == Users Name
[0][1] == LUID
[0][2] == FraudAlert
[0][3] == Username
[0][4] == l4SSN
[0][5] == dob
[0][6] == zip
[0][7] == Address
[0][8] == Country
[0][9] == Phone

The bottom right field, for users without an AD account
[1][0] == Name

index [2]* contains UM notes if there. If notes do exist then they are paired.
Each pair is set of the date of the note and then the note itself
[2][0] == Most recent note's date
[2][1] == Most recent note's note
...

The Fraud/Legal/ASIST field
[3][0] == Fraud Alert, N if none
[3][1] == Legal Action, N if none
[3][2] == ASIST Disabled, N if n/a


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
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime
from socket import error as socket_error
import sys, threading, os, errno, linecache

#Init directory for all text files
PATH = os.path.join('c:', os.sep, 'scripts','helper')
APP_DATA = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local')
USER_DATA = os.path.join(APP_DATA, 'Google', 'Chrome', 'User Data')
CALL = os.path.join(PATH, 'call.txt')
FINESSE_LOG = os.path.join(PATH, 'finesseLog.txt')
FILENAME = 'aext'
LOCSTORE = os.path.join(PATH, 'wloc.txt')

#Headers for csv format, required by Helper tool
headers = [
    ['Value0','Value1','Value2','Value3','Value4','Value5','Value6','Value7','Value8','Value9'],
    ['Value0','Value1','Value2','Value3','Value4','Value5','Value6','Value7','Value8','Value9'],
    ['Date_Added','Note'],
    ['FraudAlert','LegalAction','AsistDisabled']
]

class Helper:
    '''
    This class is for interacting with the Argos Webviewer and the HelperLookupV2 report
    located at -> https://argosreport05.liberty.edu/Argos/AWV/#explorer/Banner%00Helpdesk%00Reports/HelperLookupV2
    signs in, handles expired sessions and if the page is closed before a call is made to the page
    extracts user's data into txt files at C:/scripts/helper for the Service Now driver to use later on
    ** if Chromedriver stalls then upgrade Chromedriver from https://chromedriver.storage.googleapis.com/index.html
         current version updated from 75.0.3770.8 repository.
    '''

    chrome_options = Options()
    #chrome_options.add_argument('--load-extension=./Auto-Refresh_v1.3.11.crx')
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
    chrome_options.add_extension('./Auto-Refresh_v1.3.11.crx')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        #self.driver.set_window_size(675,465)
        #self.driver.set_window_position(555,1)

    def open(self):
        #Open Argos Web Viewer directly to HelperLookupV2
        print('Opening Argos Web Viewer...')
        self.driver.get('https://argosreports05.liberty.edu/Argos/AWV/#shortcut/shared//datablock/HelperLookupV2')
        #Wait for page to load
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="loginUsername"]'))
            )
        #Quit on failure
        except:
            self.driver.quit()
        #Wait to prevent typing before sign in page animation finishes
        sleep(0.5)
        #Sign in
        field_username = self.driver.find_element_by_xpath('//*[@id="loginUsername"]')
        field_password = self.driver.find_element_by_xpath('//*[@id="loginPassword"]')
        button_signIn  = self.driver.find_element_by_xpath('//*[@id="modalLogin"]/div[3]/button')

        field_username.send_keys(self.username)
        field_password.send_keys(self.password)
        button_signIn.click()
        sleep(0.5)


    def search(self, un):
        #Wait for search input to load
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="fo-idn"]/input'))
            )
        #If it doesn't load, go to recover method
        except TimeoutException:
            return self.recover(un)
        #If window is closed, reinitialize driver and run recover method
        except socket_error as serr:
            if serr.errno != errno.ECONNREFUSED:
                self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
                self.recover(un)

        #Once we find the search input, clear it, fill it out and press Enter to start search
        field_search = self.driver.find_element_by_xpath('//*[@id="fo-idn"]/input')
        field_search.clear()
        field_search.send_keys(un)
        field_search.send_keys(Keys.ENTER)
        #Wait for results
        sleep(10)
        #Init arrays for returning user data from search
        a = []
        b = []
        c = []
        d = []
        #Find container for top box of report
        #Find span items in box
        results_top = self.driver.find_element_by_xpath('//*[@id="fo-IDSearch"]/div/div[1]/div[2]')
        x = results_top.find_elements_by_tag_name('span')
        #Add all text to array
        for i in x:
        	a.append(i.get_attribute('outerText'))
        #Strip down to first result
        if len(a) > 0:
            a = a[0:9]
        #If top box is empty, search bottom box for Claim data
        else:
            results_bottom = self.driver.find_element_by_xpath('//*[@id="fo-CalimAccount"]/div/div[1]/div[2]')
            x = results_bottom.find_elements_by_tag_name('span')
            #Add all text to array
            for i in x:
                b.append(i.get_attribute('outerText'))
            #Strip down to first result
            b = b[0:8]
        #Search bottom left box for User Manager notes
        um = self.driver.find_elements_by_xpath('//*[@id="fo-multicolumn1"]/div/div[1]/div[2]')
        #Add all text to array
        for v in um:
        	x = v.find_elements_by_tag_name('span')
            #Add all text to the array, strip no results
        	for i in x:
        		c.append(i.get_attribute('outerText'))
        #Search top left box for flag data
        results_flags = self.driver.find_elements_by_xpath('//*[@id="fo-multicolumn2"]/div/div[1]/div[2]')

        for x in results_flags:
            #Add all text to the array, strip no results
            for i in x.find_elements_by_tag_name('span'):
                d.append(i.get_attribute('outerText'))

        #DEBUG: print a, b, c, d
        #Return all results in a 4 length list, including blank entries
        return [a, b, c, d]

    def recover(self, un):
        #Check title to see if form is open
        title = self.driver.title
        #If form is not open, go to it and wait for it to load
        if title != 'Argos Web Viewer by Evisions':
            self.driver.get('https://argosreports05.liberty.edu/Argos/AWV/#explorer/Banner%00Helpdesk%00Reports/HelperLookupV2')

            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="loginUsername"]'))
                )

            except:
                self.driver.quit()
            #Precautious wait to prevent errors
            sleep(0.5)
        #Once we're sure we're on the form, sign in again
        if title == 'Argos Web Viewer by Evisions':
            self.driver.set_window_size(675,465)
            field_username = self.driver.find_element_by_xpath('//*[@id="loginUsername"]')
            field_password = self.driver.find_element_by_xpath('//*[@id="loginPassword"]')
            button_signIn  = self.driver.find_element_by_xpath('//*[@id="modalLogin"]/div[3]/button')
            field_username.send_keys(self.username)
            field_password.send_keys(self.password)
            button_signIn.click()
            sleep(.5)
            self.driver.set_window_size(1180,370)
        self.search(un)

    def dump(self, top, bottom, usermanager, flags):
        #Store list with report results
        d = [top, bottom, usermanager, flags]
        #Loop through list of 0 - 3 for the logic of the aext0 - aext3 files
        for n in range(4):
            #Create file name, ex: aext0.txt
            FILEN = FILENAME + str(n) +'.txt'
            #Delete all files in directory to fit into Helper logic for if user data exists
            if os.path.exists(os.path.join(PATH, FILEN)):
                os.remove(os.path.join(PATH, FILEN))
            #First two files aext0 and aext1
            if n <= 1:
                #If data exists in list, write headers first, then data to meet required csv format
                if len(d[n]) > 0:
                    try:
                        with open(os.path.join(PATH, FILEN), 'w+') as f:
                            #DEBUG:print('\t'.join(headers[n])+'\n')
                            #DEBUG:print('\t'.join(d[n]))
                            f.write('\t'.join(headers[n])+'\n')
                            f.write('\t'.join(d[n]))
                        #Close file to prevent issue loading into Helper.
                        f.close()

                    except:
                        raise
            #Second two files aext2 and aext3
            else:
                #Write headers, then data
                with open(os.path.join(PATH, FILEN), 'w+') as f:
                    f.write('\t'.join(headers[n])+'\n')
                    try:
                        f.write('\t'.join(d[n]))
                    except:
                        raise
                    f.close()

    def quit(self):
        self.driver.quit()
