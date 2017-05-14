from flask import Blueprint, jsonify, session


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
    pass


@api.route('/movie/<movie_id>/recommended', methods=['GET'])
def recommend_movies_based_on_movie(movie_id):
    pass


@api.route('/movies/recommended', methods=['GET'])
def recommend_movies_based_on_user():
    user_id = session['user_id']
    pass
