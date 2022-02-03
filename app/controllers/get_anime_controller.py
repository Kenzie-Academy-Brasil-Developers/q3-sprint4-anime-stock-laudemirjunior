from flask import jsonify, request
from http import HTTPStatus
from app.models.anime_model import Anime
from psycopg2.errors import UndefinedTable

def read():
    try:
        Anime.get_animes()
        
    except UndefinedTable:
        Anime.create()
        return jsonify({"data": []}), HTTPStatus.OK    
    
    except TypeError:
        return jsonify({"data": []}), HTTPStatus.OK    
    
    serie_keys = ['id', 'anime', 'released_date', 'seasons']
    
    series_list = [dict(zip(serie_keys, serie)) for serie in Anime.get_animes()]
    
    return jsonify({'data': series_list}), HTTPStatus.OK