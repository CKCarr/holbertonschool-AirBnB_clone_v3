#!/usr/bin/python3
""" Create a new view for User objects that handles all default RestFul API """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


# GET /api/v1/users
@views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all User objects """
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


# GET /api/v1/users/<user_id>
def get_user(user_id):
    """ Retrieves a User object by its user_id """
    user = storage.get(User, user_id)
    if user is None:
        # If the user_id is not linked
        # to any User object, raise a 404 error
        abort(404)
    # Convert the User object to a dictionary
    # and return it as JSON response
    return jsonify(user.to_dict())


# DELETE api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object based on the user_id
    if user doesn't exist, raise a 404 error, delete it,
    return an empty dictionary with the status code 200 """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


# POST api/v1/users
def post_user():
    """ Creates a User object based on the JSON body request.
    if the JSON body request is not valid, raise a 400 error.
    if the JSON body request does not contain the key name, raise a 400 error.
    return a dictionary representation of the new
    User object with a status code 201 """
    # If the JSON body request is not valid, raise a 400 error
    if not request.is_json:
        abort(400, description="Not a JSON")
    # If the JSON body request does not contain the key name, raise a 400 error
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    # Create a new User object
    user = User(**request.get_json())
    # Save the new User object
    storage.new(user)
    storage.save()
    # Convert the new User object to a dictionary
    # and return it as JSON response
    return jsonify(user.to_dict()), 201


# PUT api/v1/users/<user_id>
def put_user(user_id):
    """ Updates a User object based on the user_id """
    # If the user_id is not linked to any User object, raise a 404 error
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    # If the JSON body request is not valid, raise a 400 error
    if not request.is_json:
        abort(400, description="Not a JSON")
    # Update the User object
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    # Save the new User object
    storage.save()
    # Convert the new User object to a dictionary
    # and return it as JSON response
    return jsonify(user.to_dict())
