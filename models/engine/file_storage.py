#!/usr/bin/python3
""" Define FileStorage Class that serializes instances to a JSON file
and deserializes JSON file to instances"""

import json
import os.path
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.review import Review


class FileStorage:
    """define FileStorage class"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """return dictionary of objects

        Returns:
            dict: dictionary of objects
        """
        return self.__objects

    def new(self, obj):
        """add to objects to a dictionary

        Args:
            obj (any): object
        """
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """
        Serialize __objects to the JSON file
        """
        with open(self.__file_path, mode="w") as f:
            dict_storage = {}
            for k, v in self.__objects.items():
                dict_storage[k] = v.to_dict()
            json.dump(dict_storage, f)

    def return_class(self):
        """return all known classes in the dict form

        Returns:
            dict: dictionary of classes
        """
        the_class = {"BaseModel": BaseModel,
                     "User": User,
                     "Place": Place,
                     "City": City,
                     "Review": Review,
                     "Amenity": Amenity,
                     "State": State}
        return the_class

    def reload(self):
        """deserialize json from json file"""
        dict_from_json = None
        if os.path.exists(self.__file_path):
            try:
                with open(self.__file_path, "r") as json_file:
                    dict_from_json = json.load(json_file)
            except FileNotFoundError:
                return
        else:
            return
        dict_from_json = {k: self.return_class()[v["__class__"]](**v)
                          for k, v in dict_from_json.items()}
        self.__objects = dict_from_json
