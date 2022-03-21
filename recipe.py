import time
from time import gmtime, strftime
from datetime import datetime
from geopy import distance
import json
from utils import *

class Recipe():
    def __init__(self, username, recipe_name, picture, ingredients, 
    geolocation, tags, directions, ratings, recipe_id, timestamp):
        self.username = username
        self.recipe_name = recipe_name
        self.picture = picture
        self.ingredients = ingredients
        self.geolocation = geolocation
        self.tags = tags
        self.directions = directions
        self.ratings = ratings
        self.recipe_id = recipe_id
        self.timestamp = timestamp

    def as_json(self):
        return json.dumps(self.__dict__)
    



