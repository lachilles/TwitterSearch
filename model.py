"""Models and database functions for Udemy project"""


from flask_sqlalchemy import SQLAlchemy
from api import get_tweets_by_api
import re

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
    handle = db.Column(db.String(64), nullable=False)  #user.screen_name
    user_name = db.Column(db.String(60), nullable=False)  #user.name
    user_location = db.Column(db.String(160), nullable=True)
    follower_count = db.Column(db.Integer, nullable=True)
    tweet_count = db.Column(db.Integer, nullable=True)
    verified_status = db.Column(db.String(10), nullable=True)

    tweets = db.relationship('Tweet')

    def __repr__(self):
        """Represents user object"""

        return "<User ID: %d, Name: %s>" % (self.user_id, self.handle, self.user_name)

    def as_dict(self):
        """Returns object in dictionary format"""

        data = {
            'name': self.user_name,
            'handle': self.handle,
            'follower_count': self.follower_count,
            'user_id': self.user_id
        }

        return data


class Tweet(db.Model):
    "Tweets by query string"

    __tablename__ = "tweets"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tweet_id = db.Column(db.BigInteger, nullable=False)  #id
    tweet_id_str = db.Column(db.String(64), nullable=True)  #id_str
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.user_id"), nullable=False)
    handle = db.Column(db.String(64), nullable=False)  #user.screen_name
    created_at = db.Column(db.DateTime, nullable=False)  #created_at
    text = db.Column(db.String(240), nullable=False)  #text
    retweet_count = db.Column(db.Integer, nullable=True)  #retweet_count
    favorite_count = db.Column(db.Integer, nullable=True)  #favorite_count
    hashtags = db.Column(db.String(240), nullable=True)  #hashtags
    pulled_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('TwitterUser')
    keywordmap = db.relationship('KeywordMap')

    def __repr(self):
        """Represens tweet object"""

        return "<Tweet ID: %s, Keyword: %s>" % (self.tweet_id, self.keyword)

    def as_dict(self):
        """Returns dictionary format of tweet"""

        tweet = {
            'created_at': self.created_at,
            'handle': self.user.screen_name,
            'user_id': self.user_id,
            'tweet_id': self.tweet_id,
            'text': self.text,
            'favorites': self.favorite_count,
            'hashtags': self.hashtags,
        }

        return tweet

    @staticmethod
    def normalize_input(keyword):
        """Preprocess input"""
        # Convert to lower case
        keyword = keyword.lower()
        # Remove additional white spaces
        keyword = re.sub('[\s]+', ' ', keyword)

        return keyword

    @classmethod
    def get_tweets(self, keyword):
        """Given a keyword searches tweets"""

        keyword = self.normalize_input(keyword)

        return get_tweets_by_api(self.keyword)


class KeywordMap(db.Model):
    """Keywords found in tweets"""

    __tablename__ = "keywordmap"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    keyword = db.Column(db.String(140), nullable=False)
    last_searched = db.Column(db.DateTime, nullable=False)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweets.id"), nullable=False)

    tweet = db.relationship('Tweet')

##############################################################################
#Creates test database


# def example_data():
#     """Create some sample data."""

#     brexit = Tweet()

#     trump = Tweet()

#     jeopardy = Tweet()

#     db.session.add_all([brexit, trump, jeopardy])
#     db.session.commit()

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///twitter'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
