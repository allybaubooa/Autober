import flask
from flask import render_template, url_for
from app import flask_app


@flask_app.route("/")
def index():
    return "Hackathon2"


@flask_app.route("/homepage")
def index_homepage():
    return flask.render_template("base.html")


@flask_app.route("/profile")
def profile_page():
    return flask.render_template("profile.html")


@flask_app.route("/leaderboard")
def leaderboard_page():
    return flask.render_template("leaderboard.html")


@flask_app.route("/login")
def log_in_page():
    return flask.render_template("log-in.html")
