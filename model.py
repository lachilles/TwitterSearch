"""Models and database functions for Udemy project"""

from datetime import datetime, timedelta, tzinfo
from pytz import timezone, utc

import requests

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from delorean import Delorean
from stemming.porter2 import stem

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class TwitterUser(db.Model):
    """Users who tweeted about a given query string"""

    __tablename__ = "users"

    user_id = db.Column(db.BigInteger, primary_key=True)
    user = user = db.Column(db.String(64), nullable=False)  #user.screen_name
    user_name = db.Column(db.String(60), nullable=False)  #user.name
    user_location = db.Column(db.String(160), nullable=True)
    follower_count = db.Column(db.Integer, nullable=True)
    tweet_count = db.Column(db.Integer, nullable=True)
    verified_status = db.Column(db.String(10), nullable=False)

    tweets = db.relationship('Tweet')

    def __repr__(self):
        """Represents user object"""

        return "<User ID: %d, Name: %s>" % (self.user_id, self.user, self.user_name)

    def as_dict(self):
        """Returns object in dictionary format"""

        data = {
            'name': self.user_name,
            'handle': self.user,
            'follower_count': self.follower_count,
            'user_id': self.user_id
        }

        return data


class Tweet(db.Model):
    "Tweets by query string"

    __tablename__ = "tweets"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tweet_id = db.Column(db.BigInteger, nullable=False)  #id
    tweet_id_str = db.Column(db.String(64), nullable=True) #id_str
    user_id = db.Column(db.BigInteger, db.ForecignKey("users.user_id"), nullable=False)
    user = db.Column(db.String(64), nullable=False)  #user.screen_name
    created_at = db.Column(db.DateTime, nullable=False)  #created_at
    text = db.Column(db.String(240), nullable=False)  #text
    retweet_count = db.Column(db.Integer, nullable=True)  #retweet_count
    favorite_count = db.Column(db.Integer, nullable=True) #favorite_count
    hashtags = db.Column(db.String(240), nullable=True)
    pulled_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('TwitterUser')
    keyword = db.relationship('Keyword')

    def __repr(self):
        """Represens tweet object"""

        return "<Tweet ID: %s, Keyword: %s>" % (self.tweet_id, self.keyword)

    def as_dict(self):
        """Returns dictionary format of tweet"""

        tweet = {
            'created_at': format_time(self.created_at),
            'user': self.user.screen_name,
            'user_id': self.user_id,
            'tweet_id': self.tweet_id,
            'text': self.text,
            'favorites': self.favorite_count,
            'retweet_count': self.retweet_count,
        }

        return tweet

    @classmethod
    def recent_tweets_by_keyword(cls, keyword, amount=15):
        """Returns the most recent tweets for a query string"""

        recent_tweets_list = cls.query.filter(cls.keyword == keyword).order_by(cls.created_at.desc()).limit(amount).all()

        recent_tweets = [tweet.as_dict() for tweet in recent_tweets_list]

        return recent_tweets

    @staticmethod
    def normalize_input(keyword):
        """Given a query string, searches tweets"""

        # add hashtag of entire phrase
        keywords = ["#" + keyword.replace(" ", '')]

        # add each word of the phrase
        words = keyword.lower().split(" ")
        keywords.extend(words)

        # check stem of each word (i.e. immigrants -> immigrant)
        stems = [stem(word) for word in keywords]
        keywords.extend(stems)

        return keywords

    @classmethod
    def search_tweets(cls, keyword):
        """Given a keyword searches tweets"""

        keywords = cls.normalize_input(keyword)

    # check if any tweets match the tokenized keywords, prioritizing tweets with more matching keywords

    search_query = db.session.query(Keyword.tweet_id, func.count(Keyword.keyword))


class Keyword(db.Model):
    """Keywords found in tweets"""

    __tablename__ = "keyword"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    keyword = db.Column(db.String(140), nullable=False)
    last_searched db.Column(db.DateTime, nullable=False)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweets.id"), nullable=False)

    tweet = db.relationship('Tweet')

##############################################################################
#Creates test database


def example_data():
    """Create some sample data."""

    brexit = Tweet()

    trump = Tweet()

    jeopardy = Tweet()

    db.session.add_all([brexit, trump, jeopardy])
    db.session.commit()

##############################################################################
# Helper functions


def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///twitter'

    db.app = app
    db.init_app(app)

    print "Connected to DB."


def format_time(datetime):
    """Formats datetime objects for user-friendliness"""

    d = Delorean(datetime, timezone='UTC')

    return d.humanize()


if __name__ == "__main__":

    from server import app

    connect_to_db(app)

    db.create_all()
