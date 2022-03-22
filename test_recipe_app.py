import datetime
from flask import Flask, request, redirect, render_template, url_for, jsonify, session
import requests
import json
from recipe import Recipe

app = Flask(__name__)




@app.route('/post_recipe', methods=["GET", "POST"])
def post_recipe():
    if request.method == 'POST':
        if request.form.get("submit_recipe") == "True":
            recipe_name = request.values.get('recipe_name')
            ingredients = request.values.get('ingredients')
            directions = request.values.get('directions')
            picture = request.values.get('file')

        recipe = Recipe(
            picture="https://www.abakingjourney.com/wp-content/uploads/2020/04/French-Crepes-feature.jpg",
            recipe_name=recipe_name,
            ingredients=ingredients,
            directions=directions
        )

        return (render_template("view_recipe.html", recipe=recipe))

    return (render_template("post_recipe.html"))


@app.route('/view_recipe', methods=["GET", "POST"])
def view_recipe():
    # test visualizing a recipe
    recipe = Recipe(
        picture="https://www.abakingjourney.com/wp-content/uploads/2020/04/French-Crepes-feature.jpg",
        recipe_name="Basic crepes",
        ingredients="1 cup flour 1 cup milk 1 egg",
        directions="add all the stuff together and then cook em up"
    )
    return (render_template("view_recipe.html", recipe=recipe))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)