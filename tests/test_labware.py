from pyindex.labware import Labware
from pyindex.registry import Registry
from pyindex.error import BadJSONError
import sys


def test_instantiation():
    """Ensure instantiation behavior works as expected."""
    with open("labware_json/lp_0200.json", "r") as f:
        json_data = f.read().replace('\n', '')
    lp = Labware(json_data)

    assert(lp.name == "LP-0200")
    assert(not lp.plate.sterile)
    assert(lp.plate.skirted)
    assert(lp.plate.enzyme_free)
    assert(lp.plate.length == 127.76)
    assert(lp.plate.width == 85.48)
    assert(lp.plate.height == 10.48)
    assert(lp.plate.well_spacing == 4.5)
    assert(lp.plate.well_num == 384)
    assert(lp.plate.composition == "Cyclic Olefin Copolymer")
    assert(lp.well.volume == 14)
    assert(lp.well.depth == 5.10)
    assert(lp.well.top_diameter == 2.432)
    assert(lp.well.bottom_diameter == 1.53)

    with open("labware_json/bad_data.json", "r") as f:
        json_data = f.read().replace('\n', '')

    # Initializing Labware object w/ bad data should throw custom error.
    try:
        Labware(json_data)
        sys.exit(1)
    except BadJSONError as e:
        pass


def test_save():
    """Test for uncorrupted serialization in the correct location."""

    registry = Registry()
    registry.wipe()


def test_hash():
    """Ensure unique hash id generation."""

    with open("labware_json/lp_0200.json", "r") as f:
        lp_data = f.read().replace('\n', '')
    lp_hash = Labware(lp_data).hash()

    with open("labware_json/corning_3960.json", "r") as f:
        corn_data = f.read().replace('\n', '')
    corn_hash = Labware(corn_data).hash()

    with open("labware_json/biorad_HSP9601B.json", "r") as f:
        bio_data = f.read().replace('\n', '')
    bio_hash = Labware(bio_data).hash()

    with open("labware_json/thermofisherscientific_140156.json", "r") as f:
        therm_data = f.read().replace('\n', '')
    therm_hash = Labware(therm_data).hash()

    assert(lp_hash != corn_hash != bio_hash != therm_hash)

    # Different object with the same fields should have the same hash value.
    lp_hash_dup = Labware(lp_data).hash()
    assert(lp_hash == lp_hash_dup)


def test_repr():
    """Ensure proper representation of Labware object."""

    with open("labware_json/lp_0200.json", "r") as f:
        lp_data = f.read().replace('\n', '')
    lp = Labware(lp_data)

    assert(lp.__repr__() == "LP-0200 with length 127.76 mm, width 85.48 mm,"
           " height 10.48 mm, and 384 wells.")


def test_equality():
    """Ensures equality based on SHA-1 criteria only."""

    with open("labware_json/lp_0200.json", "r") as f:
        lp_data = f.read().replace('\n', '')
    lp = Labware(lp_data)
    lp_dup = Labware(lp_data)

    with open("labware_json/corning_3960.json", "r") as f:
        corn_data = f.read().replace('\n', '')
    corn = Labware(corn_data)

    assert(lp != corn)
    assert(lp == lp_dup)
