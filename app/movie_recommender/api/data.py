from collections import namedtuple
import io


Movie = namedtuple('Movie', ['id', 'title', 'link', 'genres'])
GENRES = [
    "Action", "Adventure", "Animation", "Children's",
    "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
    "Film-Noir", "Horror", "Musical", "Mystery", "Romance",
    "Sci-Fi", "Thriller", "War", "Western"
]


def get_genres(bits):
    indexes = (i for i, b in enumerate(bits) if b == '1')
    genres = [GENRES[i] for i in indexes]
    return genres


class MovieDataset:
    def __init__(self):
        self._movies = {}

    def initialize(self, data_filepath, delimiter='|'):
        movies = self._movies

        with io.open(data_filepath, encoding='ISO-8859-1') as f:
            for line in f:
                tokens = line.split(delimiter)

                movie_id = tokens[0]
                movies[movie_id] = Movie(id=movie_id, title=tokens[1], link=tokens[4], genres=get_genres(tokens[5:]))

    def get_movies(self, movie_ids=None):
        movies = self._movies

        if movie_ids is None:
            return movies.values()
        else:
            return [movies[movie_id] for movie_id in movie_ids]


movie_dataset = MovieDataset()
