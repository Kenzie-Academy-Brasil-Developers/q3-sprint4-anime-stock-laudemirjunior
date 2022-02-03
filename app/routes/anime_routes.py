from flask import Blueprint
from app.controllers.post_anime_controller import create
from app.controllers.get_anime_controller import read
from app.controllers.get_by_id_controller import get_by_id
from app.controllers.patch_anime_controller import update
from app.controllers.delete_anime_controller import delete


bp = Blueprint('animes', __name__)

bp.get("")(read)

bp.post("")(create)

bp.get("/<int:anime_id>")(get_by_id)

bp.patch("/<int:anime_id>")(update)

bp.delete("/<int:anime_id>")(delete)