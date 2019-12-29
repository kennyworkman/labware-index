from pyindex.well import Well


def test_instantiation():
    """Ensure instantiation behavior works as expected."""

    small = Well(14, 5.1, 2.432, 1.53)

    assert(small.volume == 14)
    assert(small.depth == 5.1)
    assert(small.top_diameter == 2.432)
    assert(small.bottom_diameter == 1.53)


def test_repr():
    """Ensure proper representation of Well object."""

    small = Well(14, 5.1, 2.432, 1.53)

    assert(small.__repr__() == "Well with volume 14 uL, depth 5.1 mm, top"
           " diameter 2.432 mm, and bottom diameter 1.53 mm.")


def test_equality():
    """Objects with identical fields should be equal."""

    small = Well(14, 5.1, 2.432, 1.53)
    not_equal = Well(13, 5.1, 2.432, 1.53)
    assert(small != not_equal)

    equal = Well(14, 5.1, 2.432, 1.53)
    assert(small == equal)
