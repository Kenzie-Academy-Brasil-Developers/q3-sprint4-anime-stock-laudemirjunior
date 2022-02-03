from flask import jsonify
from http import HTTPStatus
from app.models.anime_model import Anime

def get_by_id(anime_id):
    serie_keys = ['id', 'anime', 'released_date', 'seasons']
    
    series_list = [dict(zip(serie_keys, serie)) for serie in Anime.get_anime_by_id(anime_id)]
    
    if series_list == []:
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND

    return jsonify({'data': series_list}), HTTPStatus.OK