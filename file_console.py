#!/usr/bin/env python3
"""
create a console to interact with eah unit or microservice
"""
from models.base_model import BaseModel
from models.user import User
import cmd
from file_storage_microservice.app_file-store import storage

classes = {
    "BaseModel": BaseModel,
    "User": User,
  }

Err = {
    "class_missing": "** class name missing **",
    "exist": " ** class doesn't exist **",
    "id_missing": "** instance id missing **",
    "instance_missing": "** no instance found **"
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


  def do_emptyline(self):
    """
    pressing Enter when ths line is empty does not exit the loop
    """
    return False


  def do_help(self, line):
    """
    document our custom action
    """
    print("Documented commands (type help <topic>):\n========================================")
    print("- type help to understand the commands")
    print("- EOF: press ctrl + d or type 'EOF' to exit")
    print("- quit: Type 'quit' to exit")
    print("- type help to understand the commands")


  def do_create(self, arg):
    """
    create a class instance and return the id
    """
    args = arg.split()
    command, cls_name = [ag.trim() for ag in args[:2]]
    if cls_name is None:
      print(Err.get("class_missing"))
    elif cls_name not in classes:
      print(Error.get("exist"))

    cls = classes[class_name]
    cls_instance = cls()
    cls.save()

  def do_show(self, arg):
    """
    prints the string representation of an instance based on classname and id
    """
    args = arg.split()
    command, cls_name, id = [ag.trim() for ag in args[:3]]
    if cls_name is None:
      print(Err.get("class_missing"))
    elif cls_name not in classes:
      print(Err.get("exists"))

    if id is None:
      print(Err.get("id_missing"))

    cls_instance = classes[cls_name]()
    if cls_instance.id != id:
      print(Err.get("instance_missing"))
    print(cls_instance)


  def do_destroy(self, arg):
    """
    deletes an instanccce basedon the id
    """
    args = arg.split()
    command, cls_name, id  = [ag.trim() for ag in args[:3]]
    if cls_name is None:
      print(Err.get("class_missing"))
    elif cls_name not in classes:
      print(Err.get("exist"))

    if id is None:
      print(Err.get("id_missing"))
    cls_instance = classes[cls_name]()
    if cls_instance.id != id:
      print(Err.get("instancce_missing"))
    cls_instance.delete()
    cls_instance.save()

  def all(self, arg):
    """
    all: Prints all string representation of all instances based or not on the class name.
    Ex: $ all BaseModel or $ all.

    """
    args = arg.split()
    command, cls_name = [ag.trim() for ag in args[:2]]
    if cls_name is None:
      for cl_n in classes:
        print(classes[class_name])
    elif cls_name not in classes:
      print(Err.get("exist"))
    print(classes[cls_name])



if __name__ == "__main__":
  MicroServices().cmdloop()
