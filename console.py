#!/usr/bin/python3
"""Defines the entry point of the command interpreter."""
import cmd
import re
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """ Command interpreter class."""

    prompt = "(hbnb) "
    cls = {"BaseModel", "User", "Place", "City", "Amenity", "Review", "State"}

    def do_quit(self, arg):
        """Command quit to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF to exit the program."""
        print()
        return True

    def emptyline(self):
        """ Empty line and do nothing."""
        pass

    def do_create(self, arg):
        """ Creates a new instance of BaseModel."""
        if not arg:
            print("** class name missing **")
        else:
            try:
                new_inst = eval(arg)()
                new_inst.save()
                print(new_inst.id)
            except NameError:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        ar = arg.split()
        if not ar:
            print("** class name missing **")
        else:
            try:
                c_name = ar[0]
                if c_name not in HBNBCommand.cls:
                    print("** class doesn't exist **")
                elif len(ar) < 2:
                    print("** instance id missing **")
                else:
                    obj_key = "{}.{}".format(c_name, ar[1])
                    all_objs = storage.all()
                    if obj_key in all_objs:
                        print(all_objs[obj_key])
                    else:
                        print("** no instance found **")
            except IndexError:
                print("** instance id missing **")

    def do_destroy(self, arg):
        """Deletes an instance and save the change into thr JSON file."""
        ar = arg.split()
        if not ar:
            print("** class name missing **")
        else:
            try:
                c_name = ar[0]
                if c_name not in HBNBCommand.cls:
                    print("** class doesn't exist **")
                elif len(ar) < 2:
                    print("** instance id missing **")
                else:
                    obj_key = "{}.{}".format(c_name, ar[1])
                    all_objs = storage.all()
                    if obj_key in all_objs:
                        del all_objs[obj_key]
                        storage.save()
                    else:
                        print("** no instance found **")
            except IndexError:
                print("** instance id missing **")

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        ar = arg.split()
        all_objs = storage.all()
        if not ar:
            print([str(obj) for obj in all_objs.values()])
        else:
            try:
                c_name = ar[0]
                if c_name not in HBNBCommand.cls:
                    print("** class doesn't exist **")
                else:
                    objs_cls = [
                        str(obj)
                        for key, obj in all_objs.items()
                        if key.startswith(c_name + ".")
                    ]
                    print(objs_cls)
            except IndexError:
                print("** class name missing **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        args = arg.split()
        if len(args) >= 4:
            key = "{}.{}".format(args[0], args[1])
            if key in storage.all():
                obj = storage.all()[key]
                attribute_name = args[2]
                new_value = args[3].strip('"').strip("'")
                if hasattr(obj, attribute_name):
                    attribute_type = type(getattr(obj, attribute_name))
                    if attribute_type == int:
                        new_value = int(new_value)
                    elif attribute_type == float:
                        new_value = float(new_value)
                    setattr(obj, attribute_name, new_value)
                    obj.save()
                else:
                    print("** attribute name doesn't exist **")
            else:
                print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
