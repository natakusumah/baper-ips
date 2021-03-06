from datetime import datetime, timedelta

from elasticsearch import Elasticsearch
from flask import Flask, render_template
from flask import g
from sklearn import neural_network
from flask.ext.httpauth import HTTPTokenAuth
from flask.ext.mongoalchemy import MongoAlchemy
from pymongo import MongoClient

# Define the WSGI application object
app = Flask(__name__, static_url_path='/')

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = MongoAlchemy(app)
app.config["MONGO_DBNAME"] = "ips_db"
# mongo = pymongo(app, config_prefix='MONGO')
client = MongoClient('localhost', 27017)
dataset = client['ips_db']

engine = neural_network
# Define Elasticsearch
# es = Elasticsearch([app.config.get('ELASTICSEARCH_SERVER')],
#                    http_auth=(app.config.get('ELASTICSEARCH_SERVER_USERNAME'), app.config.get('ELASTICSEARCH_SERVER_PASSWORD')))

# STOP WORD
# from app.helper.stop_word_filter import StopWordFilter
# swf = StopWordFilter()

# Define the generic authentication handler
auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    from app.model.token import Token
    data = Token.query.filter({'token': token}).first()

    if data:
        if data.created_time > datetime.now() - timedelta(days=1):
            g.current_user = data.client
            return True

    return False


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod.mod_home.controller import mod_home as home_module
from app.mod.mod_auth.controller import mod_auth as auth_module
from app.mod.mod_class.controller import mod_class as ml_module

# Register blueprint(s)
app.register_blueprint(home_module)
app.register_blueprint(auth_module)
app.register_blueprint(ml_module)