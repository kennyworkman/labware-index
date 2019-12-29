"""
registry.py
~~~~~~~~~~~
Defines the Registry class.
"""

import os
import shutil
import pickle
from .error import ExistingRegistryError
from .labware import Labware


class Registry():

    """The Registry for Labware types.

    Persistence is maintained by a file system organized as follows:

    * A directory located in the **current working directory** named
     `./.labware`.
    * Within this directory, serialized Labware objects are stored in files
     named after their respective Secure Hash Algorithm (SHA-1) ids.
    * A serialized mapping of unique hash ids to user-defined names is
    kept in `./.labware/index`

    NOTE: If you built pyindex as a package, the current working directory will
    be somewhere in your site-packages directory (probably associated with some
    virtual environment), as will your persisted data. Rebuilding pyindex will
    *delete all such files*.

    """

    def __init__(self):
        """Creates a fresh Registry in the current working directory.

        The *existence* of a Registry is defined simply by the existence of a
        `.labware` directory in the current working directory; attempting to
        instantiate a Registry with this directory present will result in an
        error.

        Deleting this `.labware` folder will permanently wipe data from the
        indexing tool. A new Registry can be created at this point.
        """

        self.obj_dir = os.path.join(os.path.dirname(__file__), '..',
                                    '.labware')
        if (os.path.exists(self.obj_dir)):
            raise ExistingRegistryError("A Registry already exists in the"
                                        " working directory. Remove the"
                                        " .labware directory to create"
                                        " a new one.")
        else:
            os.makedirs(self.obj_dir)

        # Serializing an empty HashMap saves future checks for object existence
        # when loading from file.
        self.index = os.path.join(self.obj_dir, 'index')
        with open(self.index, 'wb+') as f:
            map = {}
            pickle.dump(map, f)

    def add(self, labware, name=None):
        """Adds a Labware object to the Registry.

        :param name: User-defined name to identify the labware.
        :type name: str
        :param labware: The Labware object being indexed.
        :type labware: Labware
        """
        labware.save(self, name)

    def add_json(self, name, json_data):
        """Adds a Labware object to the Registry using JSON data.

        :param name: User-defined name to identify the labware.
        :type name: str
        :param json_data: Valid JSON data with correct number and type of
         fields. **Note**: thorough documentation of what constitutes *valid*
         can be found in the `Labware` class.
        :type json_data: JSON
        """
        labware = Labware(json_data)
        self.add(labware, name)

    def get(self, name):
        """Retrieves a Labware object from the Registry.

        :param name: The user-defined name associated with the desired Labware
         type.
        :type name: str
        :returns: The desired Labware type.
        :return type: Labware.
        """
        map = None
        with open(self.index, "rb") as f:
            map = pickle.load(f)

        try:
            hash_id = map[name]
        except KeyError as e:
            raise ValueError("{} does not exist in this"
                             " Registry.".format(name))

        obj_file = os.path.join(self.obj_dir, hash_id)
        with open(obj_file, "rb") as f:
            labware = pickle.load(f)
        return labware

    def remove(self, name):
        """Removes a Labware object from the Registry by name.

        :param name: The user-defined name associated with the Labware to
         remove.
        :type name: str
        """
        map = None
        with open(self.index, "rb") as f:
            map = pickle.load(f)

        try:
            hash_id = map[name]
        except KeyError as e:
            raise ValueError("{} does not exist in this"
                             " Registry.".format(name))

        # Remove mapping from index _and_ remove serialized object file.
        del map[name]
        with open(self.index, "wb+") as f:
            pickle.dump(map, f)
        obj_file = os.path.join(self.obj_dir, hash_id)
        os.remove(obj_file)

    def list(self):
        """List the Labware types currently indexed.

        :returns: A list of user-defined names.
        :return type: list
        """
        map = None
        with open(self.index, "rb") as f:
            map = pickle.load(f)
        return list(map.keys())

    def wipe(self):
        """Removes all data stored in this Registry.

        **This is a dangerous and irreversible operation.**
        """
        shutil.rmtree(self.obj_dir)

    def __repr__(self):
        """Representation of Registry"""
        rep = "\nLabware Registry\n"
        rep += "________________\n"

        for labware in self.list():
            rep += labware
            rep += "\n"

        return rep
