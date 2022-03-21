from flask import Flask, request
from flask_classful import FlaskView, route
from firestoreio import FirestoreIO
from utils import *

HOST = "0.0.0.0"
PORT = 8000

AuthHolder() # Invoke this early just to avoid any possible race conditions
app = Flask(__name__)
ran_startup = False

def print_startup():
    """
    Print server startup
    """
    info = InfoProvider()
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print(f"Starting {info.pretty_name} Server v{info.version}")
    print(f"License: {info.license}")
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    ran_startup = True

class PTTRequests(FlaskView):
    route_base = "/"
    
    def __init__(self):
        self.__fsio = FirestoreIO()
        if ran_startup == False:
            print_startup() # Multiple instances of PTTRequests are started by Flask/Gunicorn, so this prevents spam.

    @route('/ptt/api/login/check_username_exists', methods=['POST'])
    def check_username_exists(self):
        """
        Necessary Params in POST: "Username"
        """
        request_data = request.get_json()
        if request_data["Username"] != None:
            pass
            # Implement this functionality