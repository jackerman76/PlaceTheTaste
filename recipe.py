import time
from time import gmtime, strftime
from datetime import datetime
from geopy import distance
import json
#from utils import *

class Recipe():
    def __init__(self, username=None, recipe_name=None, picture=None, ingredients=None, 
    geolocation=None, tags=None, directions=None, ratings=None, recipe_id=None, timestamp=None):
        self.username = username
        self.recipe_name = recipe_name
        self.picture = picture
        self.ingredients = ingredients
        self.geolocation = geolocation
        self.tags = tags
        self.directions = directions
        self.ratings = ratings
        self.recipe_id = recipe_id
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = time.time()

    def as_json(self):
        return json.dumps(self.__dict__)
    



