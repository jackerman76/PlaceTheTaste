from flask import Flask, request, render_template, flash
from flask_classful import FlaskView, route
from firestoreio import FirestoreIO
from user import User
from comment import Comment
from utils import *
from recipe import Recipe

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
        print(f"Team Members: {info.authors}")
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

    @route('/post_recipe', methods=["GET", "POST"])
    def post_recipe(self):
        if request.method == 'POST':
            if request.form.get("submit_recipe") == "True":
                # create recipe object
                recipe = Recipe()
                # get form fields
                recipe.recipe_name = request.values.get('recipe_name')
                recipe.ingredients = request.values.get('ingredients')
                recipe.directions = request.values.get('directions')
                recipe.picture = request.values.get('file')

                # add recipe to database

                # varify validity of recipe
                

                # return view of published recipe
                return (render_template("view_recipe.html", recipe=recipe))

        return (render_template("post_recipe.html"))

    @route('/', methods=["GET", "POST"])
    @route('/home', methods=["GET", "POST"])
    def home(self):
        return render_template("home.html")

    @route('/create_account', methods=["GET", "POST"])
    def create_account(self):
        if request.method == "POST":
            username = request.values.get("username")
            password = request.values.get("password")
            password2 = request.values.get("password2")
            phone_number = request.values.get("phone")
            if (password == password2):
                user = User(username, password, phone_number)
                flash("Account Created!")  # temporary notification to let user know info was taken

            # Note this is a naive implementation, password stuff needs overhaul still

            # print(email + " " + password + " " + phone_number)

        return render_template("create_account.html")

    @route('/post_comment', methods=["GET", "POST"])
    def post_comment(self):
        if request.method == "POST":
            message = request.values.get("message")
            # Need to connect to firestore to get actual username
            comment = Comment(username="Anon_for_now", message=message)

        return render_template("post_comment.html")

PTTRequests.register(app)