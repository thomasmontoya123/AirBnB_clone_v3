#!/usr/bin/python3
'''Handles flask server and blueprint'''
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """ Handle app context"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    json_error = {"error": "Not found"}
    return jsonify(json_error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
