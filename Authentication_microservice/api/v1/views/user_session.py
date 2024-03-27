#!/usr/bin/env python3
"""
handles sessions management
"""
from flask import make_response, abort, request, jsonify
from Authentication_microservice.api.v1.views import app_views
from models.user import User
from os import getenv
import requests


def deserialiize_response(data):
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

  res = requests.post(url, json={"email": email})
  data = res.json()
  user_dict = {}

  db_users = deserialiize_response(data)
  print(f"db_users: {db_users}")

  file_users = User.search({"email": email})
  print(f"file users: {file_users}")

  for user in db_users:
    user_dict[user.id] = user
  for user in file_users:
    if user.id not in user_dict:
      user_dict[user.id] = user
  
  users = list(user_dict.values())
  print(f"users: {[user.to_dict(fs_indicator=1) for user in users]}")
  if not users:
    return jsonify({"error": "No user found for this email"}), 404

  res = []
  for user in users:
    if user.is_valid_password(password):
      response = make_response(user.to_dict(fs_indicator=1))
      session_id = auth.create_session(user.id)
      SESSION_NAME = getenv("SESSION_NAME")
      if SESSION_NAME is None:
        SESSION_NAME = "DEFAULT"
      response.set_cookie(SESSION_NAME, session_id)

      res.append(response)
  
  if res:
    return res
  return jsonify({"error": "wrong password"}), 401


@app_views.route("/session_auth/logout", methods=["DELETE"], strict_slashes=False)
def logout():
  """
  logs a user out from a sessionn
  """
  from Authentication_microservice.api.v1.app_auth import auth

  if auth.destroy_session(request) is False:
    abort(401)
  return jsonify({"message" "session terminated successfully"}), 200
