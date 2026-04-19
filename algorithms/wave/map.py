"""Map handling for the wave algorithm."""

from ..base import DIRECTIONS, Map
from ..math_handlers import Point


class WaveMap(Map):
    """Wave method map containing passable and impassable points."""

    def _find_path(self, points: list[Point]) -> bool:
        """Find a path in the maze by iterating points.

        Returns:
            True / False whether path was found..
        """
        distance = 0
        path_found = False
        while points and not path_found:
            new_points = []
            for point in points:
                if point == self.end_point:
                    path_found = True
                self.data[point].distance = distance
                for direction in DIRECTIONS:
                    new_point = point + direction
                    if (
                        self.data[new_point].passable
                        and self.data[new_point].distance is None
                        and new_point not in new_points
                    ):
                        new_points.append(new_point)
            points = new_points
            distance += 1
        return path_found
