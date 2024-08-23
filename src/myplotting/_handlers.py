from matplotlib.legend_handler import HandlerBase
from matplotlib.patches import Rectangle, Circle


class HandlerQuantile(HandlerBase):
    def create_artists(
        self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans
    ):
        mk = orig_handle.markers[0]
        ln = orig_handle.thinlines[0]

        # Thin rectangle to represent the thin lines:
        w0 = width
        h0 = height / 20
        xy0 = (xdescent, ydescent + height / 2 - h0 / 2)
        rect0 = Rectangle(xy0, w0, h0)
        rect0.set_color(ln.get_color())

        # Thick rectangle to represent the thick lines:
        w1 = width * 0.50
        h1 = height / 4
        xy1 = (xdescent + width * 0.25, ydescent + height / 2 - h1 / 2)
        rect1 = Rectangle(xy1, w1, h1)
        rect1.set_color(ln.get_color())

        # Circle for the marker:
        radius = height / 3
        circ = Circle((xdescent + width / 2, ydescent + height / 2), radius)
        circ.set_facecolor(mk.get_markerfacecolor())
        circ.set_edgecolor(ln.get_color())
        circ.set_linewidth(mk.get_markeredgewidth())

        artists = [rect0, rect1, circ]
        for artist in artists:
            artist.set_transform(trans)
        return artists
