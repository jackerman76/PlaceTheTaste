import time
from datetime import datetime
from tkinter import N


class Comment:

    def __init__(self, username=None, message=None, comment_id=None, recipe_id=None):
        self.username = username
        self.message = message
        self.comment_id = comment_id
        self.recipe_id = recipe_id
        self.timestamp = time.time()

    def get_formatted_time(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%m-%d-%Y %I:%M:%S %p")

    def get_time_delta(self):
        delta = datetime.now() - datetime.fromtimestamp(self.timestamp)
        if delta.days != 0:
            return str(int(delta.days)) + " days ago"

        if delta.seconds > 3600:
            return str(int(delta.seconds/3600)) + " hours ago"

        else:
            return str(int(delta.seconds/60)) + " minutes ago"

    def write_comment(self, message):
        self.message = message
