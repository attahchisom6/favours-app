#!/usr/bin/env python3
"""
create a console to interact with eah unit or microservice
"""
from models.base_model import BaseModel
from models.user import User
import cmd
from file_storage_microservice.app_file_store import storage
import os
import json
import re

classes = {
    "BaseModel": BaseModel,
    "User": User,
  }

Err = {
    "class_missing": "** class name missing **",
    "exist": " ** class doesn't exist **",
    "id_missing": "** instance id missing **",
    "instance_missing": "** no instance found **",
    "attr_name": "** attribute name missing **",
    "attr_value": "** value missing **"
  }


def strip_quotes(text):
  """
  strip a double quote " from beginning and ending of a text
  """
  return re.sub(r'^\"|\"$', '', text)


class MicroServices(cmd.Cmd):
  """
  microservice unit class
  """

  # pls note that apart from the get method, every instance returned from the file storage using any other method is a dictionary whose values are instances of clases
  # The get method returns the instance itself (i.e not a dict, so no keys here), we can get the dictionary representation of the instance using __dict__

  prompt = "(micro_unit) "

  def do_EOF(self, line):
    """
    exist the program when ctrl + D is pressed
    """
    return True


  def do_quit(self, line):
    """
    quit the program, when the string 'quit' typed and Enter key is pressed
    """
    return True


  def emptyline(self):
    """
    pressing Enter when ths line is empty does not exit the loop
    """
    return False


  def do_create(self, arg):
    """
    create a class instance and return the id
    Usage:
      create <class_name>
    """
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))
        return False
    except IndexError:
      print(Err.get("class_missing"))
      return False

    cls = classes[cls_name]
    cls_instance = cls()
    cls_instance.save()
    print(cls_instance.id)


  def do_show(self, arg):
    """
    prints the string representation of an instance based on classname and id
      Usage:
        show <class> <class_id>
    """
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))
        return False

      try:
        id = strip_quotes(args[1].strip())
        if id:
          instance = storage.get(cls_name, id)
          if not instance:
            print(Err.get("instance_missing"))
            return False
          else:
            print(instance)
      except IndexError:
        print(Err.get("id_missing"))
        return False
    except IndexError:
      print(Err.get("class_missing"))
      return False


  def do_destroy(self, arg):
    """
    deletes an instanccce based on the classname and id
    Usage:
      destroy <class_name> <id>
    """
    id, cls_name = None, None
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))
        return False

      try:
        id = strip_quotes(args[1].strip())
      except IndexError:
        print(Err.get("id_missing"))
        return False
    except IndexError:
      print(Err.get("class_missing"))
      return False

    if id and cls_name:
      instance = storage.get(cls_name, id)
      if instance:
        instance.delete()
      else:
        print(Err.get("instance_missing"))
      storage.save()


  def do_all(self, arg):
    """
    all: Prints all string representation of all instances based or not on the class name.
    Usgage:
      all <class> or simply all
        Ex: $ all BaseModel or $ all
    """
    instances = None
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))
        return False
      elif cls_name:
        instances = storage.all(cls_name)
    except IndexError:
      instances = storage.all()

    array = []
    for value in instances.values():
      array.append(str(value))
    print("[", end="")
    print(", ".join(array), end="")
    print("]")


  def do_update(self, arg):
    """
    update an instance with a given attribute name to a given value based on its id and class name
    Ex: update BaseModel 1277 email "eome@email"
    Usage:
      update <class> <id> <attr_name> <value>
    """
    # instance = None
    # attr_name, attr_value, id = "", None, None
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))
        return False
      try:
        id = strip_quotes(args[1].strip())
        instance = storage.get(cls_name, id)
        if instance:
          try:
            attr_name = args[2].strip()
            try:
              attr_value = strip_quotes(args[3].strip())
            except IndexError:
              print(Err.get("attr_value"))
              return False
          except IndexError:
            print(Err.get("attr_name"))
            return False
          try:
            attr_type = type(getattr(instance, attr_name))
            if attr_type is int:
              attr_value = int(attr_value)
            elif attr_type == float:
              attr_value = float(attr_value)
            else:
              attr_value = attr_value
            setattr(instance, attr_name, attr_value)
          except AttributeError:
            pass
          instance.save()
        else:
          print(Err.get("instance_missing"))
      except IndexError:
        print(Err.get("id_missing"))
        return False
    except IndexError:
      print(Err.get("class_missing"))
      return False


if __name__ == "__main__":
  MicroServices().cmdloop()
