"""
registry.py
~~~~~~~~~~~
Defines the Registry class.
"""

import os
import shutil
import pickle
from .error import ExistingRegistryError


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
        """Creates a fresh registry in the current working directory."""

        self.obj_dir = os.path.join(os.path.dirname(__file__), '..',
                                    '.labware')
        print(self.obj_dir)
        if (os.path.exists(self.obj_dir)):
            raise ExistingRegistryError("A Registry already exists in the"
                                        " working directory. Remove the"
                                        " .labware directory to create"
                                        " a new one.")
        else:
            os.makedirs(self.obj_dir)

        # Serialize empty HashMap to avoid downstream checks for object
        # existence for pickle.load calls.
        self.index = os.path.join(self.obj_dir, 'index')
        with open(self.index, 'wb+') as f:
            map = {}
            pickle.dump(map, f)

    def add(self, name, labware):
        """Adds a Labware object to the Registry.

        :param name: User-defined name to identify the labware.
        :type name: str
        :param labware: The Labware object being indexed.
        :type labware: Labware
        """
        # Create Labware
        # Save Labware

    def add_json(self, name, json_data):
        """Adds a Labware object to the Registry using JSON data.

        :param name: User-defined name to identify the labware.
        :type name: str
        :param json_data: Valid JSON data with correct number and type of
         fields. **Note**: thorough documentation of what constitutes *valid*
         can be found in the `Labware` class.
        :type json_data: JSON
        """

    def get(self, name):
        """Retrieves a Labware object from the Registry.

        :param name: The user-defined name associated with the desired Labware
         type.
        :type name: str
        :returns: The desired Labware type.
        :return type: Labware.
        """

    def list(self):
        """List the Labware types currently indexed.

        :returns: A list of user-defined names.
        :return type: list
        """

    def wipe(self):
        """Removes all data stored in this Registry.

        **This is a dangerous and irreversible operation.**
        """

        shutil.rmtree(self.obj_dir)
