"""Twitter search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
from sqlalchemy import func
from model import KeywordMap, Tweet, TwitterUser, connect_to_db
import unicodedata
import moment
import time
import random

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage showing a search form"""

    keyword = request.args.get("search").lower()

    if keyword is None:
        flash("Search for anything you want"):

    tweets = 