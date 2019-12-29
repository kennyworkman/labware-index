from pyindex.well import Well
from pyindex.plate import Plate


def test_instantiation():
    """Ensure instantiation behavior works as expected."""

    # First without a defined composition attribute.
    small = Well(14, 5.1, 2.432, 1.53)
    plate = Plate(True, True, True, 127.76, 85.48, 10.48, 4.5, 384, small)

    assert(plate.sterile and plate.skirted and plate.enzyme_free)
    assert(plate.length == 127.76)
    assert(plate.width == 85.48)
    assert(plate.height == 10.48)
    assert(plate.well_spacing == 4.5)
    assert(plate.well_num == 384)

    # Easy to see if we don't know the composition of our plate.
    assert(plate.composition == "unknown")

    assert(plate.well.depth == 5.1)
    assert(plate.well.top_diameter == 2.432)
    assert(plate.well.bottom_diameter == 1.53)

    plate = Plate(True, True, True, 127.76, 85.48, 10.48, 4.5, 384, small,
                  "coc")
    assert(plate.composition == "coc")


def test_repr():
    """Ensure proper representation of Plate object."""

    small = Well(14, 5.1, 2.432, 1.53)
    plate = Plate(True, True, True, 127.76, 85.48, 10.48, 4.5, 384, small)

    assert(plate.__repr__() == "Plate with length 127.76 mm, width 85.48 mm,"
           " height 10.48 mm, and 384 wells.")


def test_equality():
    """Objects with identical fields should be equal."""

    # Standard equality check.
    small = Well(14, 5.1, 2.432, 1.53)
    plate = Plate(True, True, True, 127.76, 85.48, 10.48, 4.5, 384, small)
    not_equal = Plate(False, True, True, 127.76, 85.48, 10.48, 4.5, 384, small)
    assert(plate != not_equal)

    equal = Plate(True, True, True, 127.76, 85.48, 10.48, 4.5, 384, small)
    assert(plate == equal)

    # Equality check with different well object.
    small = Well(13, 5.1, 2.432, 1.53)
    not_equal = Plate(True, True, True, 127.76, 85.48, 10.48, 4.5, 384, small)
    assert(small != not_equal)
