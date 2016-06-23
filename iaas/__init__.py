from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


# Configure app
app = Flask(__name__)
app.config['SERVER_NAME']='localhost:5000'


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getcwd() + '/integers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


from iaas.dev import dev_blueprint
from iaas.site import site_blueprint
import iaas.models


# Blueprint registration
app.register_blueprint(dev_blueprint, subdomain='dev')
app.register_blueprint(site_blueprint)


# import iaas.views
