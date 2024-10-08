import matplotlib as mpl
import matplotlib.cbook as cbook
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import numpy as np

from ._containers import QuantileContainer, SpaghettiContainer, RibbonsContainer


def _pct_line(position, samples, percentile, orientation="vertical", **kwargs):
    """
    Creates a Line2D object representing the specified percentile range
    of the data samples at a given position.

    Parameters:
    position (float): The position on the axis where the line will be drawn.
    samples (array-like): Data samples from which to calculate the percentile.
    percentile (float): The percentile range to calculate (e.g., 95 for the 95% range).
    orientation (str, optional): Orientation of the line, either 'vertical' or 'horizontal'. Default is 'vertical'.
    **kwargs: Additional keyword arguments passed to Line2D.

    Returns:
    mlines.Line2D: The Line2D object representing the percentile range.
    """
    mid = 50
    offset = percentile / 2
    lo, hi = mid - offset, mid + offset
    y1, y2 = np.percentile(samples, q=[lo, hi])
    x = [position, position]
    y = [y1, y2]
    if orientation == "horizontal":
        x, y = y, x

    line = mlines.Line2D(x, y, **kwargs, label="_nolegend_")
    return line


def _mid_marker(position, samples, orientation="vertical", **kwargs):
    """
    Creates a Line2D object representing the median of the data samples at a given position.

    Parameters:
    position (float): The position on the axis where the marker will be drawn.
    samples (array-like): Data samples from which to calculate the median.
    orientation (str, optional): Orientation of the marker, either 'vertical' or 'horizontal'. Default is 'vertical'.
    **kwargs: Additional keyword arguments passed to Line2D.

    Returns:
    mlines.Line2D: The Line2D object representing the median marker.
    """
    x = [position]
    y = [np.median(samples)]
    if orientation == "horizontal":
        x, y = y, x

    # usually white:
    fill_color = mpl.pyplot.rcParams["figure.facecolor"]
    marker = mlines.Line2D(
        x, y, marker="o", mfc=fill_color, label="_nolegend_", **kwargs
    )
    return marker


def _box(position, samples, pct_inner, pct_outer, orientation="vertical", **kwargs):
    """
    Creates a box consisting of two percentile lines and a median marker
    for the given data samples at a specified position.

    Parameters:
    position (float): The position on the axis where the box will be drawn.
    samples (array-like): Data samples from which to calculate the percentiles and median.
    pct_inner (float): The inner percentile range (e.g., 50 for the 50% range).
    pct_outer (float): The outer percentile range (e.g., 95 for the 95% range).
    orientation (str, optional): Orientation of the box, either 'vertical' or 'horizontal'. Default is 'vertical'.
    **kwargs: Additional keyword arguments passed to Line2D.

    Returns:
    tuple: A tuple containing the outer percentile line, inner percentile line, and median marker.
    """
    thin_line = _pct_line(position, samples, pct_outer, orientation, **kwargs)
    thick_line = _pct_line(position, samples, pct_inner, orientation, **kwargs)
    marker = _mid_marker(position, samples, orientation, **kwargs)
    return thin_line, thick_line, marker


def _plot_quantiles1d(
    positions,
    samples,
    pct_inner=50,
    pct_outer=95,
    orientation="vertical",
    ax=None,
    **kwargs,
):
    """
    Plots quantiles for 1D data at specified positions.

    Parameters:
    positions (array-like): Positions at which to plot the quantiles.
    samples (array-like): Data samples for which the quantiles are calculated.
    pct_inner (float, optional): The inner percentile range (default is 50).
    pct_outer (float, optional): The outer percentile range (default is 95).
    orientation (str, optional): Orientation of the plot, either 'vertical' or 'horizontal'. Default is 'vertical'.
    ax (matplotlib.axes.Axes, optional): The axes on which to draw the plot. If None, uses the current axes.
    **kwargs: Additional keyword arguments passed to Line2D.

    Returns:
    QuantileContainer: A container holding the plotted quantiles, which includes
                       thin lines, thick lines, and markers.
    """
    if ax is None:
        ax = mpl.pyplot.gca()

    kwargs = cbook.normalize_kwargs(kwargs, mlines.Line2D)
    linewidth = kwargs.pop("linewidth", mpl.rcParams["lines.linewidth"])
    color = kwargs.pop("color", None)
    if color is None:
        color = ax._get_patches_for_fill.get_next_color()
    color = mcolors.to_rgba_array(color)
    container_label = kwargs.pop("label", None)

    outer_lines = []
    inner_lines = []
    mid_markers = []
    for pos in np.unique(positions):
        mask = positions == pos
        l1, l2, m = _box(
            pos, samples[mask], pct_inner, pct_outer, orientation, **kwargs
        )
        l1._internal_update({"color": color, "linewidth": 0.8 * linewidth})
        l2._internal_update({"color": color, "linewidth": 1.8 * linewidth})
        m._internal_update({"color": color, "linewidth": 1.5 * linewidth})
        outer_lines.append(l1)
        inner_lines.append(l2)
        mid_markers.append(m)
        ax.add_line(l1)
        ax.add_line(l2)
        ax.add_line(m)

    ax._request_autoscale_view()
    container = QuantileContainer(
        outer_lines, inner_lines, mid_markers, label=container_label
    )
    ax.add_container(container)
    return container


def _plot_quantiles2d(
    positions,
    samples,
    pct_inner=50,
    pct_outer=95,
    orientation="vertical",
    ax=None,
    **kwargs,
):
    """
    Plots quantiles for 2D data at specified positions.

    Parameters:
    positions (array-like): Positions at which to plot the quantiles.
    samples (array-like): 2D data samples for which the quantiles are calculated.
    pct_inner (float, optional): The inner percentile range (default is 50).
    pct_outer (float, optional): The outer percentile range (default is 95).
    orientation (str, optional): Orientation of the plot, either 'vertical' or 'horizontal'. Default is 'vertical'.
    ax (matplotlib.axes.Axes, optional): The axes on which to draw the plot. If None, uses the current axes.
    **kwargs: Additional keyword arguments passed to Line2D.

    Returns:
    QuantileContainer: A container holding the plotted quantiles, which includes
                       thin lines, thick lines, and markers.
    """
    if ax is None:
        ax = mpl.pyplot.gca()

    kwargs = cbook.normalize_kwargs(kwargs, mlines.Line2D)
    linewidth = kwargs.pop("linewidth", mpl.rcParams["lines.linewidth"])
    color = kwargs.pop("color", None)
    if color is None:
        color = ax._get_patches_for_fill.get_next_color()
    color = mcolors.to_rgba_array(color)
    container_label = kwargs.pop("label", None)

    outer_lines = []
    inner_lines = []
    mid_markers = []
    for pos, sam in zip(positions, samples.T):
        l1, l2, m = _box(pos, sam, pct_inner, pct_outer, orientation, **kwargs)
        l1._internal_update({"color": color, "linewidth": 0.8 * linewidth})
        l2._internal_update({"color": color, "linewidth": 1.8 * linewidth})
        m._internal_update({"color": color, "linewidth": 1.5 * linewidth})
        outer_lines.append(l1)
        inner_lines.append(l2)
        mid_markers.append(m)
        ax.add_line(l1)
        ax.add_line(l2)
        ax.add_line(m)

    ax._request_autoscale_view()
    container = QuantileContainer(
        outer_lines, inner_lines, mid_markers, label=container_label
    )
    ax.add_container(container)
    return container


def plot_quantiles(
    positions,
    samples,
    pct_inner=50,
    pct_outer=95,
    orientation="vertical",
    ax=None,
    **kwargs,
):
    """Plot quantiles and median for the data samples at the specified positions

    Args:
        positions (array-like, numeric):
            Positions corresponding to the data samples
        samples (array-like, numeric):
            Data samples for which the quantiles will be calculated
        pct_inner (float, optional):
            Inner percentile to be plotted. Defaults to 50.
        pct_outer (float, optional):
            Outer percentile to be plotted. Defaults to 95.
        orientation (str, optional):
            Orientation of the lines, either "vertical" or "horizontal".
        ax (matplotlib.Axes, optional):
            Axes where the plot will be drawn.

    Raises:
        NotImplementedError: When dimensions of the data provided are not supported.

    Returns:
        QuantileContainer:
            matplotilib container object with the lines representing the quantiles and
            the markers for the medians.
    """
    positions = np.asarray(positions)
    samples = np.asarray(samples)
    _kwargs = {
        "positions": positions,
        "samples": samples,
        "pct_inner": pct_inner,
        "pct_outer": pct_outer,
        "orientation": orientation,
        "ax": ax,
    }
    _kwargs.update(kwargs)
    if np.ndim(samples) == np.ndim(positions) == 1:
        return _plot_quantiles1d(**_kwargs)
    elif (np.ndim(samples) == 2) and (np.ndim(positions) == 1):
        return _plot_quantiles2d(**_kwargs)
    else:
        raise NotImplementedError


def plot_spaghetti(
    x,
    y,
    samples=20,
    random_state=None,
    ax=None,
    **kwargs,
):
    """Plot a few randomly selected (x, y) pairs.

    Args:
        x (array-like):
            The x-values to be plotted, shape is (num_observations,)
        y (array-like):
            An array of samples, each sample is a possible realization of `y`.
            The shape should be (num_samples, num_observations)
        samples (int or array-like, optional):
            If an int, it's interpreted as the number of samples to plot.
            If an array, it is used to select the samples of `y` that will be plotted
            and indexing is done along the axis=0 of `y`. Defaults to 20.
        random_state (int | None, optional):
            Seed for the numpy random generator. Defaults to None. Only relevant
            if the `samples` argument is an integer.
        ax (matplotlib.Axes, optional):
            Where the lines will be plotted. If None, it will use the current ax.

    Raises:
        ValueError: When `samples` is not an int or a valid index for `y`.

    Returns:
        SpaghettiContainer:
            A matplotlib container with the selected lines.
            Supports a custom legend style.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    if np.ndim(samples) == 0:  # integer was given:
        num_y_samples = len(y)
        rng = np.random.default_rng(random_state)
        indices = rng.choice(num_y_samples, size=samples, replace=False)
    elif np.ndim(samples) == 1:  # array of indices was provided
        indices = samples
    else:
        raise ValueError

    if ax is None:
        ax = mpl.pyplot.gca()

    kwargs = cbook.normalize_kwargs(kwargs, mlines.Line2D)
    color = kwargs.pop("color", None)
    if color is None:
        color = ax._get_patches_for_fill.get_next_color()
    color = mcolors.to_rgba_array(color)
    kwargs["color"] = color
    kwargs["alpha"] = kwargs.pop("alpha", 0.5)
    container_label = kwargs.pop("label", None)

    lines = []
    for idx in indices:
        line = mlines.Line2D(x, y[idx], label="_nolegend_", **kwargs)
        lines.append(line)
        ax.add_line(line)

    ax._request_autoscale_view()
    container = SpaghettiContainer(lines, label=container_label)
    ax.add_container(container)
    return container


def plot_ribbons(
    x,
    y,
    num_ribbons=10,
    percentile_min=2.5,
    percentile_max=97.5,
    ax=None,
    **kwargs,
):
    """
    Make a ribbon plot that shows the different quantiles of the
    distribution of y against x.

    Args:
        x: 1d array
            The values for the x axis
        y: 2d array
        num_ribbons: int (default 10)
            How many quantiles to show
        percentile_min: float, between 0 and 50
            The lowest percentile to be shown
        percentile_max: float between 50 and 100
            The highest percentile to show.
        ax: matplotlib.Axes
            Where to plot the figure.
        kwargs: dict
            Extra arguments passed to `plt.fill_between`.
            Controls the aspect of the ribbons.

    Returns:
        matplotlib.Axes
    """
    if ax is None:
        ax = mpl.pyplot.gca()

    lower = np.linspace(percentile_min, 50, num=num_ribbons, endpoint=False)
    upper = np.linspace(50, percentile_max, num=num_ribbons + 1)[1:]
    perc1 = np.percentile(y, lower, axis=0)
    perc2 = np.percentile(y, upper, axis=0)

    # fix some kwargs:
    alpha = kwargs.pop("alpha", 1)
    alpha = alpha / num_ribbons
    kwargs["alpha"] = alpha
    color = kwargs.pop("color", None)
    if color is None:
        color = ax._get_patches_for_fill.get_next_color()
    color = mcolors.to_rgba_array(color)
    kwargs["color"] = color
    container_label = kwargs.pop("label", None)

    polygon_collections = []
    for p1, p2 in zip(perc1, perc2):
        collection = ax.fill_between(x, p1, p2, label="_nolegend_", **kwargs)
        polygon_collections.append(collection)

    container = RibbonsContainer(polygon_collections, label=container_label)
    ax.add_container(container)
    return ax
