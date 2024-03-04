#!/usr/bin/env python3
"""
aoi's defined here doesn't need authorizarion
"""
from flask import abort, jsonify
from Authentication_microservice.api.v1.views import app_views

@app_views.route("/status", methods=["GET"], strict_slashes=False)
def get_status():
  """
  get server status
  """
  return jsonify({"status": "Ok"}), 200

@app_views.route("/stats", strict_slashes=False)
def user_number():
  """
  get the numbers of users in db
  """
  from models.user import User
  stats = {}
  stats["user"] = User.count()
  return jsonify({"stats": stats}), 200

@app_views.route("/unauthorized", strict_slashes=False)
def user_unauthorized():
  """
  the user is not authorized
  """
  abort(401)

@app_views.route("/forbidden", strict_slashes=False)
def forbidden():
  """
  forbidden route - user is authorized but not allowed to access this route
  """
  abort(403)
