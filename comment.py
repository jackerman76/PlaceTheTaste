import time
from datetime import datetime


class Comment:

    def __init__(self, username, message, recipe_id):
        self.username = username
        self.message = message
        self.recipe_id = recipe_id;
        self.timestamp = time.time()

    def get_formatted_time(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%m-%d-%Y %I:%M:%S %p")

    def write_comment(self, message):
        self.message = message
