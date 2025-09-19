# Imports
from myWebBrowser import scrapePage

#  Setting up my classes && constants
class Country:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance

# Setting up data cleaning functions
def getNewestCountry(data):
    try :
        func_name = data # GET THE TAG
        func_distance = int(data) # GET THE TAG
    except Exception as e:
        print('No country was found')
        return None
    newest_country = Country(func_name, func_distance)
    return newest_country