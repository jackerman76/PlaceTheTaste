import bcrypt
from flask import Flask, request, render_template, flash, session, redirect, url_for
from flask_classful import FlaskView, route
from firestoreio import FirestoreIO
from user import User
from comment import Comment
from utils import *
from data_objects import Recipe
from flask_bcrypt import Bcrypt
import uuid
import time
from google.cloud import storage

HOST = "0.0.0.0"
PORT = 8000

AuthHolder()  # Invoke this early just to avoid any possible race conditions
app = Flask(__name__, static_folder='static')
# add secret key here using app.secret_key = INSERT_KEY_HERE for now until more permanent solution (if that is a thing)

bcrypt = Bcrypt(app)
ran_startup = False

_BUCKET_NAME = "recipe-images"




def get_test_recipes():
    """Returns a list of test recipes for testing purposes"""
    recipes = []

    recipe1 = Recipe()
    recipe1.recipe_name = "Roasted Chicken"
    recipe1.recipe_id = str(uuid.uuid4())
    recipe1.ingredients = "1. 1 whole chicken\r\n2. 2 t poultry seasoning\r\n3. 1 T butter (melted)\r\n4. 1 t salt"
    recipe1.directions = "1. Mix ingredients 2-4\r\n2. Rub ingredients on chicken\r\n3. Bake at 280 F for 2.5-3 hours"
    recipe1.geolocation = "[40.44062479999999, -79.9958864]"
    recipe1.location_description = "5165 Grant St, Pittsburgh, PA 15129, US"
    recipe1.username = "joshackerman"
    recipe1.timestamp = 1649165332.34273
    recipe1.picture = "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F43%2F2022%2F01%2F19%2F83557-juicy-roast-chicken-mfs495-1.jpg"

    recipe2 = Recipe()
    recipe2.recipe_name = "Slow Roasted Carrots"
    recipe2.recipe_id = str(uuid.uuid4())
    recipe2.ingredients = "1. 1 lb carrots\r\n2. 2 t garlic\r\n3. 1 T butter (melted)\r\n4. 1 t salt"
    recipe2.directions = "1. Mix ingredients 2-4\r\n2. Bake at 300 F for 60 - 90 minutes"
    recipe2.geolocation = "[40.3765791,-80.0858934]"
    recipe2.location_description = "200 Adams Ave, Pittsburgh, PA, 15243, US"
    recipe2.username = "johndoe"
    recipe2.timestamp = 1649165300.34273
    recipe2.picture = "https://www.spendwithpennies.com/wp-content/uploads/2018/10/Spend-With-Pennies-Roasted-Carrots-25.jpg"

    recipes.append(recipe1)
    recipes.append(recipe2)

    return recipes


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
        if not session.get('username'):
            return redirect(url_for('PTTRequests:login'))
        if request.method == 'POST':
            if request.form.get("submit_recipe") == "True":
                # create recipe object

                # get form fields
                recipe_name = request.values.get('recipe_name')
                ingredients = request.values.get('ingredients')
                directions = request.values.get('directions')

                # Assign a unique recipe id to this recipe
                recipe_id = str(uuid.uuid4())

                # file handling
                # uploaded_file = request.files['recipe_image']
                # file_name = uploaded_file.filename or "image_upload"
                # file_name += session["username"] + "-" + str(time.time())

                print(session["username"])

                # UPload file to filestore
                """
                gcs_client = storage.Client()
                storage_bucket = gcs_client.get_bucket(_BUCKET_NAME)
                blob = storage_bucket.blob(file_name)
                c_type = uploaded_file.content_type
                blob.upload_from_string(uploaded_file.read(), content_type=c_type)

                recipe.picture = blob.public_url
                """
                # location input using google maps api
                latitude = float(request.values.get("loc_lat"))
                longitude = float(request.values.get("loc_long"))
                geolocation = str([latitude, longitude])
                location_description = request.values.get("recipe_location")

                # for test purposes
                # recipe.username = "JoshAckerman"
                # comment this when enabling filestore
                picture = "https://hips.hearstapps.com/hmg-prod/images/delish-basic-crepes-horizontal-1545245797.jpg"
                # print out recipe
                # print(recipe.as_json())

                # no picture yet Add when filestore is setup
                recipe = Recipe(username=session.get('username'), recipe_name=recipe_name, picture=picture,
                                ingredients=ingredients, geolocation=geolocation, tags=["tag1", "tag2", "tag3"],
                                directions=directions, timestamp=str(time.time()),
                                location_description=location_description)
                id = recipe.gen_new_recipe_uuid()

                print(recipe.__dict__)
                recipes = [recipe]
                # add recipe to database and let user know if it failed
                if not recipe.write_recipe():
                    flash("Sorry, there was an error with posting your recipe to our server. Please try again.")
                    return render_template("post_recipe.html")

                return render_template("view_map.html", recipes=recipes)

                # varify validity of recipe

                # return view of published recipe
                return (render_template("view_recipe.html", recipe=recipe))

        return (render_template("post_recipe.html"))

    @route('/', methods=["GET", "POST"])
    @route('/view_map', methods=["GET", "POST"])
    def view_map(self):
        # list of recipes to be returned for map
        # TODO fetch recipes from database
        r = Recipe()
        rps = r.get_all_recipes()
        recipes = []
        for recipe in rps:
            r = Recipe()
            r.init_recipe_by_id(recipe['recipe_id'])
            recipes.append(r)


        #recipes = get_test_recipes()
        return render_template("view_map.html", recipes=recipes)

    @route('/create_account', methods=["GET", "POST"])
    def create_account(self):
        if request.method == "POST":
            username = request.values.get("username")
            phone_number = request.values.get("phone")
            password = request.values.get("password")
            password2 = request.values.get("password2")
            if password == password2:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf_8')  # hashed pw converted to str
                if self.__fsio.read_docs_by_query("/Users/", ["username", "==", username]):
                    flash("An account with that username already exists.")  # temporary behavior
                else:
                    user = User(username, hashed_password, phone_number)
                    session['username'] = username
                    ret = self.__fsio.write_doc("/Users/" + username, user.__dict__)
                    flash("Account Created!")  # Notification to let user know info was taken
                    return render_template("login.html")
                # print(ret)

        return render_template("create_account.html")

    @route('/login', methods=["GET", "POST"])
    def login(self):
        if session.get('username'):
            return redirect(url_for('PTTRequests:view_map_0'))
        if request.method == "POST":
            username = request.values.get("username")
            password = request.values.get("password")
            user_dict = self.__fsio.read_docs_by_query("/Users/", ["username", "==", username])
            if session.get('username'):
                flash("already logged in")
                return render_template("login.html")
            if user_dict != None:  # if dict exists
                if bcrypt.check_password_hash(user_dict[username]['password'], password):
                    session['username'] = username
                    return redirect(url_for('PTTRequests:view_map_0'))
                else:
                    flash("wrong password")
                    return render_template("login.html")
            else:
                flash("username does not exist")
                return render_template("login.html")

        return render_template("login.html")

    @route('/view_recipe', methods=["GET", "POST"])
    @route('/view_recipe/<requested_recipe_id>', methods=['GET', 'POST'])
    def view_recipe(self, requested_recipe_id=None):
        # print(requested_recipe_id)
        recipe = Recipe()
        if requested_recipe_id:
            # found_recipe = self.__fsio.read_docs_by_query("/Recipe/", ["recipe_id", "==", requested_recipe_id])
            found_recipe = recipe.init_recipe_by_id(requested_recipe_id)
            if found_recipe:
                # return render_template("view_map.html", recipes=found_recipe)
                return render_template("view_recipe.html", recipe=recipe)
        if request.method == "POST":

            commenter_name = request.values.get("commenter_name")  # TODO: Replace with Session username

            commenter_ratings = request.values.get("rating1")
            comment_text = request.values.get("comment")

            #  for testing purposes

            # TEMPORARY RECIPE ID  (change later to be id from database)
            recipe.recipe_name = "crepe"
            recipe.ingredients = "1 cup flour 1 cup milk"
            recipe.directions = "mix then cook"
            recipe.recipe_id = 99

            if commenter_ratings:
                recipe.add_rating(commenter_ratings)
            comment_id = str(uuid.uuid4())
            comment = Comment(commenter_name, comment_text, comment_id, recipe.recipe_id)
            if not self.__fsio.write_doc("/Comment/" + comment_id, comment.__dict__):
                flash("Comment could not be added. Please try again.")

        return render_template("view_recipe.html", recipe=recipe)

    @route('/logout')
    def logout(self):
        if session.get('username'):
            session.pop('username', default=None)
        else:
            flash("You are not logged in")
        return redirect(url_for('PTTRequests:view_map_0'))


PTTRequests.register(app)
