#!/usr/bin/env python
"""
Define the users platform
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, LargeBinary
import jwt


class User(BaseModel, Base):
  """
  users class
  """
  if models.storage_t == "db":
    __tablename__ = "users"
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    _password = Column("password", String(128), nullable=False)
    email = Column(String(128), nullable=False)
  else:
    first_name = ""
    last_name = ""
    email = ""
    _password = ""


  def __init__(self, *args, **kwargs):
    """
    initializing variables
    """
    super().__init__(*args, **kwargs)


  @property
  def password(self):
    return self._password

  @password.setter
  def password(self, value):
    self._password = jwt.encode({"password": value}, key="SECRET", algorithm="HS256")


  def __setattr__(self, name, value):
    """
    method to hash the password in jwt
    """
    if models.storage_t != "db":
      if name =="password":
        value = jwt.encode({name: value}, key="2nd_SECRET", algorithm="HS384")
    super().__setattr__(name, value)
