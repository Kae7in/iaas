from flask import Blueprint
import flask_restful


dev_blueprint = Blueprint('dev',
              __name__,
              template_folder='./templates',
              static_folder='./static',
              subdomain='dev'
)


dev = flask_restful.Api()
dev.init_app(dev_blueprint)


from . import views