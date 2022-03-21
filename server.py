from flask import Flask, request
from flask_classful import FlaskView, route
from firestoreio import FirestoreIO
from utils import *

HOST = "0.0.0.0"
PORT = 8000

AuthHolder() # Invoke this early just to avoid any possible race conditions
app = Flask(__name__)
ran_startup = False

class PTTRequests(FlaskView):
    route_base = "/"
    
    def __init__(self):
        self.__fsio = FirestoreIO()
        if ran_startup == False:
            self.print_startup() # Multiple instances of PTTRequests are started by Flask/Gunicorn, so this prevents spam.

    def print_startup(self):
        """
        Print server startup
        """
        info = InfoProvider()
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print(f"Starting {info.pretty_name} Server v{info.version}")
        print(f"License: {info.license}")
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        global ran_startup
        ran_startup = True

    @route('/ptt/api/login/check_username_exists', methods=['POST'])
    def check_username_exists(self):
        """
        Necessary Params in POST: "Username"
        """
        request_data = request.get_json()
        if request_data["Username"] != None:
            pass
            # Implement this functionality

PTTRequests.register(app)
