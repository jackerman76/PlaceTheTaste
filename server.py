import bcrypt
from flask import Flask, request, render_template, flash, session
from flask_classful import FlaskView, route
from firestoreio import FirestoreIO
from user import User
from comment import Comment
from utils import *
from recipe import Recipe
from flask_bcrypt import Bcrypt

HOST = "0.0.0.0"
PORT = 8000

AuthHolder()  # Invoke this early just to avoid any possible race conditions
app = Flask(__name__, static_folder='static')
# add secret key here using app.secret_key = INSERT_KEY_HERE for now until more permanent solution (if that is a thing)
app.secret_key = 'THIS_IS_SUPER_SECRET_GUYS_REALLY_HUSH_STUFF'
bcrypt = Bcrypt(app)
ran_startup = False


class PTTRequests(FlaskView):
    route_base = "/"

    def __init__(self):
        self.__fsio = FirestoreIO()
        if ran_startup == False:
            self.print_startup()  # Multiple instances of PTTRequests are started by Flask/Gunicorn, so this prevents spam.

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
    @route('/view_map', methods=["GET", "POST"])
    def view_map(self):
        return render_template("view_map.html")

    @route('/create_account', methods=["GET", "POST"])
    def create_account(self):
        if request.method == "POST":
            username = request.values.get("username")
            phone_number = request.values.get("phone")
            password = request.values.get("password")
            password2 = request.values.get("password2")
            if password == password2:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf_8')  # hashed pw converted to str
                user = User(username, hashed_password, phone_number)
                session['username'] = username

                flash("Account Created!")  # temporary notification to let user know info was taken

        # print(username + " " + hashed_password + " " + phone_number)

        return render_template("create_account.html")

    @route('/login', methods=["GET", "POST"])
    def login(self):
        return render_template("login.html")

    @route('/view_recipe', methods=["GET", "POST"])
    def view_recipe(self):
        if request.method == "POST":
            commenter_name = request.values.get("commenter_name") # TODO: Replace with Session username

            commenter_ratings = request.values.get("rating1")
            comment_text = request.values.get("comment")

            #  for testing purposes
            recipe = Recipe()
            # TEMPORARY RECIPE ID  (change later to be id from database)
            recipe.recipe_name = "crepe";
            recipe.ingredients = "1 cup flour 1 cup milk"
            recipe.directions = "mix then cook"
            recipe.recipe_id = 99
            

            if(commenter_ratings):
                recipe.ratings = commenter_ratings #  TODO: incorrect impl for now
                
            comment = Comment(commenter_name, comment_text, recipe.recipe_id)

        return render_template("view_recipe.html")


PTTRequests.register(app)
