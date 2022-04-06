import datetime
from flask import Flask, request, redirect, render_template, url_for, jsonify, session

from user import *
import time
import requests
import json

from utils import *

app = Flask(__name__, static_folder='branding')
import test_routes
app.secret_key = 'SECRET_KEY'
# _BUCKET_NAME = "banana-post-pictures"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

