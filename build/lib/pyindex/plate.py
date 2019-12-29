"""
plate.py
~~~~~~~~
Defines the Plate class.
"""


class Plate():

    """The representation of the Plate infrastructure for arbitrary Labware."""

    def __init__(self,
                 sterile,
                 skirted,
                 enzyme_free,
                 length,
                 width,
                 height,
                 well_spacing,
                 well_num,
                 well,
                 composition="unknown"):
        """Defines new Plate infrastructure.

        :param sterile: True if the plate is sterile.
        :type sterile: bool
        :param skirted: True if the plate is skirted (has a lip around the
         base).
        :type skirted: bool
        :param enzyme_free: True if the plate is tested to be free of
         DNase/RNase.
        :type enzyme_free: bool
        :param composition: Description of the composition material. The only
         optional parameter. Defaults to "unknown" if nothing is provided.
        :type composition: str
        :param length: Length of the plate *at the base* in **mm**.
        :type length: float
        :param width: Width of the plate *at the base* in **mm**.
        :type width: float
        :param height: Overall plate height in **mm**.
        :type height: float
        :param well_spacing: Distance between *the centers* of any two wells in
         **mm**.
        :type well_spacing: float
        :param well_num: Number of wells.
        :type well_num: int
        :param well: Type of well used in the plate.
        :type well: Well
        """

        self.sterile = sterile
        self.skirted = skirted
        self.enzyme_free = enzyme_free
        self.length = length
        self.width = width
        self.height = height
        self.well_spacing = well_spacing
        self.well_num = well_num
        self.well = well
        self.composition = "unknown" if not composition else composition

    def __repr__(self):
        """Succinct Plate representation."""
        return "Plate with length {} mm, width {} mm, height {} mm," \
            " and {} wells.".format(self.length, self.width,
                                    self.height,
                                    self.well_num)

    def __eq__(self, other):
        """Identical attributes between objects is sufficient for equality."""
        return self.__dict__ == other.__dict__
