from datetime import datetime, timedelta

from elasticsearch import Elasticsearch
from flask import Flask, render_template
from flask import g
from flask.ext.httpauth import HTTPTokenAuth
from flask.ext.mongoalchemy import MongoAlchemy

# Define the WSGI application object
app = Flask(__name__, static_url_path='/')

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = MongoAlchemy(app)

# Define Elasticsearch
es = Elasticsearch([app.config.get('ELASTICSEARCH_SERVER')],
                   http_auth=(app.config.get('ELASTICSEARCH_SERVER_USERNAME'), app.config.get('ELASTICSEARCH_SERVER_PASSWORD')))

# STOP WORD
# from app.helper.stop_word_filter import StopWordFilter
# swf = StopWordFilter()

# Define the generic authentication handler
auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    from apps.model.token import Token
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
from apps.mod.mod_home.controller import mod_home as home_module
from apps.mod.mod_auth.controller import mod_auth as auth_module
# from app.mod.mod_summary.controller import mod_summary as summary_module
# from app.mod.mod_kml.controller import mod_kml as kml_module
# from app.mod.mod_post.controller import mod_post as post_module
# from app.mod.mod_cloud_key.controller import mod_cloud_key as cloud_key_module
# from app.mod.mod_potential_solution.controller import mod_ps as potential_solution_module

# Register blueprint(s)
app.register_blueprint(home_module)
app.register_blueprint(auth_module)
# app.register_blueprint(summary_module)
# app.register_blueprint(kml_module)
# app.register_blueprint(post_module)
# app.register_blueprint(cloud_key_module)
# app.register_blueprint(potential_solution_module)