#!/usr/bin/python3
'''starts a Flask web application'''
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    '''return the status of the API'''
    ok_result = {'status': 'OK'}
    return jsonify(ok_result)


@app_views.route('/stats', strict_slashes=False)
def objects_counter():
    '''Retrieves the number of each objects by type'''
    json_to_retieve = {'amenities': storage.count('Amenity'),
                       'cities': storage.count('City'),
                       'places': storage.count('Place'),
                       'reviews': storage.count('Review'),
                       'states': storage.count('State'),
                       'users': storage.count('User')}
    return jsonify(json_to_retieve)
