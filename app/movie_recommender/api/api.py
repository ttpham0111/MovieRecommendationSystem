from functools import wraps

from flask import Blueprint, jsonify, session, request

from movie_recommender.api.data import movie_dataset
from movie_recommender.api.models import movie_recommender
from collections import defaultdict
from surprise import SVD
from surprise import Dataset
from surprise import NMF



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
    movies = movie_dataset.get_movies()
    return jsonify(movies), 200


@api.route('/movie/<movie_id>/recommended', methods=['GET'])
def recommend_movies_based_on_movie(movie_id):
    movies = movie_recommender.get_similar_movies(movie_id)
    return jsonify(movies), 200


@login_required
@api.route('/movies/recommended', methods=['GET'])
def recommend_movies_based_on_user():
    # user_id = session['user_id']
    data = Dataset.load_builtin('ml-100k')
    trainset = data.build_full_trainset()
    algo = NMF()
    algo.train(trainset)
    #input a user id
    uid_test = str(101) 
    #input an item id
    iid_test = str(300)
    user_id = str(932)
    #predictions = algo.predict(uid_test, iid_test, r_ui = 4, verbose = true)
    
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)

    top_n = get_top_n_items(predictions, n = 10)

    recommended_movies = top_n[user_id]

    # for uid, user_ratings in top_n.items():
    #     print (uid, [iid for (iid, _) in user_ratings])
    # print (user_id)
    # user_index = predictions.index(user_id)
    return jsonify(recommended_movies), 200



def get_top_n_items(predictions, n = 10):
    top_n_items = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n_items[uid].append((iid,est))

    for uid, user_ratings in top_n_items.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n_items[uid] = user_ratings[:n]

    return top_n_items
