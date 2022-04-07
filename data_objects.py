import uuid
from firestoreio import FirestoreIO

class Recipe:

    def __init__(self, username=None, recipe_name=None, picture=None, ingredients=None, geolocation=None, tags=None, directions=None, recipe_id=None, timestamp=None, location_description=None, ratings=None, rating_num=None, comment_ids=None):
        """
        Recipe data shuffler object by Noah Martino
        This object can be used to read/write recipe data as an object from the Firestore.
        If you just provide a recipe ID we will initialize the object for you.
        
        OPTIONAL constructor values:
        :param str username:
        :param str recipe_name:
        :param str picture: Link to picture
        :param str ingredients: List of ingredients 
        :param str geolocation: Geolocation
        :param list tags: List of string format tags
        :param str directions: Directions for the recipe
        :param str recipe_id: UUID recipe ID. If you want to pull a recipe from DB, init with this, or pass it in when calling init_recipe_by_id()
        :param str timestamp:
        :param str location_description: City, Province, Country, etc.
        :param list ratings: List of integers, ex [3, 5, 4, 1, 3, 2] a list of ratings. You normally wouldn't pass this in. To add a rating, init_recipe_by_id() and then use the add_rating() method.
        :param int rating_num: Number of ratings
        :param list comment_ids: List of the comment_ids that correspond to this recipe. A set of UUIDs for comments formatted as strings which can be used with the Comment object
        """
        self.username = username
        self.recipe_name = recipe_name
        self.picture = picture
        self.ingredients = ingredients
        self.geolocation = geolocation
        self.tags = tags
        self.directions = directions
        self.recipe_id = recipe_id
        self.timestamp = timestamp
        self.location_description = location_description
        self.ratings = ratings
        self.rating_num = rating_num
        self.comment_ids = comment_ids
        self.__r_dict = {}
        self.__is_instantiated = False
        self.get_dict_from_obj() # This will set self.__r_dict one line above to the values from the object 
        self.__check_minimum_data_populated() # This will decide whether the object is write-able
        # See if user just added a recipe_id and auto-populate the rest
        if self.__is_instantiated == False and self.recipe_id != None:
            i = self.init_recipe_by_id(self.recipe_id)
        self.__fsio = FirestoreIO()
        self.__COLLECTION_BASE = "/Recipe/"

    def __check_minimum_data_populated(self):
        self.get_dict_from_obj()
        for key in self.__r_dict:
            if key != "comment_ids" and key != "rating_num" and key != "ratings": #These are not required to set up a recipe for the first time so can afford to be blank
                if self.__r_dict[key] == None:
                    self.__is_instantiated = False
                    return
        self.__is_instantiated = True
        return

    def diag_print_fields(self):
        """
        Diagnostic function to print the data in the object's dictionary
        """
        self.get_dict_from_obj()
        print(self.__r_dict)

    def add_rating(self, rating_int, recipe_id=None):
        """
        If the object has all of the necessary data instantiated, will add a rating
        Will try to instantiate the object if it has not been and if a recipe_id has been provided either via the constructor or via the optional argument in this method
        THIS WILL WRITE TO DATABASE!

        :param int rating_int: 1-5 stars
        :param str recipe_id: OPTIONAL recipe_id if you haven't instantiated the object already.

        :returns True: Successful write
        :returns False: Error
        """
        if type(rating_int) != int:
            print(f"Type of rating_int was not int, instead was {type(rating_int)}")
            return
        if self.__is_instantiated == True:
            if self.ratings == None:
                self.ratings = []
            self.ratings.append(rating_int)
        else:                               
            # This case exists for someone who made a recipe object and didn't pass anything to c'tor, but passed recipe_id to this method.
            if recipe_id != None:
                r = self.init_recipe_by_id(recipe_id)
                if r == True:
                    if self.ratings == None:
                        self.ratings = []
                    self.ratings.append(rating_int)
                else:
                    print("Unknown error occured trying to init recipe object to add rating")
                    return False
            else:
                print("No recipe ID found in recipe object or provided when you called this method. Unable to continue.")
                return False
        w_res = self.write_recipe()
        return w_res

    def add_comment(self, comment_id, recipe_id=None):
        """
        If the object has all of the necessary data instantiated, will add a comment ID to the list
        Will try to instantiate the object if it has not been and if a recipe_id has been provided either via the constructor or via the optional argument in this method
        THIS WILL WRITE TO DATABASE!

        :param str commend_id: UUID of a comment in the DB
        :param str recipe_id: OPTIONAL recipe_id if you haven't instantiated the object already.
        """
        if self.__is_instantiated == True:
            if self.comment_ids == None:
                self.comment_ids == []
            self.comment_ids.append(comment_id)
        else:
            if recipe_id != None:
                r = self.init_recipe_by_id(recipe_id)
                if r ==True:
                    if self.comment_ids == None:
                        self.comment_ids = []
                    self.commend_ids.append(comment_id)
                else:
                    print("Unknown error occured trying to instantiate recipe from recipe_id given for this function")
                    return False
            else:
                print("You did not provide a recipe_id for this functionl call and none was provided in c'tor.")
                return False
        w_res = self.write_recipe()
        return w_res

    def gen_new_recipe_uuid(self):
        """
        Generate a random UUID4 for the object and set the object's recipe_id variable to it
    
        :returns str recipe_id: Also returns the recipe ID if you want it.
        """
        rid = str(uuid.uuid4())
        self.recipe_id = rid
        self.__check_minimum_data_populated()
        return self.recipe_id

    def get_dict_from_obj(self):
        """
        Returns a dictionary suitable to write as a doc using firestoreio's write_doc()
        Also sets objects internal __r_dict object which is used to write to database this dict
        """
        doc = {
            "username": self.username,
            "recipe_name": self.recipe_name,
            "picture": self.picture,
            "ingredients": self.ingredients,
            "geolocation": self.geolocation,
            "tags": self.tags,
            "directions": self.directions,
            "recipe_id": self.recipe_id,
            "timestamp": self.timestamp,
            "location_description": self.location_description,
            "ratings": self.ratings,
            "rating_num": self.rating_num,
            "comment_ids": self.comment_ids
        }
        self.__r_dict = doc
        return doc

    def init_recipe_by_id(self, recipe_id=None):
        """
        Init recipe object using the data already in Firestore

        :param str recipe_id: (Optional if you set this during construction) Recipe ID of extant recipe in database

        :returns: False if an error occured or if document does not exist
        :returns: True if success
        """
        if recipe_id != None:
            rid = recipe_id
        elif self.recipe_id != None:
            rid = self.recipe_id
        exists = self.__fsio.does_doc_exist(f"{self.__COLLECTION_BASE}{rid}")
        if exists is False or None:
            print(f"Recipe matching recipe ID '{rid}' does not seem to exist.")
            return False
        else:
            doc = self.__fsio.read_doc(f"{self.__COLLECTION_BASE}{rid}")
            if doc == None:
                print("An unknown error occured reading recipe from the database. Please check the console log for errors.")
                return False
            else:
                try:
                    self.username = doc["username"]
                    self.recipe_name = doc["recipe_name"]
                    self.picture = doc["picture"]
                    self.ingredients = doc["ingredients"]
                    self.geolocation = doc["geolocation"]
                    self.tags = doc["tags"]
                    self.directions = doc["directions"]
                    self.recipe_id = doc["recipe_id"]
                    self.timestamp = doc["timestamp"]
                    self.location_description = doc["location_description"]
                    self.ratings = doc["ratings"]
                    self.rating_num = doc["rating_num"]
                    self.comment_ids = doc["comment_ids"]
                    self.get_dict_from_obj() # Populate self.__r_dict
                    self.__check_minimum_data_populated() # Update self.__is_instantiated
                    return True
                except Exception as e:
                    print("An error (likely a missing key in Firestore) occured assigning document keys to object variables:", e)
                    return False

    def write_recipe(self):
        """
        Write a recipe object to the firestore as a document. Uses the object's variables to construct the dictionary
        Checks that none of the keys are NoneType, will error out and return False if this is the case
        Checks that tags are of type list, will error out and return False if this is the case
        Will also return false if an unknown error occurs during the write.

        :returns: True if success
        :returns: False if missing value/incorrect type() of value or if write error
        """
        if self.__is_instantiated == False or self.recipe_id == None:
            print("Error: The object lacks sufficient fields to write to DB")
            return False
        else:
            self.get_dict_from_obj() # Make absolutely 100% sure that the dictionary is up to date with any actions performed on class variables
            w_doc = self.__r_dict
            if type(w_doc["tags"]) != list:
                print(f"Unable to write recipe. Field 'tags' is not type 'list', instead type '{type(w_doc['tags'])}'")
                return False
            w_res = self.__fsio.write_doc(f"{self.__COLLECTION_BASE}{self.recipe_id}", w_doc)
            if w_res == False or w_res == None:
                print("An unknown error occured writing this recipe to firestore. Please check the console")
                return False
            else:
                return True