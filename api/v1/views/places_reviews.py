#!/usr/bin/python3
"""States view module.."""
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def all_reviews():
    """Retrieves the list of all State objects"""
    reviews_list = []
    states_objs = storage.all('Review').values()
    for element in states_objs:
        reviews_list.append(element.to_dict())
    print(reviews_list)
    return jsonify(reviews_list)


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_list(place_id):
    """Retrieves the list of all State objects"""
    reviews_list = []
    places_objs = storage.get('Place', place_id)
    if places_objs is None:
        abort(404)
    for places in places_objs.reviews:
        reviews_list.append(places.to_dict())

    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviews_list_id(review_id):
    """Retrieves a specific City object by Id"""
    places_objs = storage.all('Review').values()
    for element in places_objs:
        if element.id == review_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def reviews_remove(review_id):
    """Remove a state by Id"""
    review_to_delete = storage.get('Review', review_id)
    if review_to_delete is None:
        abort(404)
    review_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def new_review(place_id):
    """Creates a new state"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    place_data = request.get_json()
    if place_data is None:
        abort(400, "Not a JSON")
    if not place_data.get('user_id'):
        abort(400, "Missing user_id")
    if not place_data.get('text'):
        abort(400, "Missing text")
    user_obj = storage.get('User', place_data.get('user_id'))
    if user_obj is None:
        abort(404)
    place_data['city_id'] = place_data.get('city_id')
    place_data['user_id'] = place_data.get('user_id')
    print(place_data)
    new_city = Place(**place_data)
    storage.new(new_city)
    storage.save()
    storage.reload()
    return make_response(jsonify(new_city.to_dict())), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_update(review_id):
    """Updates one place based on its id"""
    forbiden_keys = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    place_to_update = storage.get('Review', review_id)
    if place_to_update is None:
        abort(404)
    data_for_update = request.get_json()
    if data_for_update is None:
        abort(400, "Not a JSON")
    for key, value in data_for_update.items():
        if key not in forbiden_keys:
            setattr(place_to_update, key, value)
    place_to_update.save()
    storage.reload()
    return jsonify(place_to_update.to_dict()), 200
