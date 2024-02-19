#!/usr/bin/env python3
"""
app to run and access file storage
"""
from flask import Flask, jsonify, request
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage, classes
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


@app.route("/create/<cls>", methods=["POST"], strict_slashes=False)
def create_instance(cls):
  """
  creates a basemodel instance to post
  """
  data = request.json
  if data:
    for key in classes:
      if key == cls:
        Cl =  classes[key]
        instance = Cl(**data)
        instance.save()
        return jsonify({"message": f"{cls} instance created successfully"}), 201
  else:
    return jsonify({"message": "Cannot create an instance, no data provided"}),201
  

@app.route("/update/<cls>/<id>", methods=["PUT"], strict_slashes=False)
def update_basemodel_instance(cls, id):
  """
  update the basemodel instance
  """
  obj = storage.get(cls, id)
  data = request.json
  if obj:
    for key, value in data.items():
      if hasattr(obj, key):
        setattr(obj, key, value)
    obj.save()
    return jsonify({"message": f"{cls} instances updated succesfully"}), 201
  else:
    return jsonify({"message": "instance Missing"}), 404


@app.route("/delete/<cls>/<id>", methods=["DELETE"], strict_slashes=False)
def delete_basemodel_instance(cls, id):
  """
  delea=te a basemodel instance
  """
  obj = storage.get(cls, id)
  if obj:
    storage.delete(obj)
    storage.save()
    return jsonify({"message": f"object with id, {obj.id} deleted succesefully"}), 201
  else:
    return jsonify({"message": "instance missing"}), 404


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
