#!/usr/bin/env python3
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_list():
    """Retrieves the list of all State objects"""
    sates_list = []
    states_objs = storage.all('State').values()
    for element in states_objs:
        states_list.append(element.to_dict())
    return jsonify(states_list)
