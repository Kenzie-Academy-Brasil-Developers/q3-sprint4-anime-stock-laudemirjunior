from http.client import NOT_FOUND
from flask import jsonify
from psycopg2.errors import UndefinedTable
from http import HTTPStatus

from app.models.anime_model import Anime

def delete(anime_id):

    anime = Anime.get_anime_by_id(anime_id)

    if anime == []:
        return jsonify({"error": "Not Found"}), NOT_FOUND

    Anime.delete_anime(anime_id)
    
    return '', HTTPStatus.NO_CONTENT 