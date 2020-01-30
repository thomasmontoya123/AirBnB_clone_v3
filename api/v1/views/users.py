#!/usr/bin/env python3
"""Users view module"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_list():
    """Retrieves the list of all User objects"""
    users_list = []
    users_objs = storage.all('User').values()
    for element in users_objs:
        users_list.append(element.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def users_list_id(user_id):
    """Retrieves a specific User object by Id"""
    users_objs = storage.all('User').values()
    for element in users_objs:
        if element.id == user_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def user_remove(user_id):
    """Remove one user by its Id"""
    user_to_delete = storage.get('User', user_id)
    if user_to_delete is None:
        abort(404)
    storage.delete(user_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
    '''Creates a new user'''
    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")
    if not user_data.get('name'):
        abort(400, "Missing name")
    if not user_data.get('email'):
        abort(400, "Missing email")
    if not user_data.get('password'):
        abort(400, "Missing password")
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def user_update(user_id):
    '''Updates one user based on its id'''
    data_for_update = request.get_json()
    if data_for_update is None:
        abort(400, "Not a JSON")
    forbiden_keys = ['id', 'created_at', 'updated_at', 'email']
    user_to_update = storage.get('User', user_id)
    if user_to_update is None:
        abort(404)
    for key, value in data_for_update.items():
        if key not in forbiden_keys:
            setattr(user_to_update, key, value)
    user_to_update.save()
    return jsonify(user_to_update.to_dict()), 200
