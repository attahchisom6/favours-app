  #!/usr/bin/env python3
"""
serializes our data and stores it in a file
"""
import models
from models.base_model import BaseModel
import json
import jwt
from models.user import User

classes = {
    "User": User,
    "BaseModel": BaseModel
  }


class FileStorage:
  """
  file storage system
  """
  __file_path = "file_store.json"
  __objects_data = {}

  def new(self, obj):
    """
    sets in __objects_data the obj with key <obj class name>.id
    """
    if obj:
      key = obj.__class__.__name__ + "." + obj.id
      self.__objects_data[key] = obj


  def all(self, cls=None):
    """
    return all object in __object_data if no class is specified else all obj in the specigied class
    """
    if cls is not None:
      class_dict = {}
      for key, value in self.__objects_data.items():
        if cls == value.__class__ or cls == value.__class__.__name__:
          class_dict[key] = value
      return class_dict
    return self.__objects_data


  def save(self):
    """
    serializes data and stores it in a file
    """
    json_dict = {}
    for key, value in self.__objects_data.items():
      json_dict[key] = value.to_dict(fs_indicator=1)
      if key == "_password":
        json_dict[key] = json_dict[key].decode("utf-8")
    with open(self.__file_path, "w") as fw:
      json.dump(json_dict, fw)

  def reload(self):
    """
    deserialixes data from the file storage backinto objects_data as instances
    """
    try:
      with open(self.__file_path, "r") as f:
        data = json.load(f)

      for key, value in data.items():
        class_name, obj_id = key.split(".")
        if class_name and class_name in classes:
          class_obj = classes[class_name]
          obj_instance = class_obj(**value)
          self.__objects_data[key] = obj_instance
        else:
          print(f"warning: {class_name} not found in valid class group")
    except:
      pass


  def close(self):
    """
    reload to deserialize json data to objects
    """
    self.reload()

  def delete(self, obj=None):
    """
    delete an object from the objects_data's dictionary if present
    """
    if obj:
      key_to_delete = f"{obj.__class__.__name__}.{obj.id}"
      if key_to_delete in self.__objects_data:
        del self.__objects_data[key_to_delete]
    self.save()


  def get(self, cls=None, id=None):
    """
    method to return an obj in objects_data if present based on the class and id
    """
    if cls and id:
      for key, obj in self.__objects_data.items():
        if key.startswith(cls) and obj.id == id:
          return obj
    return None

  def count(self, cls=None):
    """
    count the number of objs in a given ckass or whole obj in __objects_data if no class is given
    """
    if cls:
      count = len(self.all(cls))
    else:
      count = 0
      for cl in classes:
        count += len(self.all(cl))

    return count
