import os

from flask import Flask, render_template
from werkzeug.exceptions import NotFound

from movie_recommender.api.api import api
from movie_recommender.api.data import movie_dataset
from movie_recommender.api.models import movie_recommender

# Initialize app
app = Flask(__name__, static_folder='public', template_folder='public')
app.secret_key = os.environ['SECRET_KEY']

# Register API
app.register_blueprint(api, url_prefix='/api')


# Catch all route
@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def index(path):
    try:
        return app.send_static_file(path)
    except NotFound:
        return render_template('index.html')


def initialize_data():
    here = os.path.dirname(os.path.realpath(__file__))

    movie_dataset.initialize(os.path.join(here, 'api/data/ml-100k/u.item'), delimiter='|')
    movie_recommender.initialize(os.path.join(here, 'api/data/ml-100k/u.data'))


# Initialize data
initialize_data()
