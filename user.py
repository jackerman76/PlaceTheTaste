import time
from datetime import datetime

class User():
    def __init__(self, username, password, phone_number):
        self.username = str(username)
        self.password = str(password)
        self.phone_number = str(phone_number)
        self.timestamp = time.time()

    # def generate_random2fa_code(self)
        # implement

    # def send_log_2fa_sms(self, cde, to_phone)
        # implement

    #def validate_passwords(self):
        # implement
