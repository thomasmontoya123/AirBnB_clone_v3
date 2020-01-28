#!/usr/bin/python3
'''starts a Flask web application'''
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    '''return the status of the API'''
    ok_result = {'status': 'OK'}
    return jsonify(ok_result)
