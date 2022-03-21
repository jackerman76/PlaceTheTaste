import datetime
from flask import Flask, request, redirect, render_template, url_for, jsonify, session
import requests
import json

app = Flask(__name__)




@app.route('/post_recipe', methods=["GET", "POST"])
def post_recipe():
    return (render_template("post_recipe.html"))



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)