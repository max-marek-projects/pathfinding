"""Processing visual display of the A* method."""

from ..base import Graphic
from .map import AStarMap


class AStarGraphic(Graphic[AStarMap]):
    """Handler for visual display of the A* method."""

    MAP_TYPE = AStarMap
