"""Processing visual display of the wave method."""

from ..base import Graphic
from .map import WaveMap


class WaveGraphic(Graphic[WaveMap]):
    """Handler for visual display of the wave method."""

    MAP_TYPE = WaveMap
