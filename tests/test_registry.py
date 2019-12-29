from pyindex.labware import Labware
from pyindex.registry import Registry
from pyindex.error import ExistingRegistryError
import sys
import pickle
import os


def test_instantiation():
    """Ensure instantiation behavior works as expected."""
    registry = Registry()
    assert(os.path.exists(registry.obj_dir))
    assert(os.path.exists(registry.index))

    # Shouldn't be able to instantiate a second Registry.
    try:
        Registry()
        sys.exit(1)
    except ExistingRegistryError as e:
        pass

    registry.wipe()


def test_repr():
    """Ensure proper representation of Labware object."""

    registry = Registry()
    assert(registry.__repr__() == "\nLabware Registry\n________________\n")

    with open("labware_json/lp_0200.json", "r") as f:
        json_data = f.read().replace('\n', '')
    lp = Labware(json_data)
    registry.add(lp, lp.name)

    with open("labware_json/corning_3960.json", "r") as f:
        json_data = f.read().replace('\n', '')
    corn = Labware(json_data)
    registry.add(corn, corn.name)

    assert(registry.__repr__() ==
           "\nLabware Registry\n________________\nLP-0200\nCorning 3960\n")

    registry.wipe()


def test_add():
    """Test adding Labware objects to Registry."""
    registry = Registry()

    with open("labware_json/lp_0200.json", "r") as f:
        json_data = f.read().replace('\n', '')
    lp = Labware(json_data)
    registry.add(lp)
    # Should have a new serialized object in our directory.
    lp_file = os.path.join(registry.obj_dir, lp.id)
    assert(os.path.exists(lp_file))
    with open(lp_file, "rb") as f:
        assert(pickle.load(f) == lp)
    # Index should be updated with mapping to correct hashID.
    assert(os.path.exists(registry.index))
    with open(registry.index, "rb") as f:
        map = pickle.load(f)
        assert(map[lp.name] == lp.id)
        assert(len(map) == 1)

    with open("labware_json/corning_3960.json", "r") as f:
        json_data = f.read().replace('\n', '')
    corn = Labware(json_data)
    registry.add(corn, "CORN")
    # Should have a new serialized object in our directory.
    corn_file = os.path.join(registry.obj_dir, corn.id)
    assert(os.path.exists(corn_file))
    with open(corn_file, "rb") as f:
        assert(pickle.load(f) == corn)
    # Index should be updated with mapping to correct hashID.
    assert(os.path.exists(registry.index))
    with open(registry.index, "rb") as f:
        map = pickle.load(f)
        assert(map[lp.name] == lp.id)
        assert(map["CORN"] == corn.id)
        assert(len(map) == 2)

    registry.wipe()


def test_json_add():
    """Test adding Labware json to Registry."""
    registry = Registry()

    with open("labware_json/lp_0200.json", "r") as f:
        json_data = f.read().replace('\n', '')
    registry.add_json("LP", json_data)
    lp = registry.get("LP")
    lp_id = lp.id
    # Should have a new serialized object in our directory.
    lp_file = os.path.join(registry.obj_dir, lp_id)
    assert(os.path.exists(lp_file))
    with open(lp_file, "rb") as f:
        assert(pickle.load(f) == lp)
    # Index should be updated with mapping to correct hashID.
    assert(os.path.exists(registry.index))
    with open(registry.index, "rb") as f:
        map = pickle.load(f)
        assert(map["LP"] == lp_id)
        assert(len(map) == 1)

    with open("labware_json/biorad_HSP9601B.json", "r") as f:
        json_data = f.read().replace('\n', '')
    registry.add_json("RAD", json_data)
    rad = registry.get("RAD")
    rad_id = rad.id
    # Should have a new serialized object in our directory.
    rad_file = os.path.join(registry.obj_dir, rad_id)
    assert(os.path.exists(rad_file))
    with open(rad_file, "rb") as f:
        assert(pickle.load(f) == rad)
    # Index should be updated with mapping to correct hashID.
    assert(os.path.exists(registry.index))
    with open(registry.index, "rb") as f:
        map = pickle.load(f)
        assert(map["LP"] == lp_id)
        assert(map["RAD"] == rad_id)
        assert(len(map) == 2)

    registry.wipe()


def test_add_file():
    """Test adding Labware json file to Registry."""
    registry = Registry()

    registry.add_file("LP", "labware_json/lp_0200.json")
    lp = registry.get("LP")
    lp_id = lp.id
    # Should have a new serialized object in our directory.
    lp_file = os.path.join(registry.obj_dir, lp_id)
    assert(os.path.exists(lp_file))
    with open(lp_file, "rb") as f:
        assert(pickle.load(f) == lp)
    # Index should be updated with mapping to correct hashID.
    assert(os.path.exists(registry.index))
    with open(registry.index, "rb") as f:
        map = pickle.load(f)
        assert(map["LP"] == lp_id)
        assert(len(map) == 1)

    registry.wipe()


def test_remove():
    """Test the 'remove' operation."""

    registry = Registry()
    with open("labware_json/lp_0200.json", "r") as f:
        json_data = f.read().replace('\n', '')
    lp = Labware(json_data)

    registry.add(lp, "LP")
    lp_file = os.path.join(registry.obj_dir, lp.id)
    assert(os.path.exists(lp_file))
    with open(registry.index, "rb") as f:
        map = pickle.load(f)
        assert(len(map) == 1)

    registry.remove("LP")
    assert(not os.path.exists(lp_file))
    with open(registry.index, "rb") as f:
        map = pickle.load(f)
        assert(len(map) == 0)

    registry.wipe()


def test_get():
    registry = Registry()

    with open("labware_json/lp_0200.json", "r") as f:
        json_data = f.read().replace('\n', '')
    lp = Labware(json_data)
    registry.add(lp)
    retrieved = registry.get(lp.name)
    assert(lp == retrieved)

    registry.wipe()


def test_list():
    registry = Registry()

    with open("labware_json/lp_0200.json", "r") as f:
        json_data = f.read().replace('\n', '')
    lp = Labware(json_data)
    registry.add(lp)

    with open("labware_json/corning_3960.json", "r") as f:
        json_data = f.read().replace('\n', '')
    corn = Labware(json_data)
    registry.add(corn)

    with open("labware_json/biorad_HSP9601B.json", "r") as f:
        json_data = f.read().replace('\n', '')
    rad = Labware(json_data)
    registry.add(rad)

    lab_list = registry.list()
    assert(len(lab_list) == 3)
    assert(lab_list[0] == 'LP-0200')
    assert(lab_list[1] == 'Corning 3960')
    assert(lab_list[2] == 'Bio-Rad-HSP9601B')

    registry.wipe()
