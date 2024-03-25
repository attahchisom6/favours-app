#!/usr/bin/env python3
"""
handles sessions management
"""
from flask import make_response, abort, request, jsonify
from Authentication_microservice.api.v1.views import app_views
from models.user import User
from os import getenv


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

  file_users = User.search({"email": email})
  db_users = requests.post(url, json={"email": email})
  users = file_users + db_users
  if not users:
    return jsonify({"error": "No user found for this email"}), 404

  for user in users:
    if user.is_valid_password(password):
      response = make_response(user.to_dict())
      session_id = auth.create_session(user.id)
      SESSION_NAME = getenv("SESSION_NAME")
      if SESSION_NAME is None:
        SESSION_NAME = "DEFAULT"
      response.set_cookie(SESSION_NAME, session_id)

      return response
  return jsonify({"error": "wrong password"}), 401


@app_views.route("/session_auth/logout", methods=["DELETE"], strict_slashes=False)
def logout():
  """
  logs a user out from a session
  """
  from Authentication_microservice.api.v1.app_auth import auth

  if auth.destroy_session(request) is False:
    abort(401)
  return jsonify({"message" "session terminated successfully"}), 200
