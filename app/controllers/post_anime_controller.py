from flask import jsonify, request
from http import HTTPStatus
from app.models.anime_model import Anime
from psycopg2.errors import UniqueViolation

def create():   
    
    try:
        data = request.get_json()
        Anime.verify_keys(data)   
        animes = Anime(**data)
        inserted_anime = animes.create_anime()

    except UniqueViolation:
        return (
            jsonify({"error": 'anime is already exists'}), HTTPStatus.UNPROCESSABLE_ENTITY
        )

    except KeyError:
        keys = ["anime", "released_date", "seasons"]
        request_data_keys = list(data.keys())
        compared_keys = [wrong_key for wrong_key in request_data_keys if wrong_key not in keys]
        return jsonify(
            {
                "available_keys": [
                "anime",
                "released_date",
                "seasons"
                ]
            }, {
                "wrongs_keys_sended":
                compared_keys
            }
            ),HTTPStatus.UNPROCESSABLE_ENTITY

   
        
    serie_keys = ['id', 'anime', 'released_date', 'seasons']
    
    inserted_anime = dict(zip(serie_keys, inserted_anime))
    
    return jsonify(inserted_anime), HTTPStatus.CREATED