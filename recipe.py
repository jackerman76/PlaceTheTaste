import time
from time import gmtime, strftime
from datetime import datetime
from geopy import distance
import json


# from utils import *

class Recipe:

    def __init__(self, username=None, recipe_name=None, picture=None, ingredients=None,
                 geolocation=None, tags=None, directions=None, ratings=None, recipe_id=None, timestamp=None):
        self.username = username
        self.recipe_name = recipe_name
        self.picture = picture
        self.ingredients = ingredients
        self.geolocation = geolocation
        self.tags = tags
        self.directions = directions
        self.__ratings = ratings
        self.__number_of_ratings = 0
        self.recipe_id = recipe_id
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = time.time()

    def as_json(self):
        return json.dumps(self.__dict__)

    def add_rating(self, rating):
        rating = int(rating)
        self.__number_of_ratings += 1
        if self.__ratings:
            self.__ratings += rating
        else:
            self.__ratings = rating

    def get_rating(self):
        return self.__ratings / self.__number_of_ratings

    def get_formatted_time(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%m-%d-%Y %I:%M:%S %p")
