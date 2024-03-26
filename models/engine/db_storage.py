#!/usr/bin/env python3
"""
Database interaction and Management module
"""
from models.base_model import BaseModel, Base
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
# import bcrypt


classes = {
    "User": User
  }


class DBStorage:
  """
  Database storage
  """
  __session = None
  __engine = None

  def __init__(self): #  db_user=None, db_name=None, db_host=None, db_password=None):
    """
    initializing db variables
    """
    # if db_user is None and db_name is None and db_host is None and db_password is None:
    db_user = getenv("FAVOURS_DB_USER")
    db_password = getenv("FAVOURS_DB_PWD")
    db_name = getenv("FAVOURS_DB_NAME")
    db_host = getenv("FAVOURS_DB_HOST")
    self.__engine = create_engine(
        "mysql+mysqldb://{}:{}@{}/{}".format(
          db_user,
          db_password,
          db_host,
          db_name
        )
      )

    if db_name == "test":
      Base.metadata.drop_all(self.__engine)

  def new(self, obj):
    """
    add a new object to the database and commit it in ths currenr session
    """
    self.__session.add(obj)


  def all(self, cls=None):
    """
    return all instances from rhe database
    """
    obj_dict = {}

    def parse_objs(objs):
      """
      parse an obj in the dictionary format we want
      """
      if objs is None:
        return obj_dict
      for obj in objs:
        key = f"{obj.__class__.__name__}.{obj.id}"
        obj_dict[key] = obj
      return obj_dict

    for cl in classes:
      if cls is None or cls is classes[cl] or cls == cl:
        # table = classes[cls].__table__
        objs = self.__session.query(classes[cl]).all()
        parse_objs(objs)
    return obj_dict


  def save(self):
    """
    save an instance to the databasd
    """
    self.__session.commit()


  def reload(self):
    """
    reload: load data from database and initialize all tables
    """
    Base.metadata.create_all(self.__engine)
    session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    Session = scoped_session(session_factory)
    self.__session = Session

  def close(self):
    """
    remove thevcurrenf session from session cache
    """
    self.__session.remove()


  def delete(self, obj=None):
    """
    remove an object from db
    """
    if obj is not None:
      self.__session.delete(obj)


  def get(self, cls, id):
    """
    get an item from the database
    """
    # table = classes[cls].__table__
    if classes[cls] is not None:
      return self.__session.query(classes[cls]).filter_by(id=id).first()
    else:
      return None


  def count(self, cls=None):
    """
    count the number of objects a class has in the darabase
    """
    db_objects = self.all(cls)
    return len(db_objects)

  # @classmethod
  def search_db(self, clss, attributes={}):
    """
    return the instances with the ptovided attributes
    """
    if classes[clss] is not None:
      return self.__session.query(classes[clss]).filter_by(**attributes).all()
    return None
