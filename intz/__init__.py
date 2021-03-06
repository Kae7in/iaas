from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


# Configure app
app = Flask(__name__)
app.config['SERVER_NAME']='intz.com:5000'
app.config['PROPAGATE_EXCEPTIONS'] = True


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getcwd() + '/integers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# Login Manager congfiguration
app.secret_key = 'kaelin says hyperloop is the future'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'site.login'


from intz.dev import dev_blueprint
from intz.site import site_blueprint
import intz.models


# Blueprint registration
app.register_blueprint(dev_blueprint, subdomain='dev')
app.register_blueprint(site_blueprint)