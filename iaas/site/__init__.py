from flask import Blueprint
import flask_restful


site_blueprint = Blueprint('site',
              __name__,
              template_folder='./templates',
              static_folder='./static'
)


dev = flask_restful.Api()
dev.init_app(site_blueprint)


from . import views
