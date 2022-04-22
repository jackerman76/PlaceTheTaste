import pytest
from data_objects import Recipe
from firestoreio import FirestoreIO
import threading

@pytest.fixture
def fsio():
    fsio = FirestoreIO()
    return fsio

@pytest.fixture
def blank_recipe():
    recipe = Recipe()
    return recipe

@pytest.fixture
def recipe_id_recipe():
    recipe = Recipe()
    recipe.init_recipe_by_id("fba1f6f8-7c8b-45b2-8b52-aa2ecf188b51")
    return recipe

@pytest.fixture
def new_recipe_recipe():
    username = "exampleuser"
    recipe_name = "Toast"
    picture = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/ToastedWhiteBread.jpg/800px-ToastedWhiteBread.jpg"
    ingredients = "1 slice of bread"
    geolocation = ""
    tags = ["testtag1", "testtag2"]
    directions = "expose bread to heat source until toasted to desired doneness"
    timestamp = "1650256095.555848"
    location_description = "the cold plains of antarctica"
    recipe = Recipe(username=username, recipe_name=recipe_name, picture=picture, ingredients=ingredients, tags=tags, directions=directions, timestamp=timestamp, location_description=location_description)
    return recipe

class TestRecipe:
    def test_basic_db_read(self, recipe_id_recipe):
        d = recipe_id_recipe.get_dict_from_obj()
        assert d["geolocation"] == str([37.9767725, 23.7440562])
        assert d["location_description"] == "Loukianou 12, Athina 106 75, Greece"
        assert d["recipe_id"] == "fba1f6f8-7c8b-45b2-8b52-aa2ecf188b51"
        assert d["recipe_name"] == "Greek Einkorn (Wheat Berry) Salad"