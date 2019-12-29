"""
well.py
~~~~~~~~
Defines the Well class.
"""


class Well():

    """The representation of a single well within some plate."""

    def __init__(self,
                 volume,
                 depth,
                 top_diameter,
                 bottom_diameter):
        """Defines a new well.

        :param volume: The *maximum* working volume for a single well in **uL**
        :type volume: float
        :param depth: The depth of a well in **mm**.
        :type depth: float.
        :param top_diameter: The diameter at the opening in **mm**.
        :type top_diameter: float.
        :param bottom_diameter: The diameter at the bottom of the conical
         section in **mm**.
        :type bottom_diameter: float.
        """

        self.volume = volume
        self.depth = depth
        self.top_diameter = top_diameter
        self.bottom_diameter = bottom_diameter

    def __repr__(self):
        """Succinct Well representation."""
        return "Well with volume {} uL, depth {} mm, top diameter {} mm," \
            " and bottom diameter {} mm.".format(self.volume, self.depth,
                                                 self.top_diameter,
                                                 self.bottom_diameter)

    def __eq__(self, other):
        """Identical attributes between objects is sufficient for equality."""
        return self.__dict__ == other.__dict__
