

# -------------------------------------
# The better way to do this, unapproved by management
# # -------------------------------------
# from urllib.request import urlopen
#
# SIMPLE_URL = "http://www.dinopass.com/password/simple"
# COMPLEX_URL = "http://www.dinopass.com/password/strong"
#
# def getPassword():
#     response = urlopen(SIMPLE_URL)
#     bytes = response.readline()
#     return bytes.decode()
#
# def GetComplexPassword():
#     response = urlopen(COMPLEX_URL)
#     bytes = response.readline()
#     return bytes.decode()

import datetime
import random

def getPassword():

    rand4 = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))

    Adjectives = ['Blue','Red','Green']
    Nouns = ['house','tree','apple']

    password = random.choice(Adjectives) + random.choice(Nouns) + rand4
    return password
