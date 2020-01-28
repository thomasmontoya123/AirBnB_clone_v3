#!/usr/bin/env python3
"""States view module"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_list():
    """Retrieves the list of all State objects"""
    states_list = []
    states_objs = storage.all('State').values()
    for element in states_objs:
        states_list.append(element.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_list_id(state_id):
    """Retrieves a specific State object"""
    states_objs = storage.all('State').values()
    for element in states_objs:
        if element.id == state_id:
            return jsonify(element.to_dict())
