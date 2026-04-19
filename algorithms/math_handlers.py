"""Handling mathematical components."""

from collections.abc import Iterator
from dataclasses import dataclass

from .exceptions import WrongArgumentValuesError


@dataclass
class Vector:
    """Class for handling a vector.

    Attributes:
        x: vector position on the x-axis.
        y: vector position on the y-axis.
    """

    x: int
    y: int


@dataclass
class Point:
    """Class for handling a point.

    Attributes:
        x: vector position on the x-axis.
        y: vector position on the y-axis.
    """

    x: int
    y: int

    def __add__(self, vector: Vector) -> Point:
        """Add a vector to the point.

        Args:
            vector: The vector to add.

        Returns:
            A point with coordinates increased according to the vector.

        Raises:
            WrongArgumentValuesError: if some other type than Vector received.
        """
        if not isinstance(vector, Vector):
            raise WrongArgumentValuesError("Only a vector can be added to a point")

        return Point(self.x + vector.x, self.y + vector.y)

    def __mul__(self, number: int) -> Point:
        """Multiply the point by a number.

        Args:
            number: The number to multiply the point coordinates by.

        Returns:
            A point whose coordinates are multiplied by the given number.

        Raises:
            WrongArgumentValuesError: if some other type than integer received.
        """
        if not isinstance(number, int):
            raise WrongArgumentValuesError("A point can only be multiplied by a number")

        return Point(self.x * number, self.y * number)

    def __iter__(self) -> Iterator[int]:
        """Iterate over the point coordinates.

        Yields:
            The x and y coordinates sequentially.
        """
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        """Get a string representation of the point.

        Returns:
            A string with the point coordinates.
        """
        return f"Point ({self.x}, {self.y})"


class Matrix[CellVar]:
    """Handler for a matrix with variable content type."""

    def __init__(self, data: list[list[CellVar]]) -> None:
        """Initialize the matrix handler.

        Args:
            data: The content to be used.
        """
        self.data = data

    def __getitem__(self, point: Point) -> CellVar:
        """Get an element from the matrix by point.

        Args:
            point: The point whose coordinates match the desired value.

        Returns:
            The value at the given coordinates.
        """
        return self.data[point.y][point.x]

    def __setitem__(self, point: Point, value: CellVar) -> None:
        """Set a matrix element at the given point.

        Args:
            point: The point whose coordinates match the target cell.
            value: The value to place in the cell.
        """
        self.data[point.y][point.x] = value

    def __iter__(self) -> Iterator[list[CellVar]]:
        """Get an iterator over the matrix.

        Returns:
            An iterator over the stored list.
        """
        return self.data.__iter__()
