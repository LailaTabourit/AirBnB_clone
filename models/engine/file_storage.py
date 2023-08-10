#!/usr/bin/python3
""" Defines FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User

class FileStorage:
    """ Serialize instances to a JSON file and deserializes JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """ Sets in __Objects the obj with key<obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """ Serealizes __objects to JSON file."""
        obj_dict = {}
        for key, value in self.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """ Deserializes the JSON file"""
        try:
            with open(self.__file_path, 'r') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name = value["__class__"]
                    del value["__class__"]
                    self.new(eval(class_name)(**value))
        except FileNotFoundError:
            return
