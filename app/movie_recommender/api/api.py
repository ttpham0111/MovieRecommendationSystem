from flask import Blueprint, jsonify, session, request
import dataset
import knn

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def status():
    return jsonify(status='OK'), 200


@api.route('/login', methods=['GET'])
def login():
    session['user_id'] = None
    pass


""" This returns a list of all movies in the dataset with id, title, year of release, 
link to imdb page, and genres it belongs to."""
@api.route('/movies', methods=['GET'])
def get_movies():
    movies = dataset.load_movies()
    return jsonify(movies), 200


@api.route('/movie/<movie_id>/recommended', methods=['GET'])
def recommend_movies_based_on_movie(movie_id):
    
    movie_id = request.view_args['movie_id']
    movies = knn.get_recommendations(movie_id)

    return jsonify(movies), 200


@api.route('/movies/recommended', methods=['GET'])
def recommend_movies_based_on_user():
    user_id = session['user_id']
    pass