import os

from flask import Flask, render_template
from werkzeug.exceptions import NotFound

from movie_recommender.api.api import api


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
