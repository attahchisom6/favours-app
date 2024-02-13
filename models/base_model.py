#!/usr/bin/env python3
"""
A model or standard from which other models are defines
"""
import models
from sqlalchemy import Column, String, Datetime, create_engine
from sqlalchemy.orm.ext import declarative_base
import datetime
import uuid

if models.storage_t == "db":
  Base = declarative_base()
else:
  Base = object

time_format = "%Y-%m-%dT%H%:%M:%S.%f"

  class BaseModel:
    """
    The Mother or principal class
    """
    id = Column(String(128), primary_key=True)
    created_at = Column(Datatime, datetime.utcnow)
    updated_at = Column(Datetime, datetime.utcnow)

    def __init__(self, *args, **kwargs):
      """
      initializing base definintion, type, and  properties of all instances of BaseModel
      """
      if kwargs:
        for key, value in kwargs.items():
          if "__class__" not in kwargs:
            setattr(self, key, value)

        if "created_at" in kwargs and type(self.created_at) is str:
            self.created_at = strptime(kwargs["created_at"], time_format)

        if self.updated_at and type(self.updated_at) is str:
            self.updated_at = strptime(self.updated_at, time_format)

          if id is None:
            id = uuid.uuid4()

