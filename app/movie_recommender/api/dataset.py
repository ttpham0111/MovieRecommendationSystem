import os
import io  # needed because of weird encoding of u.item file

def load_movies(movies_id=None):
    movies = []
    dataset = (os.path.expanduser('~') + '/.surprise_data/ml-100k/ml-100k/u.item')
    with io.open(dataset, 'r', encoding='ISO-8859-1') as movies_dataset:
        for line in movies_dataset:
            token = line.split('|')

            movie = {
                "id" : token[0],
                "title" : token[1][:-7],   # removes the year from name
                "year" : token[2][-4:],    # removes the date and month 
                "link" : token[4],
                "genres": get_genres(token[5:])
            }

            if movies_id == None:
                movies.append(movie)
            elif token[0] in movies_id:
                movies.append(movie)
    return movies


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