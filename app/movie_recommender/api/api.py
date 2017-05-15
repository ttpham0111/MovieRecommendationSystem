from functools import wraps

from flask import Blueprint, jsonify, session, request

from movie_recommender.api import dataset
from movie_recommender.api import knn


api = Blueprint('api', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_id'):
            return jsonify(error='Unauthorized'), 401
        else:
            return f(*args, **kwargs)

    return decorated


@api.route('/', methods=['GET'])
def status():
    return jsonify(status='OK'), 200


@api.route('/login', methods=['POST'])
def login():
    user_id = request.json['user_id']
    session['user_id'] = user_id
    return jsonify(user_id=user_id), 200


@login_required
@api.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify(status='OK'), 200


@api.route('/movies', methods=['GET'])
def get_movies():
    """ Returns a list of movies.

    Returns a list of all movies in the dataset with id, title, year of release, link to imdb page, and genres it belongs to.
    """

    movies = dataset.load_movies()
    return jsonify(movies), 200


@api.route('/movie/<movie_id>/recommended', methods=['GET'])
def recommend_movies_based_on_movie(movie_id):
    movie_id = request.view_args['movie_id']
    movies = knn.get_recommendations(movie_id)

    return jsonify(movies), 200


@login_required
@api.route('/movies/recommended', methods=['GET'])
def recommend_movies_based_on_user():
    user_id = session['user_id']
    pass
