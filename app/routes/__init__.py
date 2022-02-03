from flask import Flask, Blueprint

from app.routes.anime_routes import bp as bp_animes_routes

bp_api = Blueprint("api", __name__, url_prefix="/animes")


def init_app(app: Flask):
    
    bp_api.register_blueprint(bp_animes_routes)
    
    app.register_blueprint(bp_api)