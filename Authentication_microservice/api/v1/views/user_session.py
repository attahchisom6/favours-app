#!/usr/bin/env python3
"""
handles sessions management
"""
from flask import make_response, abort, request, jsonify
from Authentication_microservice.api.v1.views import app_views
from models.user import User
from os import getenv
import requests


def deserialize_response(data):
  """
  deserialize data from an api payload back to
  user instances
  """
  if not data:
    return None
  if isinstance(data, list):
    return [User(**user_data) for user_data in data]
  elif isinstance(data, dict):
    return User(**data)
  else:
    return None

@app_views.route("/session_auth/login", methods=["POST"], strict_slashes=False)
def login():
  """
  create a session for a valid logged in user
  """
  from Authentication_microservice.api.v1.app_auth import auth
  data = request.form
  url = "http://0.0.0.0:5001/search/User"

  email, password = data.get("email"), data.get("password")

  if not email:
    return jsonify({"error": "email missing!"}), 400

  if not password:
    return jsonify({"error": "password missing!"}), 400

  try:
    res = requests.post(url, json={"email": email})
    db_data = res.json()
    users = deserialize_response(db_data)
    print(f"db_users: {users}")
  except Exception as e:
    print(f"could not fetch data from DB: {e}")
    users = None

  if users is None:
    try:
      users = User.search({"email": email})
      print(f"file users: {users}")
    except Exception as e:
      return jsonify({"Error": f"No user found for this email, {e}"})
  
  if users is None:
    return jsonify({"Error": "No user found for this email"})

  for user in users:
    if user.is_valid_password(password):
      response = make_response(jsonify(user.to_dict(fs_indicator=1)))
      SESSION_NAME = getenv("SESSION_NAME", "DEFAULT")
      session_id = auth.create_session(user.id)
      if session_id:
        response.set_cookie(SESSION_NAME, session_id)
      else:
        response = make_response(jsonify({"error": "failed to create session"}), 500)
      return response
      
  return jsonify({"error": "wrong password"}), 401


@app_views.route("/session_auth/logout", methods=["DELETE"], strict_slashes=False)
def logout():
  """
  logs a user out from a sessionn
  """
  from Authentication_microservice.api.v1.app_auth import auth

  if auth.destroy_session(request) is False:
    abort(401)
  return jsonify({"message": "session terminated successfully"}), 200
