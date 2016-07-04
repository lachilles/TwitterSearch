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

@app.route("/")
def index():
    """Homepage showing a search form"""
    # KEYWORD = request.args.get("search").lower()

    return render_template("index.html")


@app.route("/trending", methods=['POST'])
def add_trending():
    """Add a trending keyword to our database."""
    KEYWORD = request.form.get('search').lower()
    # add a keyword to our KeywordMap here

    print "\n\nTRENDING: %s\n\n" % (KEYWORD)


@app.route('/new-search', methods=['POST'])
def get_search_results():
    """Get Twitter search results"""
    KEYWORD = request.form.get('search').lower()

    print "\n\Search results: %s\n\n" % (KEYWORD)


@app.route('/search-results.json/')
def search_results():
    """Search Twitter and return a dictionary of results."""

    keyword = request.form.get('search').lower()
    tweets = keyword.get_tweets()

    result = []

    for tweet in tweets:
        #exclude retweets
        if tweet.retweeted_status is None:
            # Convert tweet text from unicode to text
            text = unicodedata.normalize('NFKD', tweet.text).encode('ascii', 'ignore')
            # Handle / Name
            user = unicodedata.normalize('NFKD', tweet.user.screen_name).encode('ascii', 'ignore')
            # Count of favorites
            favorite_count = unicodedata.normalize('NFKD', tweet.favorite_count).encode('ascii', 'ignore')
            # Hashtags
            hashtags = unicodedata.normalize('NFKD', tweet.hashtags).encode('ascii', 'ignore')
            # Convert tweet from unicode to datetime
            created_at = unicodedata.normalize('NFKD', tweet.created_at).encode('ascii', 'ignore')
            # format created_at string to ISO 8610
            created_at_str = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))
            # create a moment from the string
            created_at = moment.date(created_at_str, 'YYYY-MM-DD HH:mm:ss')
            result.append({'datetime': created_at_str, 'text': text, 'user': user,
                           'favorite_count': favorite_count, 'hashtags': hashtags})
    #sort dictionary by datetime
    sorted_result = sorted(result, key=lambda k: k['datetime'])
    tweets = json.dumps(sorted_result)

    return tweets


"""Provide feedback to user on whether if ticker is valid"""

if __name__ == "__main__":
# We have to set debug=True here, since it has to be True at the point
# that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbars
    DebugToolbarExtension(app)

    app.run()
