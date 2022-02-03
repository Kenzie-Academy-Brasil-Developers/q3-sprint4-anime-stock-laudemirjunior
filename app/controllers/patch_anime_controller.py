from flask import jsonify, request
from http import HTTPStatus
from app.models.anime_model import Anime

def update(anime_id):
    payload = request.get_json()
    try:
        Anime.verify_keys(payload) 
        updated_anime = Anime.update_anime(anime_id, payload)

        if not updated_anime:
            return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND

        serialize_anime = Anime.serialize_anime(updated_anime)

    except KeyError:
        keys = ["anime", "released_date", "seasons"]
        request_data_keys = list(payload.keys())
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
        

    return jsonify(serialize_anime), HTTPStatus.OK