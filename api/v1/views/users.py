#!/usr/bin/python3
""" Create a new view for User objects that handles all default
RestFul API actions which are: GET, DELETE, POST, PUT """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


# GET /api/v1/users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


# GET /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object by its user_id"""
    user = storage.get(User, user_id)
    if user is None:
        # If the user_id is not linked to any User object, raise a 404 error
        abort(404)
    # Convert the User object to a dictionary and return it as JSON response
    return jsonify(user.to_dict())


# DELETE /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object based on the user_id
    if user doesn't exist, raise a 404 error, delete it,
    return an empty dictionary with the status code 200"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


# POST /api/v1/users
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a User object based on the JSON body request.
    if the JSON body request is not valid, raise a 400 error.
    if the JSON body request does not contain the key email, raise a 400 error.
    if the JSON body request does not contain the key password,
    raise a 400 error.
    return a dictionary representation of the new
    User object with a status code 201
    """
    # If the JSON body request is not valid, raise a 400 error
    if not request.get_json():
        # abort() will raise an exception that returns a response
        abort(400, description="Not a JSON")
    # If the JSON body request does not contain the key email,
    # raise a 400 error
    if 'email' not in request.get_json():
        # abort() will raise an exception that returns a response
        abort(400, description="Missing email")
    # If the JSON body request does not contain the key password,
    # raise a 400 error
    if 'password' not in request.get_json():
        # abort() will raise an exception that returns a response
        abort(400, description="Missing password")
    # ** unpacks the dictionary *args *kwargs
    # User(**request.get_json()) returns a User object by unpacking the dict
    # and passing it as keyword arguments to the User constructor
    new_user = User(**request.get_json())
    # save the new user
    new_user.save()
    # return a dictionary representation of the new User object with a status
    return jsonify(new_user.to_dict()), 201


# PUT /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    Updates a User object based on the user_id
    if the JSON body request is not valid, raise a 400 error.
    if the User object doesn't exist, raise a 404 error.
    return a dictionary representation of the User object with the status code
    200
    """
    user = storage.get(User, user_id)
    # If the user_id is not linked to any User object, raise a 404 error
    if user is None:
        # abort() will raise an exception that returns a response
        abort(404)
    # If the JSON body request is not valid, raise a 400 error
    if not request.get_json():
        abort(400, description="Not a JSON")
    # Update the User object with all key-value pairs of the dictionary
    for key, value in request.get_json().items():
        # if key is not in the list, ignore it
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            # setattr(object, name, value) is the same as user.key = value
            setattr(user, key, value)
    # save the updated user
    user.save()
    # return a dictionary representation of the User object with the status
    return jsonify(user.to_dict()), 200
