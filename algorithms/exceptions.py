"""Errors when working with the interface and handler classes."""


class WrongArgumentValuesError(Exception):
    """Invalid input data value."""

    pass


class DataNotProvidedError(Exception):
    """Start point not provided."""

    pass


class WrongActionError(Exception):
    """An invalid operation is being performed."""

    pass


class CalculationFailedError(Exception):
    """Failed to calculate."""

    pass
