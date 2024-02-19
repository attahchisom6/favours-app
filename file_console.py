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

class MicroServices(cmd.Cmd):
  """
  microservice unit class
  """
  prompt = "(micro_unit) "

  def do_EOF(self, line):
    """
    exist the program when ctrl + D is pressed
    """
    return True


  def do_quit(self, line):
    """
    quit the program
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
        id = args[1].strip()
        if id:
          instance = storage.get(cls_name, id)
          if not instance:
            print(Err.get("instance_missing"))
            return False
          else:
            print(instance)
      except:
        print(Err.get("id_missing"))
        return False
    except:
      print(Err.get("class_missing"))
      return False


  def do_destroy(self, arg):
    """
    deletes an instanccce based on the classname and id
    Usage:
      destroy <class_name> <id>
    """
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))

      try:
        id = args[1].strip()
      except IndexError:
        print(Err.get("id_missing"))
    except ValueError:
      print(Err.get("class_missing"))

    cls_instance = classes[cls_name]()
    if cls_instance.id != id:
      print(Err.get("instancce_missing"))
    cls_instance.delete()
    cls_instance.save()

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


  def update(self, arg):
    """
    update an instance with a given attribute with a given value based on its id and name
    Ex: update BaseModel 1277 email "eome@email"
    Usage:
      update <class> <id> <attr_name> <value>
    """
    args = arg.split()
    try:
      cls_name = args[0].strip()
      if cls_name not in classes:
        print(Err.get("exist"))
      try:
        id = args[1].strip()
        cls_instance = classes[cls_name]()
        if cls_instance.id != id:
          print(Err.get("instance_missing"))
          try:
            attr_name = args[2].strip()
            try:
              attr_value = args[3].strip()
            except:
              print(Err.get("attr_value"))
          except:
            print(Err.get("attr_name"))
      except:
        print(Err.get("id_missing"))
    except ValueError:
      print(Err.get("class_missing"))
    setattr(cls_instance, attr_name, attr_value)
    class_instance.save()



if __name__ == "__main__":
  MicroServices().cmdloop()