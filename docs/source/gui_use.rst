.. _gui_use:

The graphical interface is a minimal visual tool that was implemented using the
`PySimpleGui` library, a wrapper itself around the more common `tkinter` and
`qt` python GUI libraries.

Navigate yourself to the ``/gui`` directory in the project directory. Make sure
the Download steps were followed thoroughly. Opening the GUI is as simple as::

  python3 gui.py

The main "control panel" should pop up.

Here's a brief rundown of the button functionality:

* `Info` - Select/Click on a Labware for a popup of summary characteristics.
* `Remove` - Select/Click on a Labware to permanently delete from the Registry.
* `Add` - Manually fill in characteristics for a new Labware type using a GUI popup. These  fields are *not* validated because the dynamic typing of python. Use with care.
* `Add From File` - Load a new Labware type from a valid .json file using a file browser. A directory ``sample_json/`` is provided within the ``gui/`` directory with some starter Labware types for this exact purpose. 
* `Wipe` - Permanently reset the entire Registry.

To load our sample Labware, we must click on the `Add From File` button, and
navigate to the ``sample_json/lp_0200.json`` (for example), name our Labware and click `Save`.

The rest of the commands should be fairly easy to navigate and follow from the API calls that they encapsulate. There is a `Help` button that summarizes such information if you need it.
