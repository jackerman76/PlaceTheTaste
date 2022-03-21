import time
from datetime import  datetime
class Comment():

    def __init__(self, username, message):
        self.username = username
        self.message = message

        self.timestamp = time.time()


    def display_time(self):
        return datetime.fromtimestamp(self.timestamp)

    def write_comment(self, message):
        self.message = message
