from surprise import KNNBaseline
from surprise import Dataset
import dataset

# First, train the algortihm to compute the similarities between movies
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = KNNBaseline(sim_options=sim_options)
algo.train(trainset)


def get_recommendations(movie_id):	
	movie_inner_id = algo.trainset.to_inner_iid(movie_id)
	
	# Retrieve inner ids of the nearest neighbors of movie.
	movie_neighbors_inner_id = algo.get_neighbors(movie_inner_id, k=10)
	
	# Convert inner ids of the neighbors into names.
	movie_neighbors_id = (algo.trainset.to_raw_iid(inner_id)
        for inner_id in movie_neighbors_inner_id)
	movie_neighbors = (id for id in movie_neighbors_id)
	
        movies_id = []

	for movie_id in movie_neighbors:
            movie_id = movie_id.encode('ascii')
            movies_id.append(movie_id)

        movies = dataset.load_movies(movies_id)
        return movies