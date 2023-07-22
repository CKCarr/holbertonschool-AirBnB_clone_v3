#!/usr/bin/python3
""" Create a new view for Amenity objects
that handles all default RestFul API """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


# GET /api/v1/amenities
@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


# GET /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id):
    """ Retrieves a Amenity object by its amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        # If the amenity_id is not linked
        # to any Amenity object, raise a 404 error
        abort(404)
    # Convert the Amenity object to a dictionary
    # and return it as JSON response
    return jsonify(amenity.to_dict())


# DELETE api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object based on the amenity_id
    if amenity doesn't exist, raise a 404 error, delete it,
    return an empty dictionary with the status code 200 """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


# POST api/v1/amenities
@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ Creates a Amenity object based on the JSON body request.
    if the JSON body request is not valid, raise a 400 error.
    if the JSON body request does not contain the key name, raise a 400 error.
    return a dictionary representation of the new
    Amenity object with a status code 201 """
    # If the JSON body request is not valid, raise a 400 error
    if not request.get_json():
        # abort() will raise an exception that returns a response
        abort(400, description="Not a JSON")
    # If the JSON body request does not contain the key name, raise a 400 error
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    # Create a new Amenity object
    amenity = Amenity(**request.get_json())
    # Save the new Amenity object
    storage.new(amenity)
    storage.save()
    # Convert the Amenity object to a dictionary
    # and return it as JSON response with status code 201
    return jsonify(amenity.to_dict()), 201


# PUT api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates a Amenity object based on the amenity_id """
    # If the amenity_id is not linked to any Amenity object, raise a 404 error
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    # If the JSON body request is not valid, raise a 400 error
    if not request.get_json():
        abort(400, description="Not a JSON")
    # Retrieve the JSON body request
    json_request = request.get_json()
    # Update the Amenity object
    for key, value in json_request.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    # Save the Amenity object
    storage.save()
    # Convert the Amenity object to a dictionary
    # and return it as JSON response with status code 200
    return jsonify(amenity.to_dict()), 200
