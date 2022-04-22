import pytest
from data_objects import Recipe
from comment import Comment
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
    tags = ["testtag1", "testtag2"]
    directions = "expose bread to heat source until toasted to desired doneness"
    timestamp = "1650256095.555848"
    location_description = "the cold plains of antarctica"
    recipe = Recipe(username=username, recipe_name=recipe_name, picture=picture, ingredients=ingredients, tags=tags, directions=directions, timestamp=timestamp, location_description=location_description)
    return recipe

@pytest.fixture
def get_test_recipes():
    """Returns a list of test recipes for testing purposes"""
    recipes = []
    recipe1 = Recipe()
    recipe1.recipe_name = "Roasted Chicken"
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

class TestRecipe:
    def test_basic_object_init(self, new_recipe_recipe):
        assert new_recipe_recipe.username == "exampleuser"
        assert new_recipe_recipe.recipe_name == "Toast"
        assert new_recipe_recipe.picture == "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/ToastedWhiteBread.jpg/800px-ToastedWhiteBread.jpg"
        assert new_recipe_recipe.ingredients == "1 slice of bread"
        assert new_recipe_recipe.tags == ["testtag1", "testtag2"]
        assert new_recipe_recipe.directions == "expose bread to heat source until toasted to desired doneness"
        assert new_recipe_recipe.timestamp == "1650256095.555848"
        assert new_recipe_recipe.location_description == "the cold plains of antarctica"

    def test_basic_db_read(self, recipe_id_recipe):
        d = recipe_id_recipe.get_dict_from_obj()
        assert d["geolocation"] == str([37.9767725, 23.7440562])
        assert d["location_description"] == "Loukianou 12, Athina 106 75, Greece"
        assert d["recipe_id"] == "fba1f6f8-7c8b-45b2-8b52-aa2ecf188b51"
        assert d["recipe_name"] == "Greek Einkorn (Wheat Berry) Salad"

    def test_get_all_recipes(self, blank_recipe):
        recipes = blank_recipe.get_all_recipes()
        assert type(recipes) == list
        assert len(recipes) > 0
        assert type(recipes[0]) == Recipe
        assert type(recipes[len(recipes)-1]) == Recipe

    def test_get_all_comments(self, recipe_id_recipe):
        comments = recipe_id_recipe.get_all_comments()
        assert (type(comments) == None or type(comments) == list) == True

    def test_get_recipes_by_tags(self, blank_recipe):
        tag_list = ["Baked", "Vegan"]
        recipes = blank_recipe.get_recipes_by_tags(tag_list)
        assert type(recipes) == list
        assert len(recipes) > 0
        assert type(recipes[0]) == Recipe
        assert "Baked" in recipes[0].tags
        assert "Vegan" in recipes[0].tags