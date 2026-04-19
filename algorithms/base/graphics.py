"""Visual display handlers for different algorithms."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import wraps
from traceback import format_exc
from typing import TYPE_CHECKING, Concatenate, ParamSpec, TypeVar

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import Event, MouseButton, MouseEvent
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.text import Text
from matplotlib.widgets import Button, TextBox

from ..exceptions import WrongActionError
from ..logging import logger
from ..math_handlers import Point

if TYPE_CHECKING:
    from algorithms.base import Map

DecParams = ParamSpec("DecParams")
RetVar = TypeVar("RetVar")
GraphicType = TypeVar("GraphicType", bound="Graphic[Map]")


def handle_error(
    message: str = "",
) -> Callable[
    [Callable[Concatenate[GraphicType, DecParams], RetVar]],
    Callable[Concatenate[GraphicType, DecParams], RetVar | None],
]:
    """Handle an exception when processing interaction with graphical elements.

    Returns:
        Function decorator.
    """

    def decorate(
        function: Callable[Concatenate[GraphicType, DecParams], RetVar],
    ) -> Callable[Concatenate[GraphicType, DecParams], RetVar | None]:

        @wraps(function)
        def wrapper(self: GraphicType, *args: DecParams.args, **kwargs: DecParams.kwargs) -> RetVar | None:
            self.clear_exception()
            try:
                return function(self, *args, **kwargs)
            except Exception as ex:
                logger.error(format_exc())
                if message:
                    self.perform_exception(WrongActionError(f"{message}\n{ex!s}"))
                else:
                    self.perform_exception(WrongActionError(str(ex)))
                return None

        return wrapper

    return decorate


class Graphic[MapType: Map](ABC):
    """Handler for visual display of the map."""

    @property
    @abstractmethod
    def MAP_TYPE(self) -> type[MapType]:
        """Type of map for current graphic."""
        ...

    fig: Figure
    ax: Axes
    event_id: int
    data: AxesImage

    def __init__(self, width: int = 10, height: int = 10) -> None:
        """Initialize the map visual display handler.

        Args:
            width: Desired maze width.
            height: Desired maze height.
        """
        self.map = self.MAP_TYPE()
        self.map.width = width
        self.map.height = height

    def delete_start_arrow(self) -> None:
        """Delete the start point of the maze."""
        if hasattr(self, "start_arrow"):
            self.start_arrow.remove()
            del self.start_arrow
            self.map.start_point = None

    def delete_end_arrow(self) -> None:
        """Delete the end point of the maze."""
        if hasattr(self, "end_arrow"):
            self.end_arrow.remove()
            del self.end_arrow
            self.map.end_point = None

    def delete_path(self) -> None:
        """Delete the path."""
        if hasattr(self, "path"):
            for line in self.path:
                line.remove()
            del self.path
            self.map.clear()

    @handle_error("Failed to select the start point position")
    def on_click_after_start(self, event: Event) -> None:
        """Handle a click on the map after pressing the "Set start point" button.

        Args:
            event: Click event.

        Raises:
            WrongActionError: if clicked point is outside of the field.
        """
        if isinstance(event, MouseEvent):
            if event.button is MouseButton.LEFT:
                if not event.xdata or not event.ydata:
                    raise WrongActionError("Clicked point is outside the field")
                point = Point(round(event.xdata), round(event.ydata))
                self.map.start_point = point
                self.start_arrow = self.ax.arrow(
                    point.x - 0.4,
                    point.y,
                    0.5,
                    0,
                    fc="green",
                    ec="green",
                    head_width=0.3,
                    head_length=0.3,
                )
                plt.show()
                plt.disconnect(self.event_id)

    @handle_error("Failed to select the end point position")
    def on_click_after_end(self, event: Event) -> None:
        """Handle a click on the map after pressing the "Set end point" button.

        Args:
            event: Click event.

        Raises:
            WrongActionError: if clicked point is outside of the field.
        """
        if isinstance(event, MouseEvent):
            if event.button is MouseButton.LEFT:
                if not event.xdata or not event.ydata:
                    raise WrongActionError("Clicked point is outside the field")
                point = Point(round(event.xdata), round(event.ydata))
                self.map.end_point = point
                self.end_arrow = self.ax.arrow(
                    point.x - 0.4,
                    point.y,
                    0.5,
                    0,
                    fc="blue",
                    ec="blue",
                    head_width=0.3,
                    head_length=0.3,
                )
                plt.show()
                plt.disconnect(self.event_id)

    @handle_error("Failed to click the start point button")
    def click_start_button(self, event: Event) -> None:
        """Handle a click on the "Set start point" button.

        Args:
            event: Click event.
        """
        if hasattr(self, "event_id"):
            plt.disconnect(self.event_id)
        self.delete_start_arrow()
        self.delete_path()
        plt.show()
        self.event_id = plt.connect("button_press_event", self.on_click_after_start)

    @handle_error("Failed to click the end point button")
    def click_end_button(self, event: Event) -> None:
        """Handle a click on the "Set end point" button.

        Args:
            event: Click event.
        """
        if hasattr(self, "event_id"):
            plt.disconnect(self.event_id)
        self.delete_end_arrow()
        self.delete_path()
        plt.show()
        self.event_id = plt.connect("button_press_event", self.on_click_after_end)

    @handle_error("Failed to click the clear map button")
    def click_clear(self, event: Event) -> None:
        """Handle a click on the "Clear" button.

        Args:
            event: Click event.
        """
        self.delete_start_arrow()
        self.delete_end_arrow()
        self.delete_path()
        plt.show()

    @handle_error("Failed to set the number of rows")
    def x_change(self, event: str) -> None:
        """Handle text input in the "Number of rows" field.

        Args:
            event: text of event.
        """
        try:
            self.map.width = self.x_input.text
        except Exception as ex:
            self.x_input.set_val(str(self.map.width))
            raise ex

    @handle_error("Failed to set the number of columns")
    def y_change(self, event: str) -> None:
        """Handle text input in the "Number of columns" field.

        Args:
            event: text of event.
        """
        try:
            self.map.height = self.y_input.text
        except Exception as ex:
            self.y_input.set_val(str(self.map.height))
            raise ex

    def plot_map(self) -> None:
        """Display the map."""
        self.map.generate_map()
        self.ax.cla()
        self.error_text = self.ax.text(
            0.5,
            -0.05,
            "",
            transform=self.ax.transAxes,
            style="italic",
            horizontalalignment="center",
            verticalalignment="top",
            bbox={"facecolor": "red", "alpha": 0.5, "pad": 10},
        )
        self.data = self.ax.imshow(
            [[0 if cell.passable else 1 for cell in row] for row in self.map.data.data],
            cmap="binary",
            interpolation="none",
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        plt.show()

    @handle_error("Failed to change the map")
    def map_change(self, event: Event) -> None:
        """Handle a click on the "Change map" button.

        Args:
            event: Click event.
        """
        self.click_clear(event)
        self.plot_map()

    @handle_error("Failed to find a path")
    def find_path(self, event: Event) -> None:
        """Handle a click on the "Find path" button.

        Args:
            event: Click event.
        """
        self.delete_path()
        path = self.map.find_path()
        self.path = self.ax.plot([point.x for point in path], [point.y for point in path])
        plt.show()

    def draw_maze(self) -> None:
        """Render the maze.

        Raises:
            WrongActionError: if wrong structure found.
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 10))

        # Control buttons
        RIGHT_POSITION = 0.9
        WIDTH = 0.1
        HEIGHT = 0.075
        MIDDLE_POSITION = 0.5

        axstart = self.fig.add_axes((RIGHT_POSITION, MIDDLE_POSITION + 0.25, WIDTH, HEIGHT))
        axend = self.fig.add_axes((RIGHT_POSITION, MIDDLE_POSITION, WIDTH, HEIGHT))
        axclear = self.fig.add_axes((RIGHT_POSITION, MIDDLE_POSITION - 0.25, WIDTH, HEIGHT))
        self.start_button = Button(axstart, "Set\nstart\npoint")
        self.start_button.on_clicked(self.click_start_button)
        self.end_button = Button(axend, "Set\nend\npoint")
        self.end_button.on_clicked(self.click_end_button)
        self.clear_button = Button(axclear, "Clear")
        self.clear_button.on_clicked(self.click_clear)

        # Input fields
        LEFT_POSITION = 0

        ax_x_input = self.fig.add_axes((LEFT_POSITION, MIDDLE_POSITION + 0.3, WIDTH, HEIGHT))
        ax_y_input = self.fig.add_axes((LEFT_POSITION, MIDDLE_POSITION + 0.1, WIDTH, HEIGHT))
        self.x_input = TextBox(ax_x_input, "Number of\nrows:", "10", textalignment="center")
        x_label = self.x_input.ax.get_children()[0]
        if not isinstance(x_label, Text):
            raise WrongActionError("Found label other than text block")
        x_label.set_position((0.5, 1.5))
        x_label.set_verticalalignment("top")
        x_label.set_horizontalalignment("center")
        self.x_input.on_submit(self.x_change)
        self.y_input = TextBox(ax_y_input, "Number of\ncolumns:", "10", textalignment="center")
        self.y_input.on_submit(self.y_change)
        y_label = self.y_input.ax.get_children()[0]
        if not isinstance(y_label, Text):
            raise WrongActionError("Found label other than text block")
        y_label.set_position((0.5, 1.5))
        y_label.set_verticalalignment("top")
        y_label.set_horizontalalignment("center")

        # Map control buttons
        ax_map_rebuild = self.fig.add_axes((LEFT_POSITION, MIDDLE_POSITION - 0.1, WIDTH, HEIGHT))
        self.map_rebuild_button = Button(ax_map_rebuild, "Change\nmap")
        self.map_rebuild_button.on_clicked(self.map_change)

        # Algorithm control buttons
        ax_find_path = self.fig.add_axes((LEFT_POSITION, MIDDLE_POSITION - 0.3, WIDTH, HEIGHT))
        self.find_path_button = Button(ax_find_path, "Find\npath")
        self.find_path_button.on_clicked(self.find_path)

        # Error text field
        self.plot_map()

    def perform_exception(self, exception: Exception) -> None:
        """Execute when an exception is raised.

        Args:
            exception: Exception to handle.
        """
        self.error_text.set_text(str(exception))
        plt.show()

    def clear_exception(self) -> None:
        """Clear the exception message."""
        self.error_text.set_text("")
        plt.show()
