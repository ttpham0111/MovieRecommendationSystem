from thread import start_new_thread
from time import time

from surprise import KNNBaseline, NMF, Dataset, Reader

from movie_recommender.api.data import movie_dataset


class MovieRecommender:
    def __init__(self):
        self._knn = None
        self._nmf = None
        self._trainset = None
        self._predictions = None

        self.initialized = False

    def initialize(self, data_filepath):
        self._data = Dataset.load_from_file(data_filepath, reader=Reader('ml-100k'))
        self._trainset = self._data.build_full_trainset()

        sim_options = {'name': 'pearson_baseline', 'user_based': False}
        self._knn = KNNBaseline(sim_options=sim_options)
        self._nmf = NMF()

        start_new_thread(self._train)

    def get_similar_movies(self, movie_id, k=10):
        if not self.initialized:
            return []

        model = self._knn

        movie_inner_id = model.trainset.to_inner_iid(movie_id)
        similar_movie_inner_ids = model.get_neighbors(movie_inner_id, k=k)

        to_raw_iid = model.trainset.to_raw_iid
        similar_movie_ids = (to_raw_iid(inner_id) for inner_id in similar_movie_inner_ids)

        movie_ids = [similar_movie_id.encode('ascii') for similar_movie_id in similar_movie_ids]
        return movie_dataset.get_movies(movie_ids)

    def get_similar_movies_for_user(self, user_id, num_movies=10):
        if not self.initialized:
            return []

        user_id = str(user_id)
        user_predictions = [prediction for prediction in self._predictions if prediction[0] == user_id]

        sorted_predictions = sorted(user_predictions, key=lambda x: x.est, reverse=True)
        top_n_predictions = sorted_predictions[:num_movies]

        similar_movie_ids = (prediction.iid for prediction in top_n_predictions)

        movie_ids = [similar_movie_id.encode('ascii') for similar_movie_id in similar_movie_ids]
        return movie_dataset.get_movies(movie_ids)

    def update_user_ratings(self, user_id, movie_id, rating):
        if not self.initialized:
            return

        rating = float(rating)

        has_previous_rating = False
        if self._trainset.knows_user(user_id):
            trainset_dict = dict(self._trainset.ur[user_id])
            has_previous_rating = movie_id in trainset_dict

        user_id = str(user_id)
        movie_id = str(movie_id)
        new_rating = (user_id, movie_id, rating, time())
        if has_previous_rating:
            for i, rating in enumerate(self._data.raw_ratings):
                if rating[0] == user_id and rating[1] == movie_id:
                    self._data.raw_ratings[i] = new_rating
                    break
        else:
            self._data.raw_ratings.append(new_rating)

        self._trainset = self._data.build_full_trainset()
        self._train()

    def _train(self):
        self._nmf.train(self._trainset)
        self._knn.train(self._trainset)

        self._predictions = self._nmf.test(self._trainset.build_anti_testset())

        self.initialized = True


movie_recommender = MovieRecommender()
