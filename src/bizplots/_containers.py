from matplotlib.lines import Line2D
from matplotlib.container import Container


class QuantileContainer(Container):
    def __init__(
        self,
        thinlines: list[Line2D],
        thicklines: list[Line2D],
        markers: list[Line2D],
        *,
        orientation: str | None = None,
        **kwargs,
    ):
        self.thinlines = thinlines
        self.thicklines = thicklines
        self.markers = markers
        self.orientation = orientation
        all_lines = thinlines + thicklines + markers
        super().__init__(all_lines, **kwargs)


class SpaghettiContainer(Container):
    def __init__(
        self,
        lines: list[Line2D],
        **kwargs,
    ):
        self.lines = lines
        super().__init__(lines, **kwargs)


class RibbonsContainer(Container):
    def __init__(
        self,
        collections,
        **kwargs,
    ):
        self.collections = collections
        super().__init__(collections, **kwargs)
