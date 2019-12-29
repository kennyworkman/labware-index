"""
error.py
~~~~~~~~
Defines custom exceptions for use in pyindex.
"""


class BadJSONError(Exception):
    """Is indicative of incorrectly structured or incomplete JSON data, for the
    purpose of insantiating data types."""
    pass


class ExistingRegistryError(Exception):
    """Will be thrown if the user is trying to instantiate a Registry object in
    a directory where one already exists."""
    pass
