#!/usr/bin/python3
""" This module initializes the blueprint app_views """

from flask import jsonify
from api.v1.views import app_views
from models import storage


# Create a route /status on the object app_views
# that returns a JSON: "status": "OK"
# to run <python3 -m api.v1.app>
# http://0.0.0.0:5000/api/v1/status
@app_views.route('/status', methods=['GET'])
def status():
    """ Returns a JSON: "status": "OK """
    return jsonify(status="OK")


# task 5 - some stats with new method count
# Create a route /stats on the object app_views
# to run <python3 -m api.v1.app>
# http://0.0.0.0:5000/api/v1/stats
@app_views.route('/stats', methods=['GET'])
def get_stats():
    """ Create an endpoint that retrieves the number of each
    objects by type: from the storage engine """
    objects_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(objects_count)
