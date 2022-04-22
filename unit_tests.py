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
    def test_basic_object_init(self, recipe_id_recipe):
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

    def test_get_formatted_time(self, recipe_id_recipe):
        time = str(recipe_id_recipe.get_formatted_time())
        assert time == "04-18-2022 01:31:01 AM"

    def test_has_geolocation(self, recipe_id_recipe):
        assert recipe_id_recipe.has_geolocation() == True

    def test_get_latitude(self, recipe_id_recipe):
        assert str(recipe_id_recipe.get_latitude()) == "37.9767725"

    def test_get_longitude(self, recipe_id_recipe):
        assert str(recipe_id_recipe.get_longitude()) == "23.7440562"

    def test_gen_new_recipe_uuid(self, get_test_recipes):
        assert get_test_recipes[0].gen_new_recipe_uuid() == get_test_recipes[0].recipe_id

    def test_write(self, recipe_id_recipe):
        assert recipe_id_recipe.write_recipe() == True

    def test_diag_print_fields(self, recipe_id_recipe):
        assert recipe_id_recipe.diag_print_fields() == True

    def test_add_rating(self, recipe_id_recipe):
        pre_count = recipe_id_recipe.rating_num
        pre_count_actual = len(recipe_id_recipe.ratings)
        assert pre_count == pre_count_actual
        recipe_id_recipe.add_rating(5)
        assert recipe_id_recipe.rating_num == (pre_count+1)
        assert len(recipe_id_recipe.ratings) == (pre_count+1)
        assert recipe_id_recipe.ratings[(pre_count_actual)] == 5
