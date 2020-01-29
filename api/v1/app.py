#!/usr/bin/python3
'''Handles flask server and blueprint'''
from models import storage
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """ Handle app context"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ Handle error Page Not Found(404)"""
    json_error = {"error": "Not found"}
    return make_response(jsonify(json_error), 404)


if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, debug=True, threaded=True)
