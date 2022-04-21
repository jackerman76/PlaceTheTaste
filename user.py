import time
from datetime import datetime

class User():
    def __init__(self, username, password, phone_number):
        self.username = str(username)
        self.password = str(password)
        self.phone_number = str(phone_number)
        self.timestamp = time.time()

    def get_formatted_time(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%m-%d-%Y %I:%M:%S %p")

