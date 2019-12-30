import PySimpleGUI as sg
from pyindex.registry import Registry
import json

"""
    A GUI for the pyindex package.
"""

sg.change_look_and_feel("Dark Blue 3")
REGISTRY = None


def init_table():
    """Instantiate our Registry and load our Labware data."""
    global REGISTRY
    REGISTRY = Registry()

    # PySimpleGUI needs a placeholder in the event of an empty table (ie.
    # Registry with no data.)
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/1451
    if (not REGISTRY.list()):
        REGISTRY.add_file("Placeholder", "placeholder.json")
    return update_table()


def update_table():
    """Update our Labware data.

    :returns: Multi-dimensional array of Labware properties.
    :return type: 2d array
    """
    table = []
    for name in REGISTRY.list():
        labware = REGISTRY.get(name)
        table.append([name, labware.name,
                      labware.plate.length, labware.plate.width,
                      labware.plate.height, labware.plate.well_num,
                      labware.well.volume])
    return table


def add_labware():
    """Spawns an input window to log a new Labware type.

    The return values are two-fold:

    * User-defined name of the Labware to be logged.
    * JSON representation of labware.

    :return: User defined name, JSON representation of Labware. (None if the
     user exits.)
    :return type: str, JSON
    """

    # Align text elements with consistent sizing.
    t = (17, 1)
    layout = [[sg.Text("Add Labware*", font="Any 16")],
              [sg.Text("Custom Name", size=t,),
                  sg.Input(size=(15, 1), key="registry_name")],
              [sg.Text("Labware Name", size=t,),
                  sg.Input(size=(15, 1), key="labware_name")],
              [sg.Text("Sterile", size=t,),
                  sg.Combo(["true", "false"], key="sterile")],
              [sg.Text("Skirted", size=t,),
                  sg.Combo(["true", "false"], key="skirted")],
              [sg.Text("DNase/RNase free", size=t,),
                  sg.Combo(["true", "false"], key="enzyme_free")],
              [sg.Text("Plate Length", size=t,),
                  sg.Input(size=(5, 1), key="plate_length")],
              [sg.Text("Plate Width", size=t,),
                  sg.Input(size=(5, 1), key="plate_width")],
              [sg.Text("Plate Height", size=t,),
                  sg.Input(size=(5, 1), key="plate_height")],
              [sg.Text("Well Spacing", size=t,),
                  sg.Input(size=(5, 1), key="well_spacing")],
              [sg.Text("Well Number", size=t,),
                  sg.Input(size=(5, 1), key="well_num")],
              [sg.Text("Composition**", size=t,),
                  sg.Input(size=(15, 1), default_text="unknown",
                           key="composition")],
              [sg.Text("Well Volume", size=t,),
                  sg.Input(size=(5, 1), key="well_volume")],
              [sg.Text("Well Depth", size=t,),
                  sg.Input(size=(5, 1), key="well_depth")],
              [sg.Text("Well Top Diameter", size=t,),
                  sg.Input(size=(5, 1), key="top_diameter")],
              [sg.Text("Well Bottom Diameter", size=t,),
                  sg.Input(size=(5, 1), key="bottom_diameter")],
              [sg.Text('*All measurements are in mm and uL.')],
              [sg.Text('**Measurement optional.')],
              [sg.Button('Save'), sg.Button('Exit')]]
    window = sg.Window('Labware Registry', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            window.close()
            return None
        if event == 'Save':
            missing = False
            for key in values:
                # Kindly alert the user with the first missing required field.
                if not values[key] and key != "composition":
                    missing = True
                    sg.Popup("{} is a required field".format(key))
                    break
            if not missing:
                window.close()
                return values["registry_name"], dict_to_json(values)


def show_info(index, table):
    """Show information for a single piece of labware.

    :param index: Index of labware in GUI table.
    :type index: int
    """
    name = table[index][0]
    labware = REGISTRY.get(name)

    t = (17, 1)
    layout = [[sg.Text(name, font="Any 16")],
              [sg.Text("Labware Name", size=t,),
                  sg.Text(labware.name, justification="left")],
              [sg.Text("Sterile", size=t,),
                  sg.Text(labware.plate.sterile, justification="left")],
              [sg.Text("Skirted", size=t,),
                  sg.Text(labware.plate.skirted, justification="left")],
              [sg.Text("DNase/RNase free", size=t,),
                  sg.Text(labware.plate.enzyme_free, justification="left")],
              [sg.Text("Plate Length", size=t,),
                  sg.Text(labware.plate.length, justification="left")],
              [sg.Text("Plate Width", size=t,),
                  sg.Text(labware.plate.width, justification="left")],
              [sg.Text("Plate Height", size=t,),
                  sg.Text(labware.plate.height, justification="left")],
              [sg.Text("Well Spacing", size=t,),
                  sg.Text(labware.plate.well_spacing, justification="left")],
              [sg.Text("Well Number", size=t,),
                  sg.Text(labware.plate.well_num, justification="left")],
              [sg.Text("Composition", size=t,),
                  sg.Text(labware.plate.composition, justification="left")],
              [sg.Text("Well Volume", size=t,),
                  sg.Text(labware.well.volume, justification="left")],
              [sg.Text("Well Depth", size=t,),
                  sg.Text(labware.well.depth, justification="left")],
              [sg.Text("Well Top Diameter", size=t,),
                  sg.Text(labware.well.top_diameter, justification="left")],
              [sg.Text("Well Bottom Diameter", size=t,),
                  sg.Text(labware.well.bottom_diameter, justification="left")],
              [sg.Cancel()]]

    window = sg.Window('Labware Registry', layout)
    event, values = window.read()
    window.close()


def show_help():
    """Show a pop-up help page."""
    t = (17, 1)
    layout = [[sg.Text("Command Overview", font="Any 16")],
              [sg.Text("Info", size=t,),
                  sg.Text("Select desired Labware for a summary of"
                          " characteristics.", justification="left")],
              [sg.Text("Remove", size=t,),
                  sg.Text("Select desired Labware to permenantly delete from"
                          " the Registry.", justification="left")],
              [sg.Text("Add", size=t,),
                  sg.Text("Fill in characteristics for a new Labware using the"
                          " GUI.", justification="left")],
              [sg.Text("Add From File", size=t,),
                  sg.Text("Load a new Labware using a valid .json file.",
                          justification="left")],
              [sg.Text("Wipe", size=t,),
                  sg.Text("Permanently delete the contents of the Registry.",
                          justification="left")],
              [sg.Cancel()]]

    window = sg.Window('Labware Registry', layout)
    event, values = window.read()
    window.close()


def add_from_file():
    """Adds Labware from user selected JSON file.

    :returns: Path to user's file.
    :return type: str
    """
    layout = [[sg.Text("Enter a custom name and select a file.")],
              [sg.Text("Custom Name", size=(12, 1)), sg.Input()],
              [sg.Text("Labware JSON", size=(12, 1)), sg.Input(),
               sg.FileBrowse()],
              [sg.Button("Save"), sg.Button("Cancel")]]
    window = sg.Window("Labware Registry", layout)

    event, values = window.read()
    if (event in (None, "Cancel")):
        window.close()
        return None

    window.close()
    return values[0], values[1]


def dict_to_json(dict):
    """Converts a dictionary of values from GUI to valid Labware JSON.

    :param dict: Dictionary of user-inputted gui values.
    :type dict: dict
    :returns: Valid JSON to construct Labware object.
    :return type: JSON
    """
    json_data = {}
    plate_dict = {}
    well_dict = {}

    plate_dict["sterile"] = dict["sterile"]
    plate_dict["skirted"] = dict["skirted"]
    plate_dict["enzyme_free"] = dict["enzyme_free"]
    plate_dict["length"] = dict["plate_length"]
    plate_dict["width"] = dict["plate_width"]
    plate_dict["height"] = dict["plate_height"]
    plate_dict["well_spacing"] = dict["well_spacing"]
    plate_dict["well_num"] = dict["well_num"]
    plate_dict["composition"] = dict.get("composition")

    well_dict["volume"] = dict["well_volume"]
    well_dict["depth"] = dict["well_depth"]
    well_dict["top_diameter"] = dict["top_diameter"]
    well_dict["bottom_diameter"] = dict["bottom_diameter"]

    json_data["name"] = dict["labware_name"]
    json_data["plate"] = plate_dict
    json_data["well"] = well_dict

    return json.dumps(json_data)


def confirm_window():
    """Presents the user with a confirmation popup.

    :returns: Boolean indicative of user's choice.
    :return type: boolean
    """

    layout = [[sg.Text("Are you sure? This action is permanent.")],
              [sg.Button("Yes"), sg.Button("Cancel")]]
    window = sg.Window("Confirmation", layout)

    while True:
        event, values = window.read()
        window.close()
        if event == "Yes":
            return True
        if event in (None, "Cancel"):
            return False


if __name__ == "__main__":
    data = init_table()
    headings = ["Name", "Labware", "Length", "Width",
                "Height", "Well Number", "Well Volume"]
    layout = [[sg.Table(values=data, headings=headings,
                        max_col_width=25,
                        auto_size_columns=True,
                        justification='center',
                        num_rows=15,
                        key="TABLE")],
              [sg.Button("Info"), sg.Button("Remove"), sg.Button("Add"),
               sg.Button("Add From File"), sg.Button("Wipe"),
               sg.Button("Help")]]
    window = sg.Window("Labware Registry",
                       layout,
                       alpha_channel=0.95,
                       grab_anywhere=True)

    while True:
        event, values = window.read()
        if (event == "Info"):
            if values["TABLE"]:
                table = window["TABLE"].get()
                for num in values["TABLE"]:
                    show_info(num, table)

        if (event == "Remove"):
            # Provides courtesy pop-up before permanent damage made.
            if values["TABLE"] and confirm_window():
                table = window["TABLE"].get()

                if (len(table) == 1):
                    sg.Popup("Cannot have an empty table.")
                    continue

                for num in values["TABLE"]:
                    REGISTRY.remove(table[num][0])
                window["TABLE"].update(values=update_table())

        if (event == "Add"):
            user_out = add_labware()
            if user_out:
                name, json_data = user_out
            else:
                continue
            REGISTRY.add_json(name, json_data)
            # Reflect updated registry in main table.
            window["TABLE"].update(values=update_table())

        if (event == "Add From File"):
            user_out = add_from_file()
            if user_out:
                name, file = user_out
            else:
                continue
            REGISTRY.add_file(name, file)
            window["TABLE"].update(values=update_table())

        if (event == "Wipe"):
            if confirm_window():
                REGISTRY.wipe()
                init_table()
                window["TABLE"].update(values=update_table())

        if (event == "Help"):
            show_help()

            # Will terminate the script in the event of a manual exit.
        if (event is None):
            break

    window.close()
