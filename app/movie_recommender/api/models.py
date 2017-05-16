from surprise import KNNBaseline, NMF, Dataset

from movie_recommender.api.data import movie_dataset


class MovieRecommender:
    def __init__(self):
        self._knn = None
        self._nmf = None

    def initialize(self):
        data = Dataset.load_builtin('ml-100k')
        self.trainset = data.build_full_trainset()

        sim_options = {'name': 'pearson_baseline', 'user_based': False}
        self._knn = KNNBaseline(sim_options=sim_options)
        self._knn.train(self.trainset)

        self._nmf = NMF()
        self._nmf.train(self.trainset)
        self._predictions = self._nmf.test(self.trainset.build_anti_testset())

    def get_similar_movies(self, movie_id, k=10):
        model = self._knn

        movie_inner_id = model.trainset.to_inner_iid(movie_id)
        similar_movie_inner_ids = model.get_neighbors(movie_inner_id, k=k)

        to_raw_iid = model.trainset.to_raw_iid
        similar_movie_ids = (to_raw_iid(inner_id) for inner_id in similar_movie_inner_ids)

        movie_ids = [similar_movie_id.encode('ascii') for similar_movie_id in similar_movie_ids]
        return movie_dataset.get_movies(movie_ids)

    def get_similar_movies_for_user(self, user_id, num_movies=10):
        user_predictions = [prediction for prediction in self._predictions if prediction[0] == user_id]

        sorted_predictions = sorted(user_predictions, key=lambda x: x.est, reverse=True)
        top_n_predictions = sorted_predictions[:num_movies]

        similar_movie_ids = (prediction.iid for prediction in top_n_predictions)

        movie_ids = [similar_movie_id.encode('ascii') for similar_movie_id in similar_movie_ids]
        return movie_dataset.get_movies(movie_ids)


movie_recommender = MovieRecommender()
