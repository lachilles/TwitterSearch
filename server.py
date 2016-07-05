"""Twitter search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
from sqlalchemy import func
# from model import KeywordMap, Tweet, TwitterUser, connect_to_db
from api import get_tweets_by_api
import unicodedata
import moment
import time
import re
from collections import Counter
# import random

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage showing a search form"""

    default_term = 'brexit'
    tweets = get_tweets_by_api(term=default_term)

    result = []

    for tweet in tweets:
        #exclude retweets
        if tweet.retweeted_status is None:
            # Convert tweet text from unicode to text
            tweet_id = tweet.id
            text = unicodedata.normalize('NFKD', tweet.text).encode('ascii', 'ignore')
            # Find URL in text and bind to url
            # url = re.search('((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))', text)
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            # Remove URL from text
            text_wo_url = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
            # Handle / Name
            user = unicodedata.normalize('NFKD', tweet.user.screen_name).encode('ascii', 'ignore')
            # Count of favorites
            favorite_count = tweet.favorite_count
            #Return dictionary of hashtags with hashtag as key and number of occurances as value
            if tweet.hashtags:
                # Convert hashtags from unicode to string
                ht_list = []
                for hashtag in tweet.hashtags:
                    ht_str = unicodedata.normalize('NFKD', hashtag.text).encode('ascii', 'ignore')
                    ht_list.append(ht_str)
                hashtags = Counter(ht_list)
            else:
                hashtags = tweet.hashtags
            # Convert tweet from unicode to datetime
            created_at = tweet.created_at
            # format created_at string to ISO 8610
            created_at_str = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))
            # create a moment from the string
            created_at = moment.date(created_at_str, 'YYYY-MM-DD HH:mm:ss')
            result.append({'created_at': created_at_str, 'text': text_wo_url, 'user': user,
                           'favorite_count': favorite_count, 'hashtags': hashtags,
                           'url': url, 'tweet_id': tweet_id})
    #sort dictionary by created_at
    sorted_result = sorted(result, key=lambda k: k['created_at'])
    print "&&&&&&&&&&&&&&&&&&&&&&&&&"
    print sorted_result
    print "&&&&&&&&&&&&&&&&&&&&&&&&&"
    tweets = json.dumps(sorted_result)
    print tweets

    return render_template("index.html", tweets=tweets)


@app.route("/trending")
def add_trending():
    """Add a trending keyword to our database."""
    keyword = request.args.get('search').lower()
    # add a keyword to our KeywordMap here

    print "\n\nTRENDING: %s\n\n" % (keyword)


@app.route('/search-results.json/<keyword>')
def search_results(keyword):
    """Search Twitter and return a dictionary of results."""

    keyword = request.args.get('search').lower()

    tweets = get_tweets_by_api(term=keyword)

    result = []

    for tweet in tweets:
        #exclude retweets
        if tweet.retweeted_status is None:
            # Convert tweet text from unicode to text
            tweet_id = tweet.id
            text = unicodedata.normalize('NFKD', tweet.text).encode('ascii', 'ignore')
            # Find URL in text and bind to url
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            # Remove URL from text
            text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
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
            result.append({'created_at': created_at_str, 'text': text, 'user': user,
                           'favorite_count': favorite_count, 'hashtags': hashtags,
                           'url': url, 'tweet_id': tweet_id})
    #sort dictionary by datetime
    sorted_result = sorted(result, key=lambda k: k['created_at'])
    tweets = json.dump(sorted_result)
    print tweets
    return tweets


"""Provide feedback to user on whether if ticker is valid"""

if __name__ == "__main__":
# We have to set debug=True here, since it has to be True at the point
# that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbars
    DebugToolbarExtension(app)

    app.run()
