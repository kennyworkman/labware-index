"""
labware.py
~~~~~~~~~~
Defines the Labware class.
"""

import json
import pickle
import hashlib
import os
from .error import BadJSONError
from .plate import Plate
from .well import Well


class Labware():

    """A class representing a generic SBS-footprint labware type."""

    def __init__(self, json_data):
        """Creates a new labware type from valid JSON data.

        *Valid json data* is defined as any such JSON-formatted data type that
        possess the necessary fields to thoroughly define a Labware object. A
        template structure is provided below; be sure to include all fields
        given in the template to avoid an instantiation error:

        .. code-block:: json

            {
                "name": str,
                "plate": {
                    "sterile": boolean,
                    "skirted": boolean,
                    "enzyme_free": boolean,
                    "length": float,
                    "width": float,
                    "height": float,
                    "well_spacing": float,
                    "well_num": int,
                    "composition": boolean (optional),
                },
                "well": {
                    "volume": float,
                    "depth": float,
                    "top_diameter": float,
                    "bottom_diameter": float,
                }
            }

        A more complete specifications describing these fields can be found in
        the parameter descriptions of the `Plate` and `Well` object
        documentation.

        :param json_data: Valid JSON data as described above.
        :type json_data: JSON
        """
        decoded = json.loads(json_data)

        try:
            self.name = decoded["name"]

            self.well = Well(decoded["well"]["volume"],
                             decoded["well"]["depth"],
                             decoded["well"]["top_diameter"],
                             decoded["well"]["bottom_diameter"])

            self.plate = Plate(decoded["plate"]["sterile"],
                               decoded["plate"]["skirted"],
                               decoded["plate"]["enzyme_free"],
                               decoded["plate"]["length"],
                               decoded["plate"]["width"],
                               decoded["plate"]["height"],
                               decoded["plate"]["well_spacing"],
                               decoded["plate"]["well_num"],
                               self.well,
                               decoded["plate"].get("composition"))
        except KeyError as e:
            raise BadJSONError("Provided JSON data is missing necessary fields"
                               " to instantiate a Labware object.")

        self.id = self.hash()

    def save(self, registry, name=None):
        """Stores a serialized version of self in the Registry.

        The process of "saving" is twofold:

        * A serialized object is stored in the object directory with a filename
         corresponding to its SHA-1 hash code.
        * The index file is updated with a mapping of this object's informal
         name to its hashcode.

        :param registry: Target Registry to save this piece of Labware to.
        :type registry: Registry
        :param name: Optional user-defined name for this piece of Labware in
         the context of a Registry. This name can be used to access the
         Labware, and defaults to the name of the object.k
        :type name: str
        """

        # Hash ID should reflect any changes in object fields.
        self.id = self.hash()

        obj_file = os.path.join(registry.obj_dir, self.id)
        with open(obj_file, "wb+") as f:
            pickle.dump(self, f)

        # Need to read and write to the hash map with different context
        # managers to avoid corrupting the file.
        map = None
        name = self.name if not name else name
        with open(registry.index, "rb") as f:
            map = pickle.load(f)
            map[name] = self.id
        with open(registry.index, "wb+") as f:
            pickle.dump(map, f)

    def hash(self):
        """Generates an SHA-1 hashcode for this object.

        Unique generation will avoid potential hashing collissions that emerge
        from indexing based on user-defined naming schemes.

        :returns: SHA-1 hashcode.
        :return type: str
        """
        byte_obj = pickle.dumps(self)
        return hashlib.sha1(byte_obj).hexdigest()

    def __repr__(self):
        """Succinct Labware representation."""
        return "{} with length {} mm, width {} mm, height {} mm," \
            " and {} wells.".format(self.name, self.plate.length,
                                    self.plate.width,
                                    self.plate.height,
                                    self.plate.well_num)

    def __eq__(self, other):
        """Unique property of SHA-1 will guarantee equality of attributes."""
        return self.id == other.id
