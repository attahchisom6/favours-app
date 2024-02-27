#!/usr/bin/env python3
"""
Database storage microservive to manage db operation (manage api's that routes to our database
"""
from flask import Flask, jsonify, request
import models
from models.engine.db_storage import DBStorage, classes
from models.base_model import BaseModel, Base
from os import getenv
from models import storage

"""db_user = getenv("FAVOURS_DB_USER")
db_password = getenv("FAVOURS_DB_PWD")
db_name = getenv("FAVOURS_DB_NAME")
db_host = getenv("FAVOURS_DB_HOST")"""

app = Flask(__name__)
"""storage = DBStorage(
    db_user=db_user,
    db_password=db_password,
    db_host=db_host,
    db_name=db_name
  )"""
# storage.reload()


@app.route("/objects", methods=["GET"], strict_slashes=False)
def get_obj():
  args = request.args
  cls, id = args.get("cls"), args.get("id")
  obj, all_objs = None, None
  if cls:
    if id:
      obj = storage.get(cls, id)
    else:
      all_objs = storage.all(cls)
  else:
    all_objs = storage.all()

  if obj:
    print(obj)
    # return jsonify(obj.__dict__)
  elif all_objs:
    print([obj for obj in all_objs])
    # return jsonify([obj.__dict__ for obj in all_objs])


@app.route("/create/<cls>", methods=["POST"], strict_slashes=False)
def create_object(cls):
  """
  creates an object/instance of the specified class cls and store it in the database
  """
  data = request.json
  if data:
    for key in classes:
      if key == cls:
        Cl = classes[key]
        instance = Cl(**data)
        instance.save()
        return jsonify({"message": "instance created successfully"}), 201
  else:
    return jsonify({"message": "instance creation failed, no data provided!"})


@app.route("/update/<cls>/<id>", methods=["PUT"], strict_slashes=False)
def update_object(cls, id):
  """
  create object and store them in the database
  """
  data = request.json
  obj = storage.get(cls, id)
  if obj:
    if data:
      for key, value in data.items():
        if hasattr(obj, key):
          print("{obj} has key {key} and value {value}")
          setattr(obj, key, value)
      storage.save()
      return jsonify({"message": f"{cls} instance updated succesfully"}), 201
    else:
      return jsonify({"message": "No data provided, provide data to update"}), 400
  else:
    return jsonify({"message": "No object in Database availaible for update"}), 404

@app.route("/delete/<cls>/<id>", methods=["DELETE"], strict_slashes=False)
def delete_object(cls, id):
  """
  delete an object from the database
  """
  obj = storage.get(cls, id)
  if obj:
    obj.delete()
    storage.save()
    return jsonify({"message": f"object with id, {obj.id} has been successfully delected"}), 201
  else:
    return jsonify({"message": "Cannot delete objet. bject not found!"}), 404


if __name__ == "__main__":
  if models.storage_t == "db":
    app.run(host="0.0.0.0", port=5000, debug=True)
  else:
    print('App can only run in "db" enviroment')
