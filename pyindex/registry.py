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

        The *existence* of a Registry is defined simply by a
        `.labware` directory in the current working directory; attempting to
        instantiate a Registry with this directory present will "load" this
        data into the new object.

        Deleting this `.labware` folder will permanently wipe data from the
        indexing tool. A new Registry can be created at this point.
        """

        self.obj_dir = os.path.join(os.path.dirname(__file__), '..',
                                    '.labware')
        self.index = os.path.join(self.obj_dir, 'index')

        if (os.path.exists(self.obj_dir)):
            print("\nExisting registry loaded from disk:")
            print(self)
        else:
            os.makedirs(self.obj_dir)
            with open(self.index, 'wb+') as f:
                map = {}
                pickle.dump(map, f)

    def add(self, labware, name=None):
        """Adds a Labware object to the Registry.

        This method is intended to be used internally. While one could
        construct a Labware object, the use of a JSON object or file with the
        `add_json()` or `add_file()` methods is probably more convenient and
        easier to use. A JSON template is provided in the `Labware` class
        documentation.

        :param name: User-defined name to identify the labware.
        :type name: str
        :param labware: The Labware object being indexed.
        :type labware: Labware
        """
        labware.save(self, name)

    def add_json(self, name, json_data):
        """Adds a Labware object to the Registry using raw JSON data.

        :param name: User-defined name to identify the labware.
        :type name: str
        :param json_data: Valid JSON data with correct number and type of
         fields. **Note**: thorough documentation of what constitutes *valid*
         can be found in the `Labware` class.
        :type json_data: JSON
        """
        labware = Labware(json_data)
        self.add(labware, name)

    def add_file(self, name, file):
        """Adds a Labware object to the Registry using a .json file.

        :param name: User-defined name to identify the labware.
        :type name: str
        :param file: A path to a file containing valid JSON data (validity
        specified in `add_json` function)
        :type file: str
        """

        with open(file, "r") as f:
            json_data = f.read().replace('\n', '')
        self.add_json(name, json_data)

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
        """List the Labware types currently indexed by user-defined names.

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
        """Representation of the Registry"""

        rep = "\nLabware Registry\n"
        rep += "________________\n\n"

        for labware in self.list():
            rep += "* "
            rep += labware
            rep += " --> "
            rep += self.get(labware).__repr__()
            rep += "\n\n"

        return rep

    def __eq__(self, other):
        """Identical attributes between objects is sufficient for equality."""
        return self.__dict__ == other.__dict__
