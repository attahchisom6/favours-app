#!/usr/bin/env python3
"""
A model or standard from which other models are defines
"""
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from typing import List, TypeVar

if models.storage_t == "db":
  Base = declarative_base()
else:
  Base = object

time_format = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
  """
  The Mother or principal class
  """
  if models.storage_t == "db":
    id = Column(String(128), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

  def __init__(self, *args, **kwargs):
    """
    initializing base definintion, type, and  properties of all instances of BaseModel
    """
    if kwargs:
      for key, value in kwargs.items():
        if key != "__class__":
          setattr(self, key, value)

      if kwargs.get("created_at", None) and type(self.created_at) is str:
        self.created_at = datetime.strptime(kwargs["created_at"], time_format)
      else:
        self.created_at = datetime.utcnow()

      if kwargs.get("updated_at", None) and type(self.updated_at) is str:
        self.updated_at = datetime.strptime(self.updated_at, time_format)
      else:
        self.updated_at = datetime.utcnow()

      if kwargs.get("id", None) is None:
        self.id = str(uuid.uuid4())

    else:
      self.id = str(uuid.uuid4())
      self.created_at = datetime.utcnow()
      self.updated_at = datetime.utcnow()


  def __str__(self):
    """
    returns a string representation of BaseModel instances
    """
    dict_repr = {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}
    return "[{:s}] ({:s}) {}".format(
        self.__class__.__name__,
        self.id,
        dict_repr
      )

  def save(self):
    """
    update the update_at attribute with the current time
    """
    setattr(self, "updated_at", datetime.utcnow())
    models.storage.new(self)
    models.storage.save()

  def to_dict(self, fs_indicator=None):
    """
    returns a dictionary representation of basemodel instances
    """
    obj_dict = self.__dict__.copy()
    obj_dict["__class__"] = self.__class__.__name__

    if obj_dict.get("created_at"):
      obj_dict["created_at"] = obj_dict["created_at"].strftime(time_format)

    if obj_dict.get("updated_at"):
      obj_dict["updated_at"] = obj_dict["updated_at"].strftime(time_format)

    if "_sa_instance_state" in obj_dict:
      del obj_dict["_sa_instance_state"]

    if fs_indicator is None:
      if "_password" in obj_dict:
        del obj_dict["_password"]

    return obj_dict

  def delete(self):
    """
    delete current instance from storage
    """
    models.storage.delete(self)


  @classmethod
  def search(cls, attributes: dict = {}) -> List[TypeVar("User")]:
    """
    searches and gets a class object bassed on the attributes
    """
    all_objs = models.storage.all(cls)
    def _search(obj):
      if len(attributes) == 0:
        return True

      for key, value in attributes.items():
        if getattr(obj, key) != value:
          return False
      return True

    return list(filter(_search, all_objs.values()))
