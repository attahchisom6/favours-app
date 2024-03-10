#!/usr/bin/env python3
"""
handle user related operations using RESTFUL API APPROACH
"""
from Authentication_microservice.api.v1.views import app_views
from models.user import User
from flask import jsonify, request
from typing import Dict
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
    return None

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


@app_views.route("/db_users/<id>", methods=["GET"], strict_slashes=False)
def get_db_user(id):
  """
  returns a user from the database
  """
  res = None
  try:
    res = requests.get(f"{db_url}/db_objects?cls=User&id={id}")
  except:
    res = None

  if res is not None:
    return res.json()
 

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
  """
  creates a user and store in the file
  """
  data = request.get_json()

  if not isinstance(data, dict):
    return jsonify({"messsage": "This endpoint requires nonempty object of type dict"}), 400
  res = None
  try:
    res =  requests.post(f"{file_url}/create/User", json=data)
  except Exception as e:
    return jsonify({"message": f"Failed to create a user for the database: {str(e)}"}), 500

  if res is not None:
    return jsonify(res.json()), res.status_code 


@app_views.route("/db_users", methods=["POST"], strict_slashes=False)
def create_db_user():
  """
  creates a user and store in the database
  """
  data = request.get_json()

  if not isinstance(data, dict):
    return jsonify({"message": "This endpoint requires nonempty object of type dict"}), 400

  res = None
  try:
    res = requests.post(f"{db_url}/create/User", json=data)
    # print(f"({res.text()} {res.status_code})")
  except Exception as e:
    return jsonify({"message": f"Failecd to create a user instance for the database: {str(e)}"}), 500

  if res is not None:
    return jsonify(res.json()), res.status_code


@app_views.route("/users/<id>", methods=["PUT"], strict_slashes=False)
@app_views.route("/users", methods=["PUT"], strict_slashes=False)
def update_user_in_file(id):
  """
  updates user instances stored in file
  """
  data = request.get_json()

  if not isinstance(data, dict):
    return jsonify({"message": "This endpoint requires nonempty objects of type dict"}), 400

  res = None
  try:
    res = requests.put(f"{file_url}/update/User/{id}", json=data)
  except Exception as e:
    return jsonify({"Failed to update the user with id {id}: {str(e)}"}), 500

  if res is not None:
    return jsonify(res.json()), res.status_code


@app_views.route("/db_users/<id>", methods=["PUT"], strict_slashes=False)
@app_views.route("/users", methods=["PUT"], strict_slashes=False)
def update_user_in_db(id):
  """
  updates user instances stored in file
  """
  data = request.get_json()

  if not isinstance(data, dict):
    return jsonify({"message": "This endpoint requires nonempty objects of type dict"}), 400

  res = None
  try:
    res = requests.put(f"{db_url}/update/User/{id}", json=data)
  except Exception as e:
    return jsonify({"Failed to update the user with id {id}: {str(e)}"}), 500

  if res is not None:
    return jsonify(res.json()), res.status_code


@app_views.route("/users/<id>", methods=["DELETE"], strict_slashes=False)
def delete_obj_from_file(id):
  """
  delete the object with `id` from the file storage
  """
  res = None
  try:
    res = request.delete(f"{file_url}/User/{id}")
  except Exception as e:
    return jsonify({"message": "Could not delete the item of concern: {str(e)}"})
  
  if res is not None:
    return jsonify(res.json()), res.status_code


@app_views.route("/db_users/<id>", methods=["DELETE"], strict_slashes=False)
def delete_obj_from_db(id):
  """
  delete the object with `id` from the file storage
  """
  res = None
  try:
    res = request.delete(f"{db_url}/User/{id}")
  except Exception as e:
    return jsonify({"message": "Could not delete the item of concern: {str(e)}"})

  if res is not None:
    return jsonify(res.json()), res.status_code
