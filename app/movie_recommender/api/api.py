from flask import Blueprint, jsonify


api = Blueprint('api', __name__)


@api.route('/')
def status():
    return jsonify(status='OK'), 200
