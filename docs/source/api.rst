.. _api:

The `pyindex` package makes up the bulk of the Labware Registry's back-end
infrastructure.

This part of the documentation covers an in-depth breakdown of the application
interface, highlighting certain design choices in class architecture.

The Registry
-------------

This is the primary user-facing interface for pyindex. It handles the indexing,
storing, and retrieval of Labware. The bulk of tool's functionality can be
extrapolated from the handful of methods within this class.

In the abstract, there should really only be a single `Registry` in existence
at any given time. The `Registry` constructor thus will "load" a `Registry`
from file when a user attempts to instantiate one in the presence of a
directory with persisted data. In such a scenario, a new `Registry` will be
created to reflect the state of this serialized data, and `Existing registry
loaded from disk` will be printed to std out to give off the illusion of a
Singleton pattern.

The design choice for persistence was largely inspired by git. Labware objects
are serialized, using the `pickle` package that comes in the Python standard
library, into files uniquely hashed by object content. The crytographic hashing
function used is Secure Hash 1, or **SHA-1**, and produces a 160-bit integer
hash from a `Labware` object byte stream. Hashing collisions under this
algorithm are impossible in practice, making for efficient and constant time
access to our data. (This is similar to the storage of commit and blob objects
in the `.git` folder for git version control.)

Users are able to index their `Labware` types by "nicknames", or whatever
custom naming scheme they desire. A serialized mapping of these nicknames to
object hash IDs is maintained to facilitate constant time object access. The
choice to serialize objects by SHA-1 hashcodes allows persisted objects to be
strictly decoupled from potentially frivolous and arbitrary user naming
schemes, avoiding the mapping of identical objects to different hashes and
vice-versa, while still allowing users to customize their Labware Index.

More information about persistence design choices are in the `Registry` section
of the API.

.. automodule:: pyindex.registry
    :members:
    :special-members:

    .. automethod:: __ 

Layers Upon Layers
------------------

When designing the class types to represent a piece of labware, a concerted
effort was made to encapsulate pieces of its functionality into modular and
relevant layers of abstraction. The `Labware` type was broken down into further
subtypes when its components, the `Plate` and the `Well`, could have utility
that is distinct and encapsulated from the `Labware` type as whole. The `Well`,
for instance, is the site of a reaction determined solely by its particular
attributes, ie. volume, depth, and any reagents that it contains, where as its
encompassing "Labware" is more or less a vessel.

This layered structure makes for a rather intuitive interface for attribute
access. If one wishes to know how many wells their labware has, they would make
the following call:

::

  labware.plate.num_wells

Likewise, the volume of their well is:

::

  labware.well.volume

A detailed breakdown of the nested class types continues below.


The Labware Object
------------------

.. automodule:: pyindex.labware
    :members:
    :special-members:

The Plate Object
----------------

.. automodule:: pyindex.plate
    :members:
    :special-members:

The Well Object
---------------

.. automodule:: pyindex.well
    :members:
    :special-members:

Some Errors
-----------

Two internal Errors were subclassed to provide verbose and specific handling of
extraneous circumstances

.. autoclass:: pyindex.error.BadJSONError
.. autoclass:: pyindex.error.ExistingRegistryError
