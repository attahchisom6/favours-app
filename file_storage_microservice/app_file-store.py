#!/usr/bin/env python3
"""
app to run and access file storage
"""
from flask import Flask, jsonify, request
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()

app = Flask(__name__)

@app.route("/<cls>", methods=["GET"], strict_slashes=False)
def get_objects(cls):
  """
  fetch all class instances matching cls
  """
  objects = storage.all(cls)
  return jsonify({cls: [obj.to_dict() for obj in objects.values()]}), 200


@app.route("/create", methods=["POST"], strict_slashes=False)
def create_basemodel_instance():
  """
  creates a basemodel instance to post
  """
  data = request.json
  if data:
    basemodel_instance = BaseModel(**data)
    basemodel_instance.save()
    return jsonify({"message": "instance created successfully"}), 201
  else:
    return jsonify({"message": f"No data parsed: here data is {data}"}),201
  

@app.route("/update/<cls>/<id>", methods=["POST"], strict_slashes=False)
def update_basemodel_instance(cls, id):
  """
  update the basemodel instance
  """
  all_obj = storage.get(cls, id)
  data = request.json
  if all_obj:
    for key, value in data:
      if key in all_obj:
        all_obj[key] = value
    return jsonify({"message": "base_model instances updated succesfully"}), 201
  else:
    return jsonify({"message": "Nodata  found for update"}), 404


@app.route("/delete/<cls>/<id>", methods=["DELETE"], strict_slashes=False)
def delete_basemodel_instance(cls, id):
  """
  delea=te a basemodel instance
  """
  all_obj = storage.get(cls, id)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
