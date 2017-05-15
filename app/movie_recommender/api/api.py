from flask import Blueprint, jsonify, session
import io
import os

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def status():
    return jsonify(status='OK'), 200


@api.route('/login', methods=['GET'])
def login():
    session['user_id'] = None
    pass


@api.route('/movies', methods=['GET'])
def get_movies():
    movies = []
    dataset = (os.path.expanduser('~')+'/.surprise_data/ml-100k/ml-100k/u.item')
    with io.open(dataset, 'r', encoding='ISO-8859-1') as movies_dataset:
        for line in movies_dataset:
            token = line.split('|')

            movie = {
                "id" : token[0],
                "title" : token[1][:-7],
                "year" : token[2][-4:],
                "link" : token[4],
                "genres": get_genres(token[5:])
            }

            movies.append(movie)

    return jsonify(movies), 200


def get_genres(bits):
    all_genres = [
        "Action", "Adventure", "Animation", "Children's",
        "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
        "Film-Noir", "Horror", "Musical", "Mystery", "Romance",
        "Sci-Fi", "Thriller", "War", "Western"
    ]

    indexes = [i for i, b in enumerate(bits) if b == '1']
    genres = [all_genres[i] for i in indexes]
    return genres



@api.route('/movie/<movie_id>/recommended', methods=['GET'])
def recommend_movies_based_on_movie(movie_id):
    pass


@api.route('/movies/recommended', methods=['GET'])
def recommend_movies_based_on_user():
    user_id = session['user_id']
    pass