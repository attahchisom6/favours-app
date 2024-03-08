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
  return the list of all users in the file storage
  """
  res = None
  try:
    res = requests.get(f"{file_url}/objects?cls=User")
  except:
    return None
    
  if res is not None:
    return res.json()


@app_views.route("/db_users", methods=["GET"], strict_slashes=False)
def get_db_users():
  """
  return all users from the database
  """
  res = None
  try:
    res = requests.get(f"{db_url}/db_objects?cls=User")
  except:
    res = None

  if res is not None:
    return res.json()


@app_views.route("/users/<id>", methods=["GET"], strict_slashes=False)
def get_user(id):
  """
  return a given users from the filestorage
  """
  res = None
  try:
    res = requests.get(f"{file_url}/objects?cls=User&id={id}")
  except:
    res = None

  if res is not None:
    return res.json()


@app_views.route("/db_users", methods=["GET"], strict_slashes=False)
def get_db_user():
  """
  return all users from the database
  """
  res = None
  try:
    res = requests.get(f"{db_url}/db_objects?cls=User&id={id}")
  except:
    res = None

  if res is not None:
    return res.json()
