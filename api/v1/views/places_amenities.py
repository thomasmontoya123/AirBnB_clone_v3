#!/usr/bin/python3
"""places_amenities view module."""
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def list_place_by_amenity(place_id):
    """list of all Amenity objects of a place"""
    amenities_list = []
    place_get = storage.get('Place', place_id)
    if place_get is None:
        abort(404)
    for element in place_get:
        amenities_list.append(element.to_dict())
    return jsonify(amenities_list)


@app_views.route('places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    '''Deletes one amenity of a place'''
    place_get = storage.get('Place', place_id)
    amenity_get = storage.get('Amenity', amenity_id)

    if place_get is None or amenity_get is None:
        abort(404)

    if amenity_get not in place_get.amenities:
        abort(404)

    place_get.amenities.remove(amenity_get)
    place_get.save()
    return jsonify({})


@app_views.route('places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def new_amenity(place_id, amenity_id):
    """Creates one amenity"""
    place_get = storage.get('Place', place_id)
    amenity_get = storage.get('Amenity', amenity_id)

    if place_get is None or amenity_get is None:
        abort(404)
    if amenity_get in place_get.amenities:
        return make_response(jsonify(amenity_get.to_dict()), 200)
    place_get.amenities.append(amenity_get)
    place_get.save()
    return make_response(jsonify(amenity_get.to_dict()), 201)
