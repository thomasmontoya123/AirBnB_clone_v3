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
    """Retrieves the list of all Review objects"""
    reviews_list = []
    review_objs = storage.all('Review').values()
    for element in review_objs:
        reviews_list.append(element.to_dict())
    print(reviews_list)
    return jsonify(reviews_list)


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_list(place_id):
    """Retrieves the place objects by its id"""
    reviews_list = []
    places_objs = storage.get('Place', place_id)
    if places_objs is None:
        abort(404)
    for places in places_objs.reviews:
        reviews_list.append(places.to_dict())

    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviews_list_id(review_id):
    """Retrieves a specific review object by Id"""
    review_objs = storage.all('Review').values()
    for element in review_objs:
        if element.id == review_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def reviews_remove(review_id):
    """Remove a review by Id"""
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
    review_data = request.get_json()
    if review_data is None:
        abort(400, "Not a JSON")
    if not review_data.get('user_id'):
        abort(400, "Missing user_id")
    if not review_data.get('text'):
        abort(400, "Missing text")
    user_obj = storage.get('User', review_data.get('user_id'))
    if user_obj is None:
        abort(404)

    review_data['place_id'] = place_id
    new_review = Review(**review_data)
    storage.new(new_review)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


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
