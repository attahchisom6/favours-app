#!/usr/bin/env python3
"""
create a console to interact with eah unit or microservice
"""
from models.base_model import BaseModel
from models.user import User
from models.user_session import UserSession
import cmd
# from file_storage_microservice.app_file_store import storage
from models import storage
import os
import json
import re
import ast
import importlib

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "UserSession": UserSession,
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


def param_list_parser(params: list) -> dict:
  """
  parse a list into dictionary
  """
  dictt = {}
  if params is None:
    return dictt

  for param in params:
    if "=" in param:
      key, value = param.split("=", 1)
      if value.startswith('"') and value.endswith('"'):
        value = strip_quotes(value).replace("_", " ")
      else:
        try:
          value = int(value)
        except:
          try:
            value = float(value)
          except:
            pass
      dictt[key] = value
  return dictt



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
    kwargs = {}
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))
        return False
    except IndexError:
      print(Err.get("class_missing"))
      return False

    try:
      params = [ag.strip() for ag in arg.split()[1:]]
      if params:
        kwargs = param_list_parser(params)
    except IndexError:
      pass
    
    cls = classes[cls_name]
    cls_instance = cls(**kwargs)
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
      if id == "all":
        instance = storage.get(cls_name)
      else:
        instance = storage.get(cls_name, id)
      if instance:
        if isinstance(instance, list):
          for obj in instance:
            storage.delete(obj)
        else:
          storage.delete(instance)
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
            attr_name = strip_quotes(args[2].strip())
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
            if hasattr(instance, attr_name):
              setattr(instance, attr_name, attr_value)
          except AttributeError as e:
            print(f"The atrr error: {e}")
            pass
          storage.save()
        else:
          print(Err.get("instance_missing"))
      except IndexError:
        print(Err.get("id_missing"))
        return False
    except IndexError:
      print(Err.get("class_missing"))
      return False


  def do_count(self, arg):
    """
    count the number of instances in a given class, else all the instances
    """
    count = 0
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))
        return False
      elif cls_name:
        count = storage.count(cls_name)
    except IndexError:
      count = storage.count()
    print(count)

  def do_reload(self, arg):
    """
    reloads a module to include any changes made in it.
    Usages:
      reload <module1> <module2> ...
    """
    modules = []
    try:
      file_names = arg.split()
      if not file_names:
        print("No files provided for reloading")

      for file in file_names:
        try:
          """module_name, _, package_name = file.rpartition("/")
          if not package_name:
            package_name = None
          module_name = module_name.replace("/", ".")"""
          module = importlib.import_module(file)
          if module:
            modules.append(module)
          else:
            print(f"Cannot import {module}")
        except FileNotFoundError:
          print(f"module not found: {file}")
        except ImportError:
          print(f"Error importing module: {file}")
    except IndexError:
      print("Invalid usage of reload command.")
    
    for module in modules:
      try:
        importlib.reload(module)
        print(f"reloaded module {module.__name__} successfully")
      except Exception as e:
        print(f"Cannot reload {module} module: {e}")
        
  def do_search(delf, arg):
    """
    search a given user object based on its   attribute
    """
    try:
      args = arg.split()
      cls_name = args[0].strip()
      if cls_name and cls_name not in classes:
        print(Err.get("exist"))
        return False
      try:
        attr_name = strip_quotes(args[1].strip())
        if attr_name:
          if not hasattr(classes[cls_name](), attr_name):
              print(f"invalid attribute: '{attr_name}'")
              return False
          try:
            attr_value = strip_quotes(args[2].strip())
          except IndexError:
            print(Err.get("attr_value"))
            return False
          try:
            instance = classes[cls_name].search({attr_name: attr_value})[0]
            if instance:
              print(instance.to_dict())
          except Exception as e:
            print(f"{Err.get('attr_value')}: {e}")
            return False
        else:
          print(Err.get("attr_value"))
      except IndexError:
        print(Err.get("attr_name"))
    except IndexError:
      print(Err.get("class_missing"))
      return False


  def default(self, arg):
    """
    handle new ways of executing cmd commands
    the default method in cmd handles unrecognized commands or input (that's is command not defined earlier
    Usages:
      <class_name>.all()
      <class_name>.create()
      <class_name>".show(<id>)
      <class_name>.destroy(<id>)
      <class_name>.update(<id>, <**kwargs i.e dict_representation>)
      <class_name>.count()
      File.reload(module1, module2, ...)
      <class_name>.search(<**kwargs i.e dict_representation>)
    """
    valid_commands = {
        "all": self.do_all,
        "create": self.do_create,
        "show": self.do_show,
        "destroy": self.do_destroy,
        "update": self.do_update,
        "count": self.do_count,
        "reload": self.do_reload,
        "search": self.do_search
      }

    line = ""
    command = ""
    update_items = []

    arg = arg.strip()
    values = arg.split(".", 1)
    # check if thare is only single dot, if not default to 
    if len(values) != 2:
      cmd.Cmd.default(self, arg)
      return False

    cls_name = values[0]
    command = values[1]

    if command.endswith("()"):
      command = command[:-2]
      if cls_name in classes and command in valid_commands:
        if command == "all" or command == "count" or command == "create":
          line  = f"{cls_name}"

    elif re.match(r'(.+)\((.+)\)', command):
      groups = re.match(r'(.+)\((.+)\)', command)
      command = groups[1]
      id_or_dict = groups[2]

      if cls_name in classes and command in valid_commands:
        if command == "show" or command == "destroy":
          line = f"{cls_name} {id_or_dict}"
        
        elif command == "update" or command == "search":
          id_or_dict_match = re.match('^(.+), (\{.*\})$', id_or_dict)
          if id_or_dict_match:
            id, str_dict = id_or_dict_match.groups()
            if str_dict:
              dictt = ast.literal_eval(str_dict)
              if dictt:
                for attr_name, attr_value in dictt.items():
                  line = f"{cls_name} {id} {attr_name} {attr_value}"
                  update_items.append(line)
        else:
          return False
    
      elif cls_name == "File" and command == "reload":
        str_array = id_or_dict
        array_items = str_array.split(", ")
        if array_items:
          line = " ".join(array_items)

    else:
      return False

    if update_items:
      for line in update_items:
        valid_commands[command](line)
      update_items = []

    try:
      valid_commands[command](line)
    except:
      return False


if __name__ == "__main__":
  MicroServices().cmdloop()
