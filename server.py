import bcrypt
from flask import Flask, request, render_template, flash, session, redirect, url_for
from flask_classful import FlaskView, route
from firestoreio import FirestoreIO
from user import User
from comment import Comment
from utils import *
from data_objects import Recipe
from flask_bcrypt import Bcrypt
from sms_handler import TwoFactorAuthManager
import uuid
import time

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
    #recipe1.recipe_id = str(uuid.uuid4()) replace with object builtin below
    recipe1.gen_new_recipe_uuid()
    recipe1.ingredients = "1. 1 whole chicken\r\n2. 2 t poultry seasoning\r\n3. 1 T butter (melted)\r\n4. 1 t salt"
    recipe1.directions = "1. Mix ingredients 2-4\r\n2. Rub ingredients on chicken\r\n3. Bake at 280 F for 2.5-3 hours"
    recipe1.geolocation = "[40.44062479999999, -79.9958864]"
    recipe1.location_description = "5165 Grant St, Pittsburgh, PA 15129, US"
    recipe1.username = "joshackerman"
    recipe1.timestamp = 1649165332.34273
    recipe1.picture = "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F43%2F2022%2F01%2F19%2F83557-juicy-roast-chicken-mfs495-1.jpg"
    recipe2 = Recipe()
    recipe2.recipe_name = "Slow Roasted Carrots"
    #recipe2.recipe_id = str(uuid.uuid4()) replace with object builtin below
    recipe2.gen_new_recipe_uuid()
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

    @route('/post_recipe', methods=["GET", "POST"])
    def post_recipe(self):
        if not session.get('username') or not session.get('authenticated'):
            flash("You are not logged in")
            return redirect(url_for('PTTRequests:login', enter_code=False))

        if request.method == 'POST':
            if request.form.get("submit_recipe") == "True":

                # get form fields
                recipe_name = request.values.get('recipe_name')
                ingredients = request.values.get('ingredients')
                directions = request.values.get('directions')

                # Upload file to filestore
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
                # picture = "https://hips.hearstapps.com/hmg-prod/images/delish-basic-crepes-horizontal-1545245797.jpg"

                # Store picture
                picture = request.values.get("img_string")
                picture = "data:image/png;base64, " + picture

                # Get recipe tags
                tags = request.values.getlist('recipe-tag')

                recipe = Recipe(username=session.get('username'), recipe_name=recipe_name, picture=picture,
                                ingredients=ingredients, geolocation=geolocation, tags=tags,
                                directions=directions, timestamp=str(time.time()),
                                location_description=location_description)
                recipes = [recipe]
                # Generate a unique id before storing the recipe
                recipe.gen_new_recipe_uuid()

                # add recipe to database and let user know if it failed
                if not recipe.write_recipe():
                    flash("Sorry, there was an error with posting your recipe to our server. Please try again.")
                    return render_template("post_recipe.html", username=session.get('username'))

                return render_template("view_map.html", recipes=recipes, username=session.get('username'), filtered=False)

        return render_template("post_recipe.html", username=session.get('username'))

    @route('/', methods=["GET", "POST"])
    @route('/view_map', methods=["GET", "POST"])
    def view_map(self):
        # Determine the list of recipes to be returned for the map
        r = Recipe()
        filtered = False  # Flag to tell whether recipes were filtered or not
        if request.method == "POST":
            tags = request.values.getlist('recipe-tag')
            if len(tags) == 0:
                flash("Please select at least one tag to filter.")
                return redirect(url_for('PTTRequests:view_map_0'))
            else:
                filtered = True
                recipes = r.get_recipes_by_tags(tags)
        else:
            recipes = r.get_all_recipes()
            # recipes = get_test_recipes()  # when reloading the page a lot for testing, use this instead
        return render_template("view_map.html", recipes=recipes, username=session.get('username'), filtered=filtered)

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
                    flash("An account with that username already exists.")
                    redirect(url_for("PTTRequests:login"))
                else:
                    user = User(username, hashed_password, phone_number)
                    if self.__fsio.write_doc("/Users/" + username, user.__dict__):
                        # tfa = TwoFactorAuthManager(username)
                        # # Checking if TFA is functional! (this tells u if the user exists and u can continue)
                        #
                        # if tfa.functional:
                        #     # First,  lets generate a new 2fa code for this user
                        # tfa.init_new_2fa_code()  # This will make a code, log it and the fact that it hasn't
                        # been used yet to the user in DB, then text the user the code

                        return redirect(url_for('PTTRequests:login'))
                    else:
                        flash("Sorry, there was some trouble with our servers, account could not be created. Please "
                              "try again later.")
                        return redirect(url_for("PTTRequests:create_account"))

        return render_template("create_account.html", username=session.get('username'))

    @route('/login', methods=["GET", "POST"])
    def login(self):
        if request.method == "POST":
            if 'password' in request.form:
                if session.get('username'):
                    return redirect(url_for('PTTRequests:view_map_0', username=session.get('username')))
                username = request.values.get("username")
                password = request.values.get("password")
                user_dict = self.__fsio.read_docs_by_query("/Users/", ["username", "==", username])

                if user_dict is not None:  # if dict exists
                    if bcrypt.check_password_hash(user_dict[username]['password'], password):
                        session['username'] = username
                        tfa = TwoFactorAuthManager(session.get('username'))
                        tfa.init_new_2fa_code()  # generate new 2fa code and sms it to the user
                        session['authenticated'] = False
                        # return redirect(url_for('PTTRequests:view_map_0', username=username, filtered=False))
                        return render_template("login.html", username=session.get('username'), enter_code=True)
                    else:
                        flash("wrong password")
                        return render_template("login.html", username=session.get('username'))
                else:
                    flash("username does not exist")
                    return render_template("login.html", username=session.get('username'))
            elif '2fa_code' in request.form:
                # # Check to see if the user got the right twilio code
                tfa = TwoFactorAuthManager(session.get('username'))
                user_entered_2fa = request.values.get('2fa_code')
                code_valid = tfa.validate_2fa_code(user_entered_2fa)
                if code_valid:
                    print("Code Is Valid")
                    session['authenticated'] = True
                    return redirect(url_for('PTTRequests:view_map_0', username=session.get('username'), filtered=False))
                else:
                    print("Code is invalid")
                    flash("Two factor authentication failed")
                    return redirect(url_for('PTTRequests:login', username=session.get('username'), enter_code=True))
        return render_template("login.html", username=session.get('username'), enter_code=False)

    @route('/view_recipe', methods=["GET", "POST"])
    @route('/view_recipe/<requested_recipe_id>', methods=['GET', 'POST'])
    def view_recipe(self, requested_recipe_id=None):
        recipe = Recipe()

        if requested_recipe_id:
            found_recipe = recipe.init_recipe_by_id(requested_recipe_id)
            if found_recipe:
                if request.method == "POST":
                    print(session.get('authenticated'))
                    if not session.get('username') or session.get('authenticated') != True:
                        flash("Please Login to Comment")
                        return redirect(url_for('PTTRequests:login'))
                    else:
                        commenter_name = session.get('username')

                    ratings = request.values.get("rating")

                    comment_text = request.values.get("comment")

                    if ratings:
                        recipe.add_rating(int(ratings))
                    if comment_text:
                        comment_id = str(uuid.uuid4())
                        comment = Comment(commenter_name, comment_text, comment_id, recipe.recipe_id)
                        if not self.__fsio.write_doc("/Comment/" + comment_id, comment.__dict__):
                            flash("Comment could not be added. Please try again.")
                        recipe.add_comment(comment_id)

                # get list of comments from firestore
                self.__fsio.read_docs_by_query("/Comment/", ["recipe_id", "==", recipe.recipe_id])
                return render_template("view_recipe.html", recipe=recipe, comments=recipe.get_all_comments(),
                                       username=session.get('username'))

        return render_template("view_recipe.html", username=session.get('username'))

    @route('/logout')
    def logout(self):
        if session.get('username'):
            session.pop('username', default=None)
        else:
            flash("You are not logged in")
        return redirect(url_for('PTTRequests:login'))


PTTRequests.register(app)
