## Twitter Search
Basic app that allows for an end user to search tweets by query string, and display some info about them.

## <a name="technologiesused"></a>Technologies Used

* Python
* Flask
* PostgresSQL
* SQLAlchemy
* Javascript/AJAX
* Jinja2
* Bootstrap
* Twitter API

### Running locally

  * Set up and activate a python virtualenv, and install all dependencies:
    * `pip install -r requirements.txt`
  * Source your secrets (Twitter API credentials)
    * `source secrets.sh`
    * Verify from `echo $TWITTER_CONSUMER_KEY`
  * Make sure you have PostgreSQL running. Create a new database in psql named (dbname):
    * `psql`
    * `CREATE DATABASE (dbname);`
  * Create the tables in your database:
    * `python -i model.py`
    * While in interactive mode, create tables: `db.create_all()`
    * Seed the tables: `psql (dbname) < dump.sql`
  * Now, quit interactive mode. Start up the flask server:
    * `python server.py`
  * Go to localhost:5000 to see the web app