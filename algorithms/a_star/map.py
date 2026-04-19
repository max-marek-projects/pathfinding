"""Processing the map with the A* algorithm."""

from ..base import DIRECTIONS, Map
from ..exceptions import CalculationFailedError, DataNotProvidedError
from ..math_handlers import Point


class AStarMap(Map):
    """Wave method map containing passable and impassable points."""

    def _find_path(self, points: list[Point]) -> bool:
        """Find a path in the maze by iterating points.

        Returns:
            True / False whether path was found.

        Raises:
            CalculationFailedError: if received any point with not calculated distance.
        """
        path_found = False
        while points and not path_found:
            point = points[0]
            if point == self.end_point:
                path_found = True
            for direction in DIRECTIONS:
                new_point = point + direction
                if self.data[new_point].passable and self.data[new_point].distance is None and new_point not in points:
                    points.append(new_point)
                    if point_distance := self.data[point].distance is None:
                        raise CalculationFailedError(f"Received point with not calculated distance: {point}")
                    self.data[new_point].distance = point_distance + 1
            points = sorted(points, key=self.heuristic_function)
        return path_found

    def heuristic_function(self, point: Point) -> int:
        """Calculate the heuristic function for a given point.

        Args:
            point: The point for which to calculate the function.

        Returns:
            Value of the heuristic function (square of the distance to the target point).

        Raises:
            DataNotProvidedError: if end point not provided.
        """
        if not self.end_point:
            raise DataNotProvidedError("End point not provided")
        return (self.end_point.x - point.x) ** 2 + (self.end_point.y - point.y) ** 2
