.. _api_use:

Here a suggested workflow using the API with a python interpreter is presented.


First instantiate a fresh `Registry`. Note the format of the object representation.

>>> from pyindex.registry import Registry
>>> registry = Registry()
>>> registry
Labware Registry
________________

Now we need to add a `Labware` object to our `Registry`. We have three options
to do so: 

* directly passing a `Labware` object 
* providing raw JSON data
* loading JSON data from a file.

Working with JSON files is the cleanest and safest option, especially when using a template or using sample files included with the repository (located under ``tests/labware_json/`` or ``gui/sample_json/``).

>>> registry.add_file("RAD", "tests/labware_json/biorad_HSP9601B.json")

Now our tool has something in it. Notice the updated object repr.

>>> registry
Labware Registry
________________
* RAD --> Bio-Rad-HSP9601B with length 127.76 mm, width 85.48 mm, height 16.06 mm, and 96 wells.

"RAD" is an example of a user-defined name. You can name your `Labware` however you wish. The serialization of the actual object occurs independently of this field.

Lets add another piece of labware.

>>> registry.add_file("CORN", "tests/labware_json/corning_3960.json")
>>> registry
Labware Registry
________________
* RAD --> Bio-Rad-HSP9601B with length 127.76 mm, width 85.48 mm, height 16.06 mm, and 96 wells.
* CORN --> Corning 3960 with length 127.8 mm, width 85.9 mm, height 43.8 mm, and 96 wells.

Now that we have some labware filed away. How do we access it?

We can get a quick list of our named labware with:

>>> registry.list()
['RAD', 'CORN']

Using our names, we can then query an object and pick it apart for a desired attribute(s).

>>> rad = registry.get("Rad")
>>> rad
Bio-Rad-HSP9601B with length 127.76 mm, width 85.48 mm, height 16.06 mm, and 96 wells.
>>> rad.plate
Plate with length 127.76 mm, width 85.48 mm, height 16.06 mm, and 96 wells.
>>> rad.well
Well with volume 200 uL, depth 14.81 mm, top diameter 5.46 mm, and bottom diameter 2.64 mm.
>>> rad.plate.well_num
96

A detailed look at all of the `Labware` attributes is provided in the API section of the documentation.

Let's say I don't like "CORN" anymore. We can remove it simply as so:

>>> registry.remove("CORN")
>>> registry
Labware Registry
________________
* RAD --> Bio-Rad-HSP9601B with length 127.76 mm, width 85.48 mm, height 16.06 mm, and 96 wells.

To start completely fresh, we can wipe our repo.

>>> registry.wipe()
>>> registry
Labware Registry
________________
