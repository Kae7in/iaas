from flask import Blueprint
from intz import dev_blueprint
import flask_restful


site_blueprint = Blueprint('site',
              __name__,
              template_folder='./templates',
              static_folder='./static',
            static_url_path='/site/static'
)


dev = flask_restful.Api()
dev.init_app(site_blueprint)


from . import views
