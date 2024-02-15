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
    return f"No data parsed: {data}"


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
