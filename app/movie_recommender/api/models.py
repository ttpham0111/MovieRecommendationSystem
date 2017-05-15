from surprise import KNNBaseline, Dataset

from movie_recommender.api.data import movie_dataset


class MovieRecommender:
    def __init__(self):
        self._model = None

    def initialize(self):
        data = Dataset.load_builtin('ml-100k')
        trainset = data.build_full_trainset()
        sim_options = {'name': 'pearson_baseline', 'user_based': False}

        self._model = KNNBaseline(sim_options=sim_options)
        self._model.train(trainset)

    def get_similar_movies(self, movie_id, k=10):
        model = self._model

        movie_inner_id = model.trainset.to_inner_iid(movie_id)
        similar_movie_inner_ids = model.get_neighbors(movie_inner_id, k=k)

        to_raw_iid = model.trainset.to_raw_iid
        similar_movie_ids = (to_raw_iid(inner_id) for inner_id in similar_movie_inner_ids)

        movie_ids = [similar_movie_id.encode('ascii') for similar_movie_id in similar_movie_ids]
        return movie_dataset.get_movies(movie_ids)


movie_recommender = MovieRecommender()
