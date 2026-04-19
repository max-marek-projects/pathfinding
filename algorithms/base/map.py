"""Map handling."""

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..exceptions import CalculationFailedError, DataNotProvidedError, WrongArgumentValuesError
from ..math_handlers import Matrix, Point, Vector

DIRECTIONS = [Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)]


@dataclass
class MapPoint:
    """Handler for a point on the map.

    Attributes:
            passable: Whether the point is passable.
            distance: Distance from the start point.
    """

    passable: bool
    distance: int | None = None

    def clear(self) -> None:
        """Clear the table cell."""
        self.distance = None


class Map(ABC):
    """Map containing passable and impassable points."""

    data: Matrix[MapPoint]
    _n: int
    _m: int
    _start_point: Point | None = None
    _end_point: Point | None = None
    _height: int
    _width: int
    path: list[Point]

    @property
    def start_point(self) -> Point | None:
        """Get the value of the start point.

        Returns:
            Point handler describing the start point.
        """
        return self._start_point

    @start_point.setter
    def start_point(self, point: Point | None) -> None:
        """Set the value of the start point.

        Args:
            point: Value of the start point.

        Raises:
            DataNotProvidedError: if map was not yet generated.
            WrongArgumentValuesError: if impassable point selected.
        """
        if point:
            if not hasattr(self, "data"):
                raise DataNotProvidedError("Map has not been generated yet")
            if not self.data[point].passable:
                raise WrongArgumentValuesError("Selected an impassable point")
        self._start_point = point

    @property
    def end_point(self) -> Point | None:
        """Get the value of the end point.

        Returns:
            Value of the end point.
        """
        return self._end_point

    @end_point.setter
    def end_point(self, point: Point | None) -> None:
        """Set the value of the end point.

        Args:
            point: Value of the end point.

        Raises:
            DataNotProvidedError: if map was not yet generated.
            WrongArgumentValuesError: if impassable point selected.
        """
        if point:
            if not hasattr(self, "data"):
                raise DataNotProvidedError("Map has not been generated yet")
            if not self.data[point].passable:
                raise WrongArgumentValuesError("Selected an impassable point")
        self._end_point = point

    @property
    def height(self) -> int:
        """Get the height value.

        Returns:
            Integer corresponding to the number of maze rows.
        """
        return self._height

    @height.setter
    def height(self, value: object) -> None:
        """Set the maze height value.

        Args:
            value: Maze height value.

        Raises:
            WrongArgumentValuesError: if received some type that can not be converted to integer or is lower than 1.
        """
        try:
            int_value = int(value)  # type: ignore[call-overload, ty:invalid-argument-type]
        except ValueError as ex:
            raise WrongArgumentValuesError(f'Invalid input value: "{value}". Must be an integer') from ex
        if int_value < 1:
            raise WrongArgumentValuesError("Value must be greater than 0")
        self._height = int_value

    @property
    def width(self) -> int:
        """Get the width value.

        Returns:
            Integer corresponding to the number of maze columns.
        """
        return self._width

    @width.setter
    def width(self, value: object) -> None:
        """Set the maze width value.

        Args:
            value: Maze width value.

        Raises:
            WrongArgumentValuesError: if received some type that can not be converted to integer or is lower than 1.
        """
        try:
            int_value = int(value)  # type: ignore[call-overload, ty:invalid-argument-type]
        except ValueError as ex:
            raise WrongArgumentValuesError(f'Invalid input value: "{value}". Must be an integer') from ex
        if int_value < 1:
            raise WrongArgumentValuesError("Value must be greater than 0")
        self._width = int_value

    def generate_map(self) -> None:
        """Generate the map."""
        self._n = 2 * self.height + 1
        self._m = 2 * self.width + 1
        self.data = Matrix([[MapPoint(passable=False) for _ in range(self._m)] for _ in range(self._n)])

        stack = [Point(0, 0)]
        while len(stack) > 0:
            point = stack[-1]
            random.shuffle(DIRECTIONS)

            for direction in DIRECTIONS:
                next_point = point + direction
                if (
                    next_point.x >= 0
                    and next_point.y >= 0
                    and next_point.x < self.width
                    and next_point.y < self.height
                    and not self.data[self.to_raw(next_point)].passable
                ):
                    self.data[self.to_raw(next_point)].passable = True
                    self.data[self.to_raw(point) + direction].passable = True
                    stack.append(next_point)
                    break
            else:
                stack.pop()

    def __repr__(self) -> str:
        """Get a string representation of the map.

        Returns:
            String representation as black and white squares.
        """
        return "\n".join(["\t".join([str(cell) for cell in row]) for row in self.data])

    @staticmethod
    def to_raw(point: Point) -> Point:
        """Convert point coordinates to raw coordinates inside the maze.

        Returns:
            Point with converted coordinates.
        """
        return point * 2 + Vector(1, 1)

    def find_path(self) -> list[Point]:
        """Find a path in the maze.

        Returns:
            List of points.

        Raises:
            DataNotProvidedError: if start or end points are not provided.
            CalculationFailedError: if failed to find a path.
        """
        self.clear()
        if not hasattr(self, "data"):
            raise DataNotProvidedError("Field not provided")
        if not self.start_point:
            raise DataNotProvidedError("Start point not provided")
        if not self.end_point:
            raise DataNotProvidedError("End point not provided")
        points = [self.start_point]
        self.data[self.start_point].distance = 0
        path_found = self._find_path(points)
        if not path_found:
            raise CalculationFailedError("Failed to find a path")
        path = [self.end_point]
        point = self.end_point
        while not point == self.start_point:
            for direction in DIRECTIONS:
                new_point = point + direction
                if (point_distance := self.data[point].distance) is None:
                    raise CalculationFailedError(f"Received point with not calculated distance: {point}")
                if self.data[new_point].distance == point_distance - 1:
                    path.append(new_point)
                    point = new_point
                    break
        return path

    @abstractmethod
    def _find_path(self, points: list[Point]) -> bool:
        """Find a path in the maze by iterating points.

        Returns:
            True / False whether path was found..
        """
        ...

    def clear(self) -> None:
        """Clear data for all points."""
        if hasattr(self, "data"):
            for row in self.data:
                for cell in row:
                    cell.clear()
