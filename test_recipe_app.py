import datetime
from flask import Flask, request, redirect, render_template, url_for, jsonify, session
import requests
import json
from recipe import Recipe

app = Flask(__name__)




@app.route('/post_recipe', methods=["GET", "POST"])
def post_recipe():
    return (render_template("post_recipe.html"))


@app.route('/view_recipe', methods=["GET", "POST"])
def view_recipe():
    # test visualizing a recipe
    recipe = Recipe(
        picture="https://www.abakingjourney.com/wp-content/uploads/2020/04/French-Crepes-feature.jpg",
        recipe_name="Basic crepes",
        ingredients="1 cup flour\n1 cup milk\n1 egg\n".replace("\n", "<br>"),
        directions="add all the stuff together and then cook em up"
    )
    return (render_template("view_recipe.html", recipe=recipe))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)