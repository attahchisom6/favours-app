#!/usr/bin/env python3
"""
handle user related operations using RESTFUL API APPROACH
"""
from Authentication_microservice.api.v1.views import app_views
from models.user import User
from flask import jsonify, make_response, abort
import requests


file_url = "http://0.0.0.0:5000"
db_url = "http://0.0.0.0:5001"

@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    return the list of all users in the database
    """
    res = None
    try:
        res = requests.get(f"{file_url}/objects?cls=User")
    except:
      return None
    
    if res is not None:
        return res.json()
