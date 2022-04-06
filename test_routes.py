from flask import Flask, request, redirect, render_template, url_for, jsonify, session, flash
from user import User
from comment import Comment
from __main__ import app

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route('/create_account', methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.values.get("username")
        password = request.values.get("password")
        password2 = request.values.get("password2")
        phone_number = request.values.get("phone")
        if (password == password2):
            user = User(username, password, phone_number)
            flash("Account Created!") # temporary notification to let user know info was taken

        # Note this is a naive implementation, password stuff needs overhaul still

        # print(email + " " + password + " " + phone_number)

    return render_template("create_account.html")

@app.route('/post_comment', methods=["GET", "POST"])
def post_comment():
    if request.method == "POST":
        message = request.values.get("message")
        #Need to connect to firestore to get actual username
        comment = Comment(username="Anon_for_now", message=message)

    return render_template("post_comment.html")

@app.route('/post_recipe', methods=["GET", "POST"])
def post_recipe():
    return render_template("post_recipe.html")

@app.route('/view_recipe', methods=["GET", "POST"])
def view_recipe():
    return render_template("view_recipe.html")