from app.models import DatabaseConnector
from psycopg2 import sql

class Anime(DatabaseConnector):

    anime_keys = ["id", "anime", "released_date", "seasons"]


    def __init__(self, *args, **kwargs):
        self.anime = kwargs['anime']
        self.released_date = kwargs['released_date']
        self.seasons = kwargs['seasons']

    def create_anime(self):
        self.get_conn_cur()
        
        query = """
            INSERT INTO
                animes (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """
        
        query_values = list(self.__dict__.values())
        
        self.cur.execute(query, query_values)

        insert_anime = self.cur.fetchone()
        
        self.commit_and_close()
        
        return insert_anime
        
    @classmethod
    def get_animes(cls):
        cls.get_conn_cur()
        
        query = "SELECT * FROM animes;"
        
        cls.cur.execute(query)
        
        series = cls.cur.fetchall()
        
        cls.commit_and_close()
        
        return series

    @classmethod
    def create_table(cls):
        cls.get_conn_cur()
        
        query = """CREATE TABLE IF NOT EXISTS animes(
                 id            BIGSERIAL PRIMARY KEY,
                 anime         VARCHAR(100) UNIQUE NOT NULL,
                 released_date DATE NOT NULL,
                 seasons       INTEGER NOT NULL);"""

        cls.cur.execute(query)
        
        cls.commit_and_close()
        
    @classmethod
    def get_anime_by_id(cls, serie_id):
        cls.get_conn_cur()
        
        query = "SELECT * FROM animes WHERE id = %s;"
        
        cls.cur.execute(query, (serie_id, ))
        
        animes = cls.cur.fetchall()
        
        cls.commit_and_close()
        
        return animes

    @staticmethod
    def serialize_anime(data, keys=anime_keys):
        if type(data) is tuple:
            return dict(zip(keys, data))
        if type(data) is list:
            return [dict(zip(keys, user)) for user in data]    
    
    @classmethod
    def update_anime(cls, anime_id, payload):
        cls.get_conn_cur()

        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]


        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = ROW({values})
                WHERE
                    id={id}
                RETURNING *
            """
        ).format(
            id=sql.Literal(anime_id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cls.cur.execute(query)
        updated_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_anime

    @classmethod
    def verify_keys(cls, data):
        trusted_keys = ["anime", "released_date", "seasons"]
        for key in data:
            if not key in trusted_keys:
                raise KeyError

    @classmethod
    def delete_anime(cls, id):
        cls.get_conn_cur()
        query = sql.SQL(
            """
                DELETE FROM animes WHERE id={id} RETURNING *;
            """
        ).format(id=sql.Literal(id))
        cls.cur.execute(query)
        deleted_anime = cls.cur.fetchone()
        cls.commit_and_close()
        return deleted_anime