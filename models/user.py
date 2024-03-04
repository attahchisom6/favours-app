#!/usr/bin/env python
"""
Define the users platform
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from typing import List, TypeVar
import bcrypt


class User(BaseModel, Base):
  """
  users class
  """
  if models.storage_t == "db":
    __tablename__ = "users"
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    _password = Column(String(128), nullable=False)
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
  def password(self, password):
    self._password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


  def is_valid_password(self, password):
    """
    checks if the password passed by the user is valid
    """
    if password is None or type(password) is not str:
      return False

    # Note we call a property method without parenthesis
    if self.password is None:
      return None

    return bcrypt.checkpw(password.encode("utf-8"), self.password)

  @classmethod
  def search(cls, attributes: dict = {}) -> List[TypeVar("User")]:
    """
    searches and gets a user object bassed on the attributes
    """
    all_obj = models.storage.all(cls)
    def _search(obj):
      if len(attributes) == 0:
        return True

      for key, value in attributes.items():
        if getattr(obj, key) != value:
          return False
      return True

    return list(filter(_search, all_objs.values()))

  def display_name(self):
    """
    display names based on email, first_name and last_names
    """
    if self.email is None and self.first_name is None and self.last_name is None:
      return ""

    if not self.first_name and not self.last_name:
      return self.email

    if not self.first_name:
      return self.last_name
    elif not self.last_name:
      return self.first_name
    else:
      return f"{self.first_,name} {self.last_name}"
