#!/usr/bin/env python3
"""
handles sessions management
"""
from flask import make_response, abort, request, jsonify
from Authentication_microservice.api.v1.views import app_views
from os import getenv
from utils.storage_interactor import storage_interactor

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

  users = storage_interactor(
      url=url,
      clss="User",
      method="POST",
      data={"email": email}
  )[0]

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
